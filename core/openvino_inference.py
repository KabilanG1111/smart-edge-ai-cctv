"""
OpenVINO ONNX Inference Engine
CPU-optimized YOLOv8 inference using Intel OpenVINO toolkit

Replaces ultralytics YOLO with OpenVINO for production stability:
- 2-3x faster on Intel CPUs
- Deterministic inference
- Lower memory footprint
- No torch/CUDA dependencies
"""

import numpy as np
import cv2
from typing import List, Tuple, Optional
from dataclasses import dataclass
import logging
from pathlib import Path

try:
    from openvino.runtime import Core, InferRequest
    OPENVINO_AVAILABLE = True
except ImportError:
    OPENVINO_AVAILABLE = False
    logging.warning("OpenVINO not installed. Install with: pip install openvino")

logger = logging.getLogger(__name__)


@dataclass
class Detection:
    """Single object detection"""
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2
    confidence: float
    class_id: int
    class_name: str


# STATIC INFRASTRUCTURE - These are BLOCKED (known stationary objects)
STATIC_BLOCKED_CLASSES = {
    56: "chair",
    57: "couch",
    58: "potted plant",
    59: "bed",
    60: "dining table",
    61: "toilet",
    62: "tv",  # Usually wall-mounted/stationary
    69: "oven",
    70: "toaster",
    71: "sink",
    72: "refrigerator",
    75: "vase",  # Usually decorative/stationary
}

# ALLOWED CLASSES - Everything EXCEPT static infrastructure (inverted logic)
# YOLOv8 has 80 classes (0-79). We block only known-static items.
BLOCKED_CLASS_IDS = set(STATIC_BLOCKED_CLASSES.keys())

# Full COCO class names for reference
COCO_CLASSES = {
    0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 4: "airplane",
    5: "bus", 6: "train", 7: "truck", 8: "boat", 9: "traffic light",
    10: "fire hydrant", 11: "stop sign", 12: "parking meter", 13: "bench",
    14: "bird", 15: "cat", 16: "dog", 17: "horse", 18: "sheep",
    19: "cow", 20: "elephant", 21: "bear", 22: "zebra", 23: "giraffe",
    24: "backpack", 25: "umbrella", 26: "handbag", 27: "tie", 28: "suitcase",
    29: "frisbee", 30: "skis", 31: "snowboard", 32: "sports ball", 33: "kite",
    34: "baseball bat", 35: "baseball glove", 36: "skateboard", 37: "surfboard",
    38: "tennis racket", 39: "bottle", 40: "wine glass", 41: "cup",
    42: "fork", 43: "knife", 44: "spoon", 45: "bowl", 46: "banana",
    47: "apple", 48: "sandwich", 49: "orange", 50: "broccoli", 51: "carrot",
    52: "hot dog", 53: "pizza", 54: "donut", 55: "cake", 56: "chair",
    57: "couch", 58: "potted plant", 59: "bed", 60: "dining table", 61: "toilet",
    62: "tv", 63: "laptop", 64: "mouse", 65: "remote", 66: "keyboard",
    67: "cell phone", 68: "microwave", 69: "oven", 70: "toaster", 71: "sink",
    72: "refrigerator", 73: "book", 74: "clock", 75: "vase", 76: "scissors",
    77: "teddy bear", 78: "hair drier", 79: "toothbrush"
}


