"""
Split a flat YOLO dataset into train/val folders.

Expected input layout:
  data_root/
    images/  (all images)
    labels/  (one .txt per image)

Output layout:
  data_root/
    images/train, images/val
    labels/train, labels/val
"""

import argparse
import os
import random
import shutil
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Split YOLO dataset into train/val")
    parser.add_argument("--data-root", required=True, help="Dataset root containing images/ and labels/")
    parser.add_argument("--train-ratio", type=float, default=0.8, help="Train split ratio (default: 0.8)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--copy", action="store_true", help="Copy files instead of moving")
    return parser.parse_args()


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTS


def main() -> None:
    args = parse_args()
    data_root = Path(args.data_root)
    images_dir = data_root / "images"
    labels_dir = data_root / "labels"

    if not images_dir.exists() or not labels_dir.exists():
        raise FileNotFoundError("Expected images/ and labels/ under data root")

    train_images_dir = images_dir / "train"
    val_images_dir = images_dir / "val"
    train_labels_dir = labels_dir / "train"
    val_labels_dir = labels_dir / "val"

    train_images_dir.mkdir(parents=True, exist_ok=True)
    val_images_dir.mkdir(parents=True, exist_ok=True)
    train_labels_dir.mkdir(parents=True, exist_ok=True)
    val_labels_dir.mkdir(parents=True, exist_ok=True)

    # Collect images that have matching label files
    images = [p for p in images_dir.iterdir() if p.is_file() and is_image(p)]
    pairs = []
    for img in images:
        label = labels_dir / (img.stem + ".txt")
        if label.exists():
            pairs.append((img, label))

    if not pairs:
        raise RuntimeError("No image/label pairs found in images/ and labels/")

    random.seed(args.seed)
    random.shuffle(pairs)

    split_index = int(len(pairs) * args.train_ratio)
    train_pairs = pairs[:split_index]
    val_pairs = pairs[split_index:]

    mover = shutil.copy2 if args.copy else shutil.move

    for img, label in train_pairs:
        mover(str(img), str(train_images_dir / img.name))
        mover(str(label), str(train_labels_dir / label.name))

    for img, label in val_pairs:
        mover(str(img), str(val_images_dir / img.name))
        mover(str(label), str(val_labels_dir / label.name))

    print(f"Split complete: {len(train_pairs)} train, {len(val_pairs)} val")


if __name__ == "__main__":
    main()
