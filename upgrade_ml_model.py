"""
🤖 ML MODEL UPGRADE SCRIPT
===========================

Automatically upgrade YOLOv8 model to higher accuracy variants
and prepare for custom training.

Usage:
    python upgrade_ml_model.py --model yolov8m  # Upgrade to medium
    python upgrade_ml_model.py --train          # Start custom training
    python upgrade_ml_model.py --export onnx    # Export optimized model

Author: Production AI Team
License: Enterprise
"""

import argparse
import sys
from pathlib import Path
from ultralytics import YOLO
import cv2
import time


def download_model(model_name: str):
    """
    Download YOLOv8 model variant
    
    Args:
        model_name: yolov8n/s/m/l/x
    """
    print(f"\n🚀 Downloading {model_name}.pt...")
    print("=" * 60)
    
    try:
        model = YOLO(f"{model_name}.pt")
        print(f"✅ {model_name}.pt downloaded successfully!")
        
        # Model info
        print(f"\n📊 Model Info:")
        print(f"   Architecture: {model_name.upper()}")
        
        if model_name == "yolov8n":
            print(f"   Size: 6MB")
            print(f"   Accuracy: 37.3% mAP")
            print(f"   Speed: 30-40 FPS (CPU)")
        elif model_name == "yolov8s":
            print(f"   Size: 11MB (CURRENT)")
            print(f"   Accuracy: 44.9% mAP")
            print(f"   Speed: 23-30 FPS (CPU)")
        elif model_name == "yolov8m":
            print(f"   Size: 26MB")
            print(f"   Accuracy: 50.2% mAP (+5% vs Small)")
            print(f"   Speed: 15-20 FPS (CPU)")
        elif model_name == "yolov8l":
            print(f"   Size: 44MB")
            print(f"   Accuracy: 52.9% mAP (+8% vs Small)")
            print(f"   Speed: 8-12 FPS (CPU), 60+ FPS (GPU)")
        elif model_name == "yolov8x":
            print(f"   Size: 68MB")
            print(f"   Accuracy: 53.9% mAP (+9% vs Small)")
            print(f"   Speed: 5-8 FPS (CPU), 40+ FPS (GPU)")
        
        print(f"\n✅ Ready to use!")
        print(f"\n📝 To activate, update backend/main_api.py:")
        print(f'   model_path="yolov8s.pt" → model_path="{model_name}.pt"')
        
        return True
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False


def export_model(model_path: str, format: str = "onnx"):
    """
    Export model to optimized format
    
    Args:
        model_path: Path to .pt model
        format: onnx, openvino, tensorrt, etc.
    """
    print(f"\n🔄 Exporting {model_path} to {format.upper()}...")
    print("=" * 60)
    
    try:
        model = YOLO(model_path)
        
        # Export parameters
        export_args = {
            "format": format,
            "simplify": True if format == "onnx" else False,
            "half": True if format == "openvino" else False,
        }
        
        print(f"⏳ Exporting (this may take 1-2 minutes)...")
        model.export(**export_args)
        
        print(f"\n✅ Export complete!")
        
        if format == "onnx":
            print(f"   📄 File: {model_path.replace('.pt', '.onnx')}")
            print(f"   🚀 Speedup: 1.2-1.5x (CPU)")
            print(f"   ✅ Compatible: All platforms")
        elif format == "openvino":
            print(f"   📁 Folder: {model_path.replace('.pt', '_openvino_model')}")
            print(f"   🚀 Speedup: 2-3x (Intel CPU)")
            print(f"   ✅ Compatible: Intel hardware")
        elif format == "engine":
            print(f"   📄 File: {model_path.replace('.pt', '.engine')}")
            print(f"   🚀 Speedup: 5-10x (NVIDIA GPU)")
            print(f"   ✅ Compatible: NVIDIA GPUs only")
        
        return True
    except Exception as e:
        print(f"❌ Error exporting: {e}")
        return False


def benchmark_model(model_path: str, n_frames: int = 100):
    """
    Benchmark model speed and accuracy
    
    Args:
        model_path: Path to model
        n_frames: Number of frames to test
    """
    print(f"\n⏱️  Benchmarking {model_path}...")
    print("=" * 60)
    
    try:
        model = YOLO(model_path)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("⚠️  Camera not available, using dummy image")
            # Create dummy image
            frame = cv2.imread("test_frame.jpg")
            if frame is None:
                frame = (np.random.rand(640, 640, 3) * 255).astype(np.uint8)
        
        times = []
        detection_counts = []
        
        print(f"\n🎬 Running {n_frames} inference passes...")
        
        for i in range(n_frames):
            if cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
            
            start = time.time()
            results = model(frame, conf=0.25, verbose=False)
            elapsed = time.time() - start
            
            times.append(elapsed)
            detection_counts.append(len(results[0].boxes))
            
            if (i + 1) % 20 == 0:
                avg_fps = 1 / (sum(times[-20:]) / 20)
                print(f"   Frame {i+1}/{n_frames}: {avg_fps:.1f} FPS")
        
        cap.release()
        
        # Results
        avg_time = sum(times) / len(times)
        avg_fps = 1 / avg_time
        avg_detections = sum(detection_counts) / len(detection_counts)
        
        print(f"\n📊 Benchmark Results:")
        print(f"   Average FPS: {avg_fps:.2f}")
        print(f"   Average latency: {avg_time*1000:.1f}ms")
        print(f"   Avg detections/frame: {avg_detections:.1f}")
        print(f"   Min FPS: {1/max(times):.2f}")
        print(f"   Max FPS: {1/min(times):.2f}")
        
        # Recommendations
        if avg_fps >= 30:
            print(f"\n✅ Performance: EXCELLENT (30+ FPS)")
            print(f"   Consider upgrading to larger model for better accuracy")
        elif avg_fps >= 20:
            print(f"\n✅ Performance: GOOD (20-30 FPS)")
            print(f"   Suitable for real-time monitoring")
        elif avg_fps >= 10:
            print(f"\n⚠️  Performance: ACCEPTABLE (10-20 FPS)")
            print(f"   Consider model quantization or smaller variant")
        else:
            print(f"\n❌ Performance: SLOW (<10 FPS)")
            print(f"   Downgrade to smaller model or use GPU")
        
        return avg_fps
    except Exception as e:
        print(f"❌ Benchmark error: {e}")
        return 0


