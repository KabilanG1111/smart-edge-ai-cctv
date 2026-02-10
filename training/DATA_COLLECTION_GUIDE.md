# 📸 Data Collection Guide for Focused Object Detection

To train a model that detects **fan, scissors, aeroplane, surfboard, tv, refrigerator** even in poor clarity, you need labeled training data.

## 🎯 Target: 500+ images per class minimum (1000+ recommended)

### Required Dataset Structure
```
F:\CCTV\data_focused\
├── images\
│   ├── train\      (80% of data)
│   └── val\        (20% of data)
└── labels\
    ├── train\      (YOLO .txt labels)
    └── val\        (YOLO .txt labels)
```

### Label Format (YOLO)
Each image needs a `.txt` file with same name:
```
<class_id> <x_center> <y_center> <width> <height>
```
All values normalized 0-1. Example `fan_001.txt`:
```
0 0.5 0.5 0.3 0.4
```
Class IDs (from data_focused.yaml):
- 0 = fan
- 1 = scissors
- 2 = aeroplane
- 3 = surfboard
- 4 = tv
- 5 = refrigerator

---

## 📦 Option 1: Use Existing COCO Dataset (Quick Start)

YOLOv8 pretrained models already know some of these classes from COCO:
- ✅ scissors (class 76)
- ✅ airplane (class 4)
- ✅ surfboard (class 42)
- ✅ tv (class 72)
- ✅ refrigerator (class 82)
- ❌ fan (NOT in COCO - needs custom data)

**Extract COCO subset:**
```bash
# Download COCO 2017 validation set
wget http://images.cocodataset.org/zips/val2017.zip
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip

# Use this script to extract + convert to YOLO format
python training/extract_coco_classes.py
```

---

## 📦 Option 2: Collect & Label Custom Data (Best Quality)

### A. Collect Images
1. **Variety is key:**
   - Different angles (front, side, top, tilted)
   - Different lighting (bright, dim, backlit)
   - Different distances (close-up, far away)
   - Different backgrounds (cluttered, clean)
   - Different conditions (blur, occlusion, partial view)

2. **For ceiling fans specifically:**
   - Fan OFF (blades visible)
   - Fan ON (motion blur)
   - Different blade counts (3, 4, 5 blades)
   - With/without lights attached

3. **Image quality:**
   - Mix of high + low quality (since you want poor clarity detection)
   - Various resolutions
   - Camera shake, blur, noise

### B. Label Images (Use LabelImg or Roboflow)

**Option A: LabelImg (Free, Local)**
```bash
pip install labelImg
labelImg
```
- Draw boxes around objects
- Select correct class
- Saves YOLO format automatically

**Option B: Roboflow (Free tier, Web-based)**
1. Create project at roboflow.com
2. Upload images
3. Draw bounding boxes
4. Export as "YOLOv8" format
5. Download zip with train/val split

**Option C: Label Studio (Free, Self-hosted)**
```bash
pip install label-studio
label-studio start
```

---

## 📦 Option 3: Use Roboflow Universe (Pre-labeled Datasets)

Search for existing datasets:
- https://universe.roboflow.com/search?q=fan
- https://universe.roboflow.com/search?q=scissors
- https://universe.roboflow.com/search?q=airplane
- https://universe.roboflow.com/search?q=surfboard
- https://universe.roboflow.com/search?q=tv
- https://universe.roboflow.com/search?q=refrigerator

Download in YOLOv8 format, merge into one dataset.

---

## 🚀 After Data Collection

### 1. Verify Dataset Structure
```bash
# Check you have matching images + labels
python training/verify_dataset.py --data-root F:\CCTV\data_focused
```

### 2. Split if Needed
```bash
# If images/labels are flat (not in train/val yet)
python training/split_dataset.py --data-root F:\CCTV\data_focused --train-ratio 0.8
```

### 3. Train with Heavy Augmentation
```bash
python training/train_hard_detection.py --data training/data_focused.yaml --epochs 100 --model yolov8m.pt
```

### 4. Test the Model
```bash
# On validation set
python training/test_trained_model.py --weights runs/train_robust/focused_detector/weights/best.pt --source data_focused/images/val --show

# On webcam (live test)
python training/test_trained_model.py --weights runs/train_robust/focused_detector/weights/best.pt --source 0 --show
```

### 5. Deploy to Production
Update production pipeline to use trained weights:
```python
# In core/object_tracker.py, line 73
model_path: str = "runs/train_robust/focused_detector/weights/best.pt"
```

---

## 📊 Expected Performance

With 500+ images per class + heavy augmentation:
- **mAP50**: 85-95% (detection accuracy at 50% IoU)
- **mAP50-95**: 70-85% (detection accuracy at strict IoU)
- **Inference**: 15-25ms per image on CPU (30-60 FPS)

With poor clarity:
- Model will detect objects in blur/low light
- Confidence may be lower (50-70% instead of 90%+)
- Use `conf=0.3` threshold instead of default 0.5

---

## ⚡ Quick Start (No Custom Data)

If you don't have time to collect data, start with COCO pre-trained:

```bash
# Just lower the confidence threshold + add post-processing
python training/train_hard_detection.py --data training/data_focused.yaml --epochs 50 --model yolov8s.pt
```

This'll fine-tune the existing model on whatever COCO images exist for these classes.

---

## 🆘 Need Help?

1. **No ceiling fan data?** Search "ceiling fan dataset" on Google Dataset Search
2. **Labeling too slow?** Use SAM (Segment Anything Model) for auto-annotation
3. **Model not learning?** Increase epochs to 200+, check label quality
4. **Still poor accuracy?** Collect more diverse training data (especially edge cases)
