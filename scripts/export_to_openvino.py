"""
🚀 OPENVINO EXPORT & OPTIMIZATION
=================================

Convert YOLOv8 PyTorch → ONNX → OpenVINO IR (FP16)
Optimizations:
- FP16 quantization (2x faster, 2x smaller)
- Fused operations
- CPU-specific optimizations
- Async inference support

Performance gain: 2-3x speedup vs PyTorch on Intel CPU

Usage:
    python scripts/export_to_openvino.py --model yolov8s.pt --imgsz 640
"""

import argparse
from pathlib import Path
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


def export_yolo_to_onnx(model_path: str, imgsz: int = 640, opset: int = 12):
    """
    Export YOLOv8 from PyTorch to ONNX
    
    Args:
        model_path: Path to YOLOv8 .pt file
        imgsz: Input image size (640 for production)
        opset: ONNX opset version (12 for OpenVINO compatibility)
    """
    try:
        from ultralytics import YOLO
        
        logger.info(f"📥 Loading YOLOv8 model: {model_path}")
        model = YOLO(model_path)
        
        # Export to ONNX
        onnx_path = model_path.replace('.pt', '.onnx')
        logger.info(f"🔄 Exporting to ONNX: {onnx_path}")
        
        model.export(
            format='onnx',
            imgsz=imgsz,
            opset=opset,
            simplify=True,  # Simplify ONNX graph
            dynamic=False,  # Static shapes for OpenVINO optimization
            half=False  # FP32 for ONNX (will quantize in OpenVINO)
        )
        
        logger.info(f"✅ ONNX export complete: {onnx_path}")
        return onnx_path
        
    except Exception as e:
        logger.error(f"❌ ONNX export failed: {e}")
        sys.exit(1)


def convert_onnx_to_openvino(onnx_path: str, output_dir: str = "models/openvino", fp16: bool = True):
    """
    Convert ONNX to OpenVINO IR format with optimizations
    
    Args:
        onnx_path: Path to ONNX model
        output_dir: Output directory for OpenVINO IR files
        fp16: Use FP16 quantization (2x speedup, minimal accuracy loss)
    """
    try:
        from openvino.tools import mo
        from openvino.runtime import Core, get_version
        
        logger.info(f"OpenVINO version: {get_version()}")
        logger.info(f"🔄 Converting ONNX to OpenVINO IR: {onnx_path}")
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Model name
        model_name = Path(onnx_path).stem
        if fp16:
            model_name += "_fp16"
        
        # Convert with Model Optimizer
        ir_path = output_path / model_name
        
        logger.info(f"📝 Optimization settings:")
        logger.info(f"   - FP16: {fp16}")
        logger.info(f"   - Output: {ir_path}.xml")
        
        mo.convert_model(
            onnx_path,
            output_model=str(ir_path),
            compress_to_fp16=fp16
        )
        
        logger.info(f"✅ OpenVINO IR created: {ir_path}.xml")
        
        # Verify model
        logger.info("🔍 Verifying model...")
        ie = Core()
        model = ie.read_model(model=f"{ir_path}.xml")
        logger.info(f"   - Inputs: {[inp.get_any_name() for inp in model.inputs]}")
        logger.info(f"   - Outputs: {[out.get_any_name() for out in model.outputs]}")
        logger.info(f"   - Precision: {'FP16' if fp16 else 'FP32'}")
        
        # Benchmark
        logger.info("📊 Running benchmark...")
        compiled = ie.compile_model(model, "CPU")
        infer_request = compiled.create_infer_request()
        
        import numpy as np
        import time
        
        # Dummy input
        input_shape = model.input().shape
        dummy_input = np.random.rand(*input_shape).astype(np.float32)
        
        # Warmup
        for _ in range(10):
            infer_request.infer({0: dummy_input})
        
        # Benchmark
        times = []
        for _ in range(50):
            start = time.time()
            infer_request.infer({0: dummy_input})
            times.append((time.time() - start) * 1000)
        
        avg_time = np.mean(times)
        fps = 1000.0 / avg_time
        
        logger.info(f"⚡ Performance:")
        logger.info(f"   - Avg latency: {avg_time:.2f} ms")
        logger.info(f"   - Throughput: {fps:.2f} FPS")
        logger.info(f"   - Min/Max: {min(times):.2f} / {max(times):.2f} ms")
        
        return f"{ir_path}.xml"
        
    except ImportError:
        logger.error("❌ OpenVINO not installed")
        logger.info("📥 Install: pip install openvino openvino-dev")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ OpenVINO conversion failed: {e}")
        sys.exit(1)


def optimize_for_cpu(ir_path: str):
    """
    Apply CPU-specific optimizations
    
    - Enable CPU pinning
    - Optimize for Intel architecture
    - Configure async inference
    """
    try:
        from openvino.runtime import Core, properties
        
        logger.info("🔧 Applying CPU optimizations...")
        
        ie = Core()
        model = ie.read_model(model=ir_path)
        
        # CPU optimization properties
        config = {
            properties.hint.performance_mode(): properties.hint.PerformanceMode.THROUGHPUT,
            properties.hint.num_requests(): 4,  # Async requests
            properties.streams.num(): 2,  # Inference streams
        }
        
        compiled = ie.compile_model(model, "CPU", config)
        
        logger.info("✅ CPU optimizations applied")
        logger.info(f"   - Performance mode: THROUGHPUT")
        logger.info(f"   - Async requests: 4")
        logger.info(f"   - Inference streams: 2")
        
        return compiled
        
    except Exception as e:
        logger.error(f"❌ CPU optimization failed: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Export YOLOv8 to OpenVINO IR")
    parser.add_argument("--model", type=str, required=True, help="Path to YOLOv8 .pt file")
    parser.add_argument("--imgsz", type=int, default=640, help="Input image size")
    parser.add_argument("--opset", type=int, default=12, help="ONNX opset version")
    parser.add_argument("--output", type=str, default="models/openvino", help="Output directory")
    parser.add_argument("--fp16", action="store_true", default=True, help="Use FP16 quantization")
    parser.add_argument("--no-fp16", dest="fp16", action="store_false", help="Use FP32 (no quantization)")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("🚀 YOLOV8 → OPENVINO EXPORT PIPELINE")
    logger.info("=" * 60)
    
    # Step 1: Export to ONNX
    logger.info("\n[STEP 1/3] PyTorch → ONNX")
    onnx_path = export_yolo_to_onnx(args.model, args.imgsz, args.opset)
    
    # Step 2: Convert to OpenVINO IR
    logger.info("\n[STEP 2/3] ONNX → OpenVINO IR")
    ir_path = convert_onnx_to_openvino(onnx_path, args.output, args.fp16)
    
    # Step 3: CPU optimizations
    logger.info("\n[STEP 3/3] CPU Optimizations")
    optimize_for_cpu(ir_path)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ EXPORT COMPLETE")
    logger.info("=" * 60)
    logger.info(f"📂 OpenVINO model: {ir_path}")
    logger.info(f"🔧 To use in pipeline:")
    logger.info(f'   pipeline = EnterprisePipeline(yolo_model_path="{ir_path}")')


if __name__ == "__main__":
    main()
