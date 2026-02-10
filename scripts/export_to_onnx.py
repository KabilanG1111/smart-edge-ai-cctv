"""
Export YOLOv8 to ONNX format for OpenVINO deployment

Usage:
    python scripts/export_to_onnx.py --model yolov8n.pt --imgsz 320
    
Then convert to OpenVINO IR:
    mo --input_model yolov8n.onnx --output_dir models/openvino --data_type FP16
"""

import argparse
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Export Y OLOv8 to ONNX")
    parser.add_argument("--model", default="yolov8n.pt", help="YOLOv8 model path")
    parser.add_argument("--imgsz", type=int, default=320, help="Input image size (320, 416, 640)")
    parser.add_argument("--output", default=None, help="Output ONNX path (default: same as model)")
    parser.add_argument("--opset", type=int, default=17, help="ONNX opset version")
    parser.add_argument("--dynamic", action="store_true", help="Enable dynamic batch size")
    parser.add_argument("--simplify", action="store_true", help="Simplify ONNX model (requires onnx-simplifier)")
    return parser.parse_args()


def export_to_onnx(
    model_path: str,
    imgsz: int = 320,
    output_path: str = None,
    opset: int = 17,
    dynamic: bool = False,
    simplify: bool = False
):
    """
    Export YOLOv8 model to ONNX format
    
    Args:
        model_path: Path to YOLOv8 .pt file
        imgsz: Input image size
        output_path: Output ONNX path
        opset: ONNX opset version
        dynamic: Enable dynamic batch size
        simplify: Simplify ONNX graph
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        raise RuntimeError("ultralytics not installed. Run: pip install ultralytics")
    
    logger.info("=" * 60)
    logger.info("📦 YOLOv8 → ONNX Export")
    logger.info("=" * 60)
    logger.info(f"Model: {model_path}")
    logger.info(f"Input size: {imgsz}x{imgsz}")
    logger.info(f"ONNX opset: {opset}")
    logger.info(f"Dynamic batch: {dynamic}")
    logger.info("=" * 60)
    
    # Load model
    model = YOLO(model_path)
    
    # Determine output path
    if output_path is None:
        model_stem = Path(model_path).stem
        output_path = f"{model_stem}.onnx"
    
    # Export to ONNX
    logger.info("🔄 Exporting to ONNX...")
    success = model.export(
        format="onnx",
        imgsz=imgsz,
        opset=opset,
        dynamic=dynamic,
        simplify=simplify
    )
    
    if success:
        logger.info("✅ Export successful!")
        logger.info(f"📁 ONNX file: {output_path}")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Install OpenVINO: pip install openvino openvino-dev")
        logger.info("2. Convert to OpenVINO IR:")
        logger.info(f"   mo --input_model {output_path} \\")
        logger.info("      --output_dir models/openvino \\")
        logger.info("      --data_type FP16")
        logger.info("")
        logger.info("3. Use in production:")
        logger.info("   from core.openvino_inference import OpenVINOInference")
        logger.info("   model = OpenVINOInference('models/openvino/yolov8n.xml')")
    else:
        logger.error("❌ Export failed")
        return False
    
    return True


def main():
    args = parse_args()
    
    success = export_to_onnx(
        model_path=args.model,
        imgsz=args.imgsz,
        output_path=args.output,
        opset=args.opset,
        dynamic=args.dynamic,
        simplify=args.simplify
    )
    
    if not success:
        exit(1)


if __name__ == "__main__":
    main()