def prepare_training():
    """Create directory structure for custom training"""
    print("\n📁 Preparing Custom Training Environment...")
    print("=" * 60)
    
    base_dir = Path("F:/CCTV/training")
    
    # Create directories
    dirs = [
        base_dir / "data" / "images" / "train",
        base_dir / "data" / "images" / "val",
        base_dir / "data" / "labels" / "train",
        base_dir / "data" / "labels" / "val",
        base_dir / "runs",
        base_dir / "models",
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {dir_path}")
    
    # Create dataset.yaml
    yaml_content = """# Custom CCTV Dataset Configuration
# BILLION-DOLLAR ML TRAINING

path: F:/CCTV/training/data
train: images/train
val: images/val

# Number of classes (edit based on your needs)
nc: 10

# Class names (edit based on your objects)
names:
  0: person
  1: laptop
  2: cell phone
  3: book
  4: cup
  5: bottle
  6: chair
  7: table
  8: backpack
  9: handbag

# Training hyperparameters (optimized for CCTV)
# Augmentation settings
hsv_h: 0.015  # Hue
hsv_s: 0.7    # Saturation
hsv_v: 0.4    # Brightness
degrees: 5.0  # Rotation
translate: 0.1
scale: 0.3
flipud: 0.0   # No vertical flip (cameras don't flip)
fliplr: 0.5   # Horizontal flip OK
mosaic: 1.0
mixup: 0.1
"""
    
    yaml_path = base_dir / "data" / "dataset.yaml"
    yaml_path.write_text(yaml_content)
    print(f"\n   ✅ Created: {yaml_path}")
    
    # Create training script
    train_script = """# train_custom_model.py
from ultralytics import YOLO

# Load pre-trained model
model = YOLO('yolov8s.pt')

# Train
results = model.train(
    data='F:/CCTV/training/data/dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device='cpu',  # Change to 'cuda' if GPU available
    patience=20,
    save_period=10,
    project='F:/CCTV/training/runs',
    name='custom_cctv_detector',
    exist_ok=True,
    
    # Hyperparameters (optimized)
    lr0=0.01,
    lrf=0.01,
    momentum=0.937,
    weight_decay=0.0005,
    warmup_epochs=3.0,
    box=7.5,
    cls=0.5,
    dfl=1.5,
)

print("\\n✅ Training complete!")
print(f"Best model: {results.save_dir}/weights/best.pt")
"""
    
    script_path = base_dir / "train_custom_model.py"
    script_path.write_text(train_script)
    print(f"   ✅ Created: {script_path}")
    
    print(f"\n📝 Next Steps:")
    print(f"   1. Collect images:")
    print(f"      - Record CCTV footage")
    print(f"      - Extract frames: python extract_frames.py")
    print(f"      - Or use: training/data/images/train/")
    print(f"   ")
    print(f"   2. Label images:")
    print(f"      - Use CVAT: https://www.cvat.ai")
    print(f"      - Or Label Studio: https://labelstud.io")
    print(f"      - Export in YOLO format")
    print(f"   ")
    print(f"   3. Start training:")
    print(f"      cd training")
    print(f"      python train_custom_model.py")
    print(f"   ")
    print(f"   4. Deploy custom model:")
    print(f"      Update backend/main_api.py:")
    print(f"      model_path='training/runs/custom_cctv_detector/weights/best.pt'")


def main():
    parser = argparse.ArgumentParser(description="ML Model Upgrade Tool")
    
    parser.add_argument(
        "--model",
        type=str,
        choices=["yolov8n", "yolov8s", "yolov8m", "yolov8l", "yolov8x"],
        help="Download specific YOLOv8 variant"
    )
    
    parser.add_argument(
        "--export",
        type=str,
        choices=["onnx", "openvino", "engine", "tensorrt"],
        help="Export current model to optimized format"
    )
    
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Benchmark current model performance"
    )
    
    parser.add_argument(
        "--train",
        action="store_true",
        help="Prepare environment for custom training"
    )
    
    parser.add_argument(
        "--model-path",
        type=str,
        default="yolov8s.pt",
        help="Path to model file (for export/benchmark)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("🚀 ML MODEL UPGRADE TOOL")
    print("=" * 60)
    
    if args.model:
        download_model(args.model)
    
    elif args.export:
        export_model(args.model_path, args.export)
    
    elif args.benchmark:
        benchmark_model(args.model_path)
    
    elif args.train:
        prepare_training()
    
    else:
        print("\n📚 Usage:")
        print("   Download better model:")
        print("      python upgrade_ml_model.py --model yolov8m")
        print("   ")
        print("   Export to ONNX:")
        print("      python upgrade_ml_model.py --export onnx")
        print("   ")
        print("   Benchmark speed:")
        print("      python upgrade_ml_model.py --benchmark")
        print("   ")
        print("   Prepare custom training:")
        print("      python upgrade_ml_model.py --train")
        print("\n💡 For billion-dollar accuracy, see: BILLION_DOLLAR_ML_GUIDE.md")


if __name__ == "__main__":
    main()
