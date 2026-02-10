"""
Verify YOLO dataset structure and label quality
Reports missing labels, invalid annotations, class distribution

Usage:
  python training/verify_dataset.py --data-root F:\CCTV\data_focused
"""

import argparse
from pathlib import Path
from collections import defaultdict


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def parse_args():
    parser = argparse.ArgumentParser(description="Verify YOLO dataset")
    parser.add_argument("--data-root", required=True, help="Dataset root path")
    return parser.parse_args()


def is_image(path):
    return path.suffix.lower() in IMAGE_EXTS


def verify_split(split_name, images_dir, labels_dir):
    """Verify train or val split"""
    print(f"\n{'=' * 60}")
    print(f"📂 Checking {split_name.upper()} split")
    print('=' * 60)
    
    if not images_dir.exists():
        print(f"❌ Missing: {images_dir}")
        return
    
    if not labels_dir.exists():
        print(f"❌ Missing: {labels_dir}")
        return
    
    images = [p for p in images_dir.iterdir() if p.is_file() and is_image(p)]
    labels = list(labels_dir.glob("*.txt"))
    
    print(f"Images: {len(images)}")
    print(f"Labels: {len(labels)}")
    
    # Check missing labels
    missing_labels = []
    for img in images:
        label_path = labels_dir / (img.stem + ".txt")
        if not label_path.exists():
            missing_labels.append(img.name)
    
    if missing_labels:
        print(f"\n⚠️  {len(missing_labels)} images missing labels:")
        for name in missing_labels[:5]:
            print(f"   - {name}")
        if len(missing_labels) > 5:
            print(f"   ... and {len(missing_labels) - 5} more")
    
    # Check extra labels
    extra_labels = []
    for label in labels:
        img_path = None
        for ext in IMAGE_EXTS:
            candidate = images_dir / (label.stem + ext)
            if candidate.exists():
                img_path = candidate
                break
        if img_path is None:
            extra_labels.append(label.name)
    
    if extra_labels:
        print(f"\n⚠️  {len(extra_labels)} labels without images:")
        for name in extra_labels[:5]:
            print(f"   - {name}")
        if len(extra_labels) > 5:
            print(f"   ... and {len(extra_labels) - 5} more")
    
    # Analyze label content
    class_counts = defaultdict(int)
    total_boxes = 0
    empty_labels = []
    invalid_labels = []
    
    for label in labels:
        try:
            lines = label.read_text().strip().split('\n')
            if not lines or lines == ['']:
                empty_labels.append(label.name)
                continue
            
            for line in lines:
                parts = line.strip().split()
                if len(parts) != 5:
                    invalid_labels.append((label.name, line))
                    continue
                
                cls_id = int(parts[0])
                x, y, w, h = map(float, parts[1:5])
                
                # Check normalized coordinates
                if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                    invalid_labels.append((label.name, f"invalid coords: {line}"))
                    continue
                
                class_counts[cls_id] += 1
                total_boxes += 1
        
        except Exception as e:
            invalid_labels.append((label.name, str(e)))
    
    if empty_labels:
        print(f"\n⚠️  {len(empty_labels)} empty label files")
    
    if invalid_labels:
        print(f"\n❌ {len(invalid_labels)} invalid annotations:")
        for name, reason in invalid_labels[:5]:
            print(f"   - {name}: {reason}")
        if len(invalid_labels) > 5:
            print(f"   ... and {len(invalid_labels) - 5} more")
    
    # Class distribution
    if class_counts:
        print(f"\n📊 Class distribution ({total_boxes} total boxes):")
        for cls_id in sorted(class_counts.keys()):
            count = class_counts[cls_id]
            pct = count / total_boxes * 100
            print(f"   Class {cls_id}: {count:4d} ({pct:5.1f}%)")
    
    # Summary
    valid_pairs = len(images) - len(missing_labels)
    print(f"\n✅ Valid image/label pairs: {valid_pairs}")
    
    if valid_pairs < 50:
        print("⚠️  WARNING: Less than 50 samples - need more data!")
    elif valid_pairs < 200:
        print("⚠️  Low sample count - 200+ recommended per split")
    else:
        print(f"✅ Good sample count for {split_name}")


def main():
    args = parse_args()
    data_root = Path(args.data_root)
    
    print("=" * 60)
    print("🔍 YOLO DATASET VERIFICATION")
    print("=" * 60)
    print(f"Dataset: {data_root}")
    
    if not data_root.exists():
        print(f"❌ Dataset root not found: {data_root}")
        return
    
    images_dir = data_root / "images"
    labels_dir = data_root / "labels"
    
    # Check train split
    train_images = images_dir / "train"
    train_labels = labels_dir / "train"
    verify_split("train", train_images, train_labels)
    
    # Check val split
    val_images = images_dir / "val"
    val_labels = labels_dir / "val"
    verify_split("val", val_images, val_labels)
    
    print("\n" + "=" * 60)
    print("✅ VERIFICATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