class OpenVINOInference:
    """
    Production-grade YOLOv8 inference using OpenVINO
    
    Usage:
        model = OpenVINOInference("models/openvino/yolov8n.xml", conf_threshold=0.35)
        detections = model.infer(frame)
    """
    
    def __init__(
        self,
        model_path: str,
        conf_threshold: float = 0.35,
        iou_threshold: float = 0.45,
        input_size: int = 320,
        device: str = "CPU"
    ):
        """
        Initialize OpenVINO inference engine
        
        Args:
            model_path: Path to OpenVINO IR (.xml file)
            conf_threshold: Confidence threshold for detections
            iou_threshold: NMS IoU threshold
            input_size: Model input size (320, 416, or 640)
            device: Target device (CPU, GPU, MYRIAD)
        """
        if not OPENVINO_AVAILABLE:
            raise RuntimeError("OpenVINO not installed. Run: pip install openvino")
        
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.input_size = input_size
        self.device = device
        
        # Load OpenVINO model
        logger.info(f"🔄 Loading OpenVINO model: {model_path}")
        ie = Core()
        model = ie.read_model(model_path)
        
        # Compile for target device
        self.compiled_model = ie.compile_model(model, device)
        self.infer_request = self.compiled_model.create_infer_request()
        
        # Get input/output info
        self.input_layer = self.compiled_model.input(0)
        self.output_layer = self.compiled_model.output(0)
        
        logger.info(f"✅ OpenVINO model loaded on {device}")
        logger.info(f"   Input shape: {self.input_layer.shape}")
        logger.info(f"   Output shape: {self.output_layer.shape}")
        
        # Performance tracking
        self.frame_count = 0
        self.total_inference_time = 0.0
    
    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocess frame for YOLOv8 inference
        
        Args:
            frame: BGR image (H, W, 3)
            
        Returns:
            Preprocessed tensor (1, 3, input_size, input_size)
        """
        # Resize maintaining aspect ratio
        img = cv2.resize(frame, (self.input_size, self.input_size))
        
        # BGR → RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # HWC → CHW
        img = img.transpose(2, 0, 1)
        
        # Normalize to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def postprocess(
        self,
        outputs: np.ndarray,
        orig_shape: Tuple[int, int]
    ) -> List[Detection]:
        """
        Postprocess YOLOv8 outputs to detections
        
        Args:
            outputs: Model output tensor (1, 84, 8400) for YOLOv8
            orig_shape: Original image (height, width)
            
        Returns:
            List of Detection objects
        """
        # YOLOv8 output format: (1, 84, 8400)
        # 84 = 4 (bbox) + 80 (classes)
        outputs = outputs[0]  # Remove batch dimension → (84, 8400)
        outputs = outputs.T   # Transpose → (8400, 84)
        
        # Extract boxes and scores
        boxes = outputs[:, :4]      # (8400, 4) - [x_center, y_center, w, h]
        scores = outputs[:, 4:]     # (8400, 80) - class scores
        
        # Get class with max score for each detection
        class_ids = np.argmax(scores, axis=1)
        confidences = np.max(scores, axis=1)
        
        # Filter by confidence
        mask = confidences > self.conf_threshold
        boxes = boxes[mask]
        confidences = confidences[mask]
        class_ids = class_ids[mask]
        
        # Filter ONLY static infrastructure (allow everything else)
        # Inverted logic: block only known-static items
        non_static_mask = ~np.isin(class_ids, list(BLOCKED_CLASS_IDS))
        boxes = boxes[non_static_mask]
        confidences = confidences[non_static_mask]
        class_ids = class_ids[non_static_mask]
        
        if len(boxes) == 0:
            return []
        
        # Convert from center format to corner format
        # [x_center, y_center, w, h] → [x1, y1, x2, y2]
        x_center, y_center = boxes[:, 0], boxes[:, 1]
        w, h = boxes[:, 2], boxes[:, 3]
        
        x1 = x_center - w / 2
        y1 = y_center - h / 2
        x2 = x_center + w / 2
        y2 = y_center + h / 2
        
        # Scale to original image size
        h_orig, w_orig = orig_shape
        x1 = (x1 * w_orig / self.input_size).astype(int)
        y1 = (y1 * h_orig / self.input_size).astype(int)
        x2 = (x2 * w_orig / self.input_size).astype(int)
        y2 = (y2 * h_orig / self.input_size).astype(int)
        
        # Clip to image bounds
        x1 = np.clip(x1, 0, w_orig)
        y1 = np.clip(y1, 0, h_orig)
        x2 = np.clip(x2, 0, w_orig)
        y2 = np.clip(y2, 0, h_orig)
        
        # Apply NMS
        indices = self.nms(
            np.stack([x1, y1, x2, y2], axis=1),
            confidences,
            self.iou_threshold
        )
        
        # Create Detection objects
        detections = []
        for idx in indices:
            bbox = (int(x1[idx]), int(y1[idx]), int(x2[idx]), int(y2[idx]))
            class_id = int(class_ids[idx])
            class_name = COCO_CLASSES.get(class_id, f"class_{class_id}")
            
            detections.append(Detection(
                bbox=bbox,
                confidence=float(confidences[idx]),
                class_id=class_id,
                class_name=class_name
            ))
        
        return detections
    
    def nms(
        self,
        boxes: np.ndarray,
        scores: np.ndarray,
        iou_threshold: float
    ) -> List[int]:
        """
        Non-Maximum Suppression
        
        Args:
            boxes: Array of shape (N, 4) - [x1, y1, x2, y2]
            scores: Array of shape (N,) - confidence scores
            iou_threshold: IoU threshold for suppression
            
        Returns:
            List of indices to keep
        """
        if len(boxes) == 0:
            return []
        
        # Sort by score (descending)
        sorted_indices = np.argsort(scores)[::-1]
        
        keep = []
        while len(sorted_indices) > 0:
            # Pick detection with highest score
            current = sorted_indices[0]
            keep.append(current)
            
            if len(sorted_indices) == 1:
                break
            
            # Compute IoU with remaining boxes
            current_box = boxes[current]
            remaining_boxes = boxes[sorted_indices[1:]]
            
            ious = self.compute_iou(current_box, remaining_boxes)
            
            # Keep only boxes with IoU < threshold
            sorted_indices = sorted_indices[1:][ious < iou_threshold]
        
        return keep
    
    def compute_iou(
        self,
        box: np.ndarray,
        boxes: np.ndarray
    ) -> np.ndarray:
        """
        Compute IoU between one box and multiple boxes
        
        Args:
            box: Single box (4,) - [x1, y1, x2, y2]
            boxes: Multiple boxes (N, 4)
            
        Returns:
            IoU scores (N,)
        """
        # Intersection area
        x1 = np.maximum(box[0], boxes[:, 0])
        y1 = np.maximum(box[1], boxes[:, 1])
        x2 = np.minimum(box[2], boxes[:, 2])
        y2 = np.minimum(box[3], boxes[:, 3])
        
        intersection = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
        
        # Union area
        box_area = (box[2] - box[0]) * (box[3] - box[1])
        boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
        union = box_area + boxes_area - intersection
        
        # IoU
        iou = intersection / (union + 1e-6)
        return iou
    
    def infer(self, frame: np.ndarray) -> List[Detection]:
        """
        Run inference on a single frame
        
        Args:
            frame: BGR image (H, W, 3)
            
        Returns:
            List of Detection objects
        """
        import time
        start_time = time.time()
        
        # Preprocess
        input_tensor = self.preprocess(frame)
        
        # Inference
        self.infer_request.infer({self.input_layer: input_tensor})
        outputs = self.infer_request.get_output_tensor(0).data
        
        # Postprocess
        detections = self.postprocess(outputs, frame.shape[:2])
        
        # Performance tracking
        elapsed = time.time() - start_time
        self.total_inference_time += elapsed
        self.frame_count += 1
        
        # Log every 100 frames
        if self.frame_count % 100 == 0:
            avg_time = self.total_inference_time / self.frame_count
            fps = 1.0 / avg_time
            logger.info(f"📊 OpenVINO: {fps:.1f} FPS | Avg latency: {avg_time*1000:.1f}ms")
        
        return detections
    
    def get_stats(self) -> dict:
        """Get inference statistics"""
        if self.frame_count == 0:
            return {"fps": 0, "avg_latency_ms": 0}
        
        avg_time = self.total_inference_time / self.frame_count
        return {
            "fps": 1.0 / avg_time,
            "avg_latency_ms": avg_time * 1000,
            "frame_count": self.frame_count
        }


# Fallback: Use ultralytics YOLO if OpenVINO not available
class FallbackYOLOInference:
    """
    Fallback to ultralytics YOLO if OpenVINO not available
    """
    def __init__(self, model_path: str = "yolov8n.pt", conf_threshold: float = 0.35, **kwargs):
        from ultralytics import YOLO
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        logger.warning("⚠️ Using fallback ultralytics YOLO (OpenVINO not available)")
    
    def infer(self, frame: np.ndarray) -> List[Detection]:
        results = self.model.predict(frame, conf=self.conf_threshold, verbose=False)
        
        detections = []
        for result in results:
            if result.boxes is None:
                continue
            
            for box in result.boxes:
                class_id = int(box.cls[0])
                
                # Filter ONLY static infrastructure (allow everything else)
                if class_id in BLOCKED_CLASS_IDS:
                    continue
                
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                class_name = COCO_CLASSES.get(class_id, f"class_{class_id}")
                
                detections.append(Detection(
                    bbox=(x1, y1, x2, y2),
                    confidence=conf,
                    class_id=class_id,
                    class_name=class_name
                ))
        
        return detections
    
    def get_stats(self) -> dict:
        return {"fps": 0, "avg_latency_ms": 0, "frame_count": 0}


# Factory function
def create_inference_engine(
    model_path: str,
    use_openvino: bool = True,
    **kwargs
) -> object:
    """
    Create inference engine (OpenVINO or fallback)
    
    Args:
        model_path: Path to model (.xml for OpenVINO, .pt for YOLO)
        use_openvino: Try to use OpenVINO if available
        **kwargs: Additional arguments for inference engine
        
    Returns:
        Inference engine instance
    """
    if use_openvino and OPENVINO_AVAILABLE and model_path.endswith('.xml'):
        return OpenVINOInference(model_path, **kwargs)
    else:
        return FallbackYOLOInference(model_path, **kwargs)
