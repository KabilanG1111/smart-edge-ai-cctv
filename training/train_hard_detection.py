"""
Train YOLOv8 for ROBUST detection of specific objects
Handles poor clarity, low light, blur, occlusion

Usage:
  python training/train_hard_detection.py --data training/data_focused.yaml --epochs 100
"""

import argparse
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description="Train robust YOLO detector")
    parser.add_argument("--data", required=True, help="Path to data.yaml")
    parser.add_argument("--model", default="yolov8m.pt", help="Base model (yolov8m.pt recommended)")
    parser.add_argument("--epochs", type=int, default=100, help="Training epochs (100+ recommended)")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--batch", type=int, default=16, help="Batch size (reduce if OOM)")
    parser.add_argument("--device", default="", help="CUDA device or cpu")
    parser.add_argument("--patience", type=int, default=50, help="Early stopping patience")
    return parser.parse_args()


def main():
    args = parse_args()
    
    print("=" * 60)
    print("🎯 TRAINING ROBUST OBJECT DETECTOR")
    print("=" * 60)
    print(f"Model: {args.model}")
    print(f"Epochs: {args.epochs}")
    print(f"Data: {args.data}")
    print("=" * 60)
    
    model = YOLO(args.model)
    
    # CRITICAL: Heavy augmentation for poor clarity/lighting
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device if args.device else None,
        
        # Project settings
        project="runs/train_robust",
        name="focused_detector",
        exist_ok=True,
        
        # Early stopping
        patience=args.patience,
        
        # AUGMENTATION FOR POOR QUALITY IMAGES
        hsv_h=0.02,        # Hue variation (lighting changes)
        hsv_s=0.7,         # Saturation (washed out colors)
        hsv_v=0.4,         # Brightness (low light conditions)
        degrees=15,        # Rotation (camera angle variations)
        translate=0.2,     # Translation (object position)
        scale=0.5,         # Scale (object size variation)
        shear=5.0,         # Shear (perspective distortion)
        perspective=0.001, # Perspective warp
        flipud=0.0,        # No vertical flip (objects have orientation)
        fliplr=0.5,        # Horizontal flip (50% chance)
        mosaic=1.0,        # Mosaic augmentation (multi-object scenes)
        mixup=0.1,         # Mixup (blending images)
        copy_paste=0.1,    # Copy-paste augmentation
        
        # BLUR & NOISE (simulate poor clarity)
        blur=0.01,         # Motion/focus blur
        
        # Optimizer settings for fine details
        optimizer='AdamW',
        lr0=0.001,         # Initial learning rate
        lrf=0.01,          # Final learning rate (1% of initial)
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=5.0,
        warmup_momentum=0.8,
        
        # Training stability
        box=7.5,           # Box loss weight
        cls=0.5,           # Classification loss weight
        dfl=1.5,           # Distribution focal loss weight
        
        # Save settings
        save=True,
        save_period=10,    # Save checkpoint every 10 epochs
        
        # Validation
        val=True,
        plots=True,
        
        # Performance
        workers=4,
        amp=True,          # Automatic mixed precision (faster training)
        
        # Reproducibility
        seed=42,
        deterministic=False,
        
        # Verbose
        verbose=True,
    )
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    print(f"Best weights: {results.save_dir}/weights/best.pt")
    print(f"Last weights: {results.save_dir}/weights/last.pt")
    print("=" * 60)
    print("\n📊 Validation metrics:")
    print(f"mAP50: {results.results_dict.get('metrics/mAP50(B)', 'N/A')}")
    print(f"mAP50-95: {results.results_dict.get('metrics/mAP50-95(B)', 'N/A')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
