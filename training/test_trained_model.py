"""
Test trained model on validation set or live camera
Show predictions with confidence scores

Usage:
  # Test on validation dataset
  python training/test_trained_model.py --weights runs/train_robust/focused_detector/weights/best.pt --source data_focused/images/val
  
  # Test on webcam
  python training/test_trained_model.py --weights runs/train_robust/focused_detector/weights/best.pt --source 0
  
  # Test on video file
  python training/test_trained_model.py --weights runs/train_robust/focused_detector/weights/best.pt --source video.mp4
"""

import argparse
from ultralytics import YOLO
import cv2
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Test trained YOLO model")
    parser.add_argument("--weights", required=True, help="Path to trained weights (best.pt)")
    parser.add_argument("--source", required=True, help="Test source (image folder, video, or 0 for webcam)")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--show", action="store_true", help="Display predictions")
    parser.add_argument("--save", action="store_true", help="Save predictions")
    return parser.parse_args()


def main():
    args = parse_args()
    
    print("=" * 60)
    print("🧪 TESTING TRAINED MODEL")
    print("=" * 60)
    print(f"Weights: {args.weights}")
    print(f"Source: {args.source}")
    print(f"Confidence: {args.conf}")
    print("=" * 60)
    
    # Load trained model
    model = YOLO(args.weights)
    
    # Run prediction
    results = model.predict(
        source=args.source,
        conf=args.conf,
        imgsz=args.imgsz,
        save=args.save,
        show=args.show,
        stream=True,
        verbose=True,
    )
    
    # Process results
    total_detections = 0
    class_counts = {}
    
    for i, result in enumerate(results):
        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            total_detections += len(boxes)
            
            for box in boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                conf = float(box.conf[0])
                
                if cls_name not in class_counts:
                    class_counts[cls_name] = 0
                class_counts[cls_name] += 1
                
                print(f"Frame {i+1}: {cls_name} ({conf:.2f})")
        
        # Show frame if webcam/video
        if args.show and hasattr(result, 'plot'):
            frame = result.plot()
            cv2.imshow("Predictions", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cv2.destroyAllWindows()
    
    print("\n" + "=" * 60)
    print("📊 DETECTION SUMMARY")
    print("=" * 60)
    print(f"Total detections: {total_detections}")
    print("\nDetections by class:")
    for cls_name, count in sorted(class_counts.items()):
        print(f"  {cls_name}: {count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
