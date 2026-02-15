"""
🔍 DETECTOR MODULE - Enterprise-Grade YOLOv8 Detection
=====================================================

Handles:
- Proper preprocessing (BGR→RGB, resize, normalize)
- ONNX/OpenVINO inference
- NMS filtering
- Class whitelisting
- CPU optimizations

Author: Production AI Team
License: Enterprise
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Detection:
    """Single detection with preprocessing metadata"""
    bbox: Tuple[float, float, float, float]  # x1, y1, x2, y2 (normalized 0-1)
    confidence: float
    class_id: int
    class_name: str
    
    def to_absolute(self, img_width: int, img_height: int) -> Tuple[int, int, int, int]:
        """Convert normalized bbox to absolute coordinates"""
        x1, y1, x2, y2 = self.bbox
        return (
            int(x1 * img_width),
            int(y1 * img_height),
            int(x2 * img_width),
            int(y2 * img_height)
        )


class YOLODetector:
    """
    Enterprise-grade YOLOv8 detector with stability optimizations
    
    Key Features:
    - Proper BGR→RGB conversion
    - Correct normalization (0-1 scaling)
    - Tuned confidence threshold (0.35 for stability)
    - Tuned IoU threshold (0.5 for NMS)
    - Class whitelisting (block flicker-prone classes)
    - CPU-optimized inference
    """
    
    # COCO class names (80 classes)
    COCO_CLASSES = {
        0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 5: 'bus',
        7: 'truck', 15: 'bird', 16: 'cat', 17: 'dog', 18: 'horse',
        26: 'handbag', 27: 'tie', 28: 'suitcase', 39: 'bottle', 40: 'wine glass',
        41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl',
        56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table',
        61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote',
        66: 'keyboard', 67: 'cell phone', 69: 'oven', 70: 'toaster',
        71: 'sink', 72: 'refrigerator', 73: 'book', 75: 'vase', 77: 'scissors',
        84: 'toothbrush'
    }
    
    # Classes prone to flickering - BLOCK THESE
    FLICKER_PRONE_CLASSES = {
        16: 'cat',       # Often confused with bag/shoe
        17: 'dog',       # Often confused with bag/furniture
        27: 'tie',       # Often confused with bottle/cup
        15: 'bird',      # Often confused with small objects
        18: 'horse',     # Rarely relevant in CCTV
        58: 'potted plant',  # Static, not useful
        75: 'vase',      # Static, causes confusion
    }
    
    # Billion-Dollar Detection: ALL 80 COCO classes enabled
    # Only blocking the 7 most problematic flicker classes
    ALLOWED_CLASSES = {
        # Core objects (most common)
        0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane',
        5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light',
        10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench',
        14: 'bird',  # Re-enabled (filtered later if causes issues)
        
        # Household items
        19: 'elephant', 20: 'bear', 21: 'zebra', 22: 'giraffe', 23: 'backpack',
        24: 'umbrella', 25: 'handbag', 26: 'tie',  # Re-enabled (filtered by FLICKER_PRONE)
        28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard',
        32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove',
        36: 'skateboard', 37: 'surfboard', 38: 'tennis racket',
        
        # Kitchen & dining
        39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife',
        44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich',
        49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza',
        54: 'donut', 55: 'cake',
        
        # Furniture (re-enabled for comprehensive detection)
        56: 'chair', 57: 'couch', 58: 'potted plant',  # Filtered by FLICKER_PRONE
        59: 'bed', 60: 'dining table', 61: 'toilet',
        
        # Electronics
        62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard',
        67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster',
        71: 'sink', 72: 'refrigerator',
        
        # Accessories & items
        73: 'book', 74: 'clock', 75: 'vase',  # Filtered by FLICKER_PRONE
        76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'
    }
    
    def __init__(
        self,
        model_path: str = "yolov8m.pt",      # UPGRADED: Medium model (50.2% mAP)
        input_size: int = 1280,                # HIGH-RES: 4x detail for small objects
        conf_threshold: float = 0.20,          # ULTRA-LOW: Maximum sensitivity
        iou_threshold: float = 0.40,           # OPTIMIZED: Better overlaps
        use_openvino: bool = False,
        use_class_whitelist: bool = False      # Detect ALL 80 COCO classes
    ):
        """
        Initialize detector
        
        Args:
            model_path: Path to YOLOv8 model (.pt, .onnx, or .xml)
            input_size: Model input size (640 for production)
            conf_threshold: Confidence threshold (0.35 recommended for stability)
            iou_threshold: IoU threshold for NMS (0.5 standard)
            use_openvino: Use OpenVINO if available
            use_class_whitelist: Filter to allowed classes only
        """
        self.model_path = model_path
        self.input_size = input_size
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.use_class_whitelist = use_class_whitelist
        
        # Initialize inference engine
        if use_openvino and (model_path.endswith('.xml') or model_path.endswith('.onnx')):
            self._init_openvino()
        else:
            self._init_ultralytics()
        
        logger.info(f"✅ Detector initialized: {model_path}")
        logger.info(f"   Conf threshold: {conf_threshold}")
        logger.info(f"   IoU threshold: {iou_threshold}")
        logger.info(f"   Class whitelist: {use_class_whitelist}")
        logger.info(f"   Allowed classes: {len(self.ALLOWED_CLASSES)}")
    
    def _init_openvino(self):
        """Initialize OpenVINO inference engine"""
        try:
            from openvino.runtime import Core
            
            self.ie = Core()
            
            # Load model
            if self.model_path.endswith('.xml'):
                model = self.ie.read_model(model=self.model_path)
            else:
                # Convert ONNX to IR on-the-fly
                model = self.ie.read_model(model=self.model_path)
            
            # Compile for CPU with optimizations
            self.compiled_model = self.ie.compile_model(model, "CPU", {
                "PERFORMANCE_HINT": "LATENCY",  # Optimize for single-frame latency
                "NUM_STREAMS": "1",  # Single stream for deterministic behavior
            })
            
            self.infer_request = self.compiled_model.create_infer_request()
            self.input_layer = self.compiled_model.input(0)
            self.output_layer = self.compiled_model.output(0)
            
            self.engine = "openvino"
            logger.info("✅ OpenVINO engine initialized")
            
        except Exception as e:
            logger.warning(f"OpenVINO init failed: {e}")
            logger.info("Falling back to ultralytics")
            self._init_ultralytics()
    
    def _init_ultralytics(self):
        """Initialize ultralytics YOLO (fallback)"""
        from ultralytics import YOLO
        
        self.model = YOLO(self.model_path)
        self.engine = "ultralytics"
        logger.info("✅ Ultralytics YOLO initialized")
    
    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocess frame for YOLOv8 inference
        
        CRITICAL: Proper preprocessing eliminates many false detections
        
        Steps:
        1. BGR → RGB conversion
        2. Resize to 640x640 (letterbox with padding)
        3. Normalize to 0-1 range
        4. Transpose to CHW format
        5. Add batch dimension
        
        Args:
            frame: Input BGR image (h, w, 3)
        
        Returns:
            Preprocessed tensor (1, 3, 640, 640)
        """
        # Step 1: BGR → RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Step 2: Letterbox resize (preserves aspect ratio + padding)
        h, w = rgb.shape[:2]
        scale = min(self.input_size / h, self.input_size / w)
        new_h, new_w = int(h * scale), int(w * scale)
        
        resized = cv2.resize(rgb, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        # Add padding to make square
        padded = np.full((self.input_size, self.input_size, 3), 114, dtype=np.uint8)
        pad_h = (self.input_size - new_h) // 2
        pad_w = (self.input_size - new_w) // 2
        padded[pad_h:pad_h+new_h, pad_w:pad_w+new_w] = resized
        
        # Step 3: Normalize to 0-1
        normalized = padded.astype(np.float32) / 255.0
        
        # Step 4: HWC → CHW
        transposed = normalized.transpose(2, 0, 1)
        
        # Step 5: Add batch dimension
        batched = np.expand_dims(transposed, axis=0)
        
        return batched
    
    def postprocess(
        self, 
        outputs: np.ndarray, 
        original_shape: Tuple[int, int]
    ) -> List[Detection]:
        """
        Postprocess YOLO outputs
        
        Args:
            outputs: Raw model outputs (1, 84, 8400) for YOLOv8
            original_shape: Original image (h, w)
        
        Returns:
            List of Detection objects
        """
        # YOLOv8 output format: (batch, 84, 8400)
        # 84 = 4 bbox coords + 80 class scores
        
        predictions = outputs[0]  # Remove batch dim: (84, 8400)
        predictions = predictions.T  # Transpose: (8400, 84)
        
        # Extract boxes and scores
        boxes = predictions[:, :4]  # (8400, 4) - xywh format
        scores = predictions[:, 4:]  # (8400, 80) - class scores
        
        # Get class IDs and confidences
        class_ids = np.argmax(scores, axis=1)
        confidences = np.max(scores, axis=1)
        
        # Filter by confidence
        mask = confidences >= self.conf_threshold
        boxes = boxes[mask]
        class_ids = class_ids[mask]
        confidences = confidences[mask]
        
        if len(boxes) == 0:
            return []
        
        # Convert xywh → xyxy
        x, y, w, h = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
        x1 = x - w / 2
        y1 = y - h / 2
        x2 = x + w / 2
        y2 = y + h / 2
        boxes_xyxy = np.stack([x1, y1, x2, y2], axis=1)
        
        # NMS
        keep_indices = self._nms(boxes_xyxy, confidences, self.iou_threshold)
        
        boxes_xyxy = boxes_xyxy[keep_indices]
        class_ids = class_ids[keep_indices]
        confidences = confidences[keep_indices]
        
        # Convert to Detection objects
        detections = []
        for box, class_id, conf in zip(boxes_xyxy, class_ids, confidences):
            class_id = int(class_id)
            
            # Class whitelist filtering
            if self.use_class_whitelist and class_id not in self.ALLOWED_CLASSES:
                continue
            
            # Block flicker-prone classes
            if class_id in self.FLICKER_PRONE_CLASSES:
                continue
            
            class_name = self.COCO_CLASSES.get(class_id, f"class_{class_id}")
            
            # Normalize bbox to 0-1
            x1, y1, x2, y2 = box
            x1 = max(0, min(1, x1 / self.input_size))
            y1 = max(0, min(1, y1 / self.input_size))
            x2 = max(0, min(1, x2 / self.input_size))
            y2 = max(0, min(1, y2 / self.input_size))
            
            detections.append(Detection(
                bbox=(x1, y1, x2, y2),
                confidence=float(conf),
                class_id=class_id,
                class_name=class_name
            ))
        
        return detections
    
    def _nms(
        self, 
        boxes: np.ndarray, 
        scores: np.ndarray, 
        iou_threshold: float
    ) -> np.ndarray:
        """
        Non-Maximum Suppression
        
        Args:
            boxes: (N, 4) array in xyxy format
            scores: (N,) array of confidence scores
            iou_threshold: IoU threshold for suppression
        
        Returns:
            Indices of boxes to keep
        """
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        
        areas = (x2 - x1) * (y2 - y1)
        order = scores.argsort()[::-1]
        
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            
            # Compute IoU
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            
            w = np.maximum(0.0, xx2 - xx1)
            h = np.maximum(0.0, yy2 - yy1)
            inter = w * h
            
            iou = inter / (areas[i] + areas[order[1:]] - inter)
            
            # Keep only low IoU boxes
            inds = np.where(iou <= iou_threshold)[0]
            order = order[inds + 1]
        
        return np.array(keep)
    
    def detect(self, frame: np.ndarray) -> List[Detection]:
        """
        Run detection on frame
        
        Args:
            frame: Input BGR image
        
        Returns:
            List of Detection objects
        """
        original_shape = frame.shape[:2]
        
        # Preprocess
        input_tensor = self.preprocess(frame)
        
        # Inference
        if self.engine == "openvino":
            self.infer_request.infer({self.input_layer.any_name: input_tensor})
            outputs = self.infer_request.get_output_tensor(0).data
        else:
            # Ultralytics
            results = self.model.predict(
                frame,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                verbose=False,
                classes=list(self.ALLOWED_CLASSES.keys()) if self.use_class_whitelist else None
            )
            
            # Convert ultralytics results to Detection objects
            detections = []
            if len(results) > 0 and results[0].boxes is not None:
                boxes = results[0].boxes
                for i in range(len(boxes)):
                    box = boxes.xyxy[i].cpu().numpy()
                    conf = float(boxes.conf[i])
                    class_id = int(boxes.cls[i])
                    
                    # Block flicker-prone classes
                    if class_id in self.FLICKER_PRONE_CLASSES:
                        continue
                    
                    class_name = self.COCO_CLASSES.get(class_id, f"class_{class_id}")
                    
                    # Normalize bbox
                    h, w = original_shape
                    x1, y1, x2, y2 = box
                    detections.append(Detection(
                        bbox=(x1/w, y1/h, x2/w, y2/h),
                        confidence=conf,
                        class_id=class_id,
                        class_name=class_name
                    ))
            
            return detections
        
        # Postprocess (OpenVINO path)
        detections = self.postprocess(outputs, original_shape)
        
        return detections
