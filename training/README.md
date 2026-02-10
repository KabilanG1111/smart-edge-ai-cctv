# 🎯 Training Pipeline for Poor Clarity Detection

Complete workflow to train YOLOv8 to detect **fan, scissors, aeroplane, surfboard, tv, refrigerator** even in poor image quality.

## 📋 Quick Start

### 1. Prepare Dataset
```bash
# Create dataset folder
mkdir F:\CCTV\data_focused
mkdir F:\CCTV\data_focused\images
mkdir F:\CCTV\data_focused\labels

# Collect or download images (see DATA_COLLECTION_GUIDE.md)
# Label images using LabelImg or Roboflow
# Place in images/ and labels/ folders
```

### 2. Split Dataset (if needed)
```bash
cd F:\CCTV
.\.venv\Scripts\python.exe training/split_dataset.py --data-root data_focused --train-ratio 0.8
```

### 3. Verify Dataset Quality
```bash
.\.venv\Scripts\python.exe training/verify_dataset.py --data-root data_focused
```

### 4. Train Model (100 epochs minimum)
```bash
# Using yolov8m.pt for best accuracy
.\.venv\Scripts\python.exe training/train_hard_detection.py --data training/data_focused.yaml --epochs 100 --model yolov8m.pt

# Or use yolov8s.pt for faster training (less accurate)
.\.venv\Scripts\python.exe training/train_hard_detection.py --data training/data_focused.yaml --epochs 100 --model yolov8s.pt
```

Training takes:
- **yolov8s.pt**: ~2-3 hours on CPU, ~30-45 min on GPU
- **yolov8m.pt**: ~4-6 hours on CPU, ~1-1.5 hours on GPU

### 5. Test Trained Model
```bash
# Test on validation images
.\.venv\Scripts\python.exe training/test_trained_model.py --weights runs/train_robust/focused_detector/weights/best.pt --source data_focused/images/val --show --save

# Test on webcam (live)
.\.venv\Scripts\python.exe training/test_trained_model.py --weights runs/train_robust/focused_detector/weights/best.pt --source 0 --show --conf 0.3
```

### 6. Deploy to Production
Update the model path in [core/object_tracker.py](../core/object_tracker.py) line 72:
```python
model_path: str = "runs/train_robust/focused_detector/weights/best.pt"
```

Restart backend:
```bash
.\.venv\Scripts\python.exe -m uvicorn backend.main_api:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🔧 Training Configuration

The training script uses **heavy augmentation** to simulate poor image quality:

```python
hsv_h=0.02        # Color variations
hsv_s=0.7         # Saturation (washed out colors)
hsv_v=0.4         # Brightness (low light)
degrees=15        # Rotation
scale=0.5         # Object size variations
blur=0.01         # Motion/focus blur
mosaic=1.0        # Multi-object scenes
mixup=0.1         # Image blending
```

This teaches the model to detect objects in:
- ✅ Low light / darkness
- ✅ Motion blur
- ✅ Poor focus
- ✅ Color distortion
- ✅ Occlusion (partial view)
- ✅ Different angles/perspectives

---

## 📊 Expected Results

After 100 epochs with 500+ images per class:

| Metric | Poor Quality | Good Quality |
|--------|-------------|--------------|
| **mAP50** | 75-85% | 90-95% |
| **mAP50-95** | 60-75% | 80-90% |
| **Confidence** | 30-70% | 70-95% |
| **FPS (CPU)** | 25-35 | 25-35 |

Lower the confidence threshold to `0.25-0.30` for poor clarity detection.

---

## 📁 Files Reference

- **[data_focused.yaml](data_focused.yaml)** - Dataset config (6 classes)
- **[train_hard_detection.py](train_hard_detection.py)** - Training script with heavy augmentation
- **[test_trained_model.py](test_trained_model.py)** - Test/validate trained model
- **[verify_dataset.py](verify_dataset.py)** - Check dataset quality before training
- **[split_dataset.py](split_dataset.py)** - Split flat dataset into train/val
- **[DATA_COLLECTION_GUIDE.md](DATA_COLLECTION_GUIDE.md)** - How to collect & label data

---

## 🆘 Troubleshooting

### "Not enough data"
- Need 200+ images per class minimum (500+ recommended)
- Use data augmentation to multiply dataset size

### "Model not learning"
- Increase epochs to 200+
- Check label quality with `verify_dataset.py`
- Try larger model (yolov8m.pt or yolov8l.pt)

### "Poor validation accuracy"
- Collect more diverse training data
- Include edge cases (blur, occlusion, poor lighting)
- Balance class distribution (equal samples per class)

### "Slow training"
- Reduce batch size: `--batch 8`
- Use smaller model: `--model yolov8n.pt`
- Enable GPU if available

### "Out of memory"
- Reduce batch size: `--batch 4`
- Reduce image size: `--imgsz 416`

---

## 🚀 Alternative: Use Pre-trained COCO Model

If you don't have time to collect data, COCO already has 5/6 classes:
- ✅ scissors (COCO class 76)
- ✅ airplane (COCO class 4)
- ✅ surfboard (COCO class 42)
- ✅ tv (COCO class 72)
- ✅ refrigerator (COCO class 82)
- ❌ fan (NOT in COCO)

Just lower confidence threshold:
```python
# In core/object_tracker.py
conf_threshold: float = 0.30  # Already updated
```

For ceiling fans, you MUST collect custom data (not in COCO dataset).
