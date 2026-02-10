"""
Train YOLOv8 on a custom dataset.

Usage example:
  python training/train_yolo.py --data training/data.yaml --model yolov8s.pt --epochs 50
"""

import argparse
from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train YOLOv8 on custom data")
    parser.add_argument("--data", required=True, help="Path to YOLO data.yaml")
    parser.add_argument("--model", default="yolov8s.pt", help="Base model weights")
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--workers", type=int, default=4, help="Dataloader workers")
    parser.add_argument("--project", default="runs/train", help="Output project dir")
    parser.add_argument("--name", default="cctv-custom", help="Run name")
    parser.add_argument("--device", default="", help="CUDA device id, or empty for auto")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = YOLO(args.model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        workers=args.workers,
        project=args.project,
        name=args.name,
        device=args.device if args.device != "" else None,
    )


if __name__ == "__main__":
    main()
