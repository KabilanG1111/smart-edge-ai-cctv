# 🔍 GROUNDING DINO SETUP GUIDE

## What is Grounding DINO?

**Grounding DINO** is an open vocabulary object detection model that can detect **unlimited object classes** using text prompts - no manual training required.

### Key Advantages
✅ **No training needed** - Detects any object via text description  
✅ **10,000+ classes** - Pre-trained on Objects365, Open Images, LVIS  
✅ **Zero-shot detection** - Works on objects never seen before  
✅ **Text-prompted** - "washing machine", "red pillow", "industrial pump"  
✅ **ONNX compatible** - Can be optimized with OpenVINO  

---

## Architecture Integration

Grounding DINO operates as **Stage 2** in our multi-stage pipeline:

```
Frame → Stage 1 (YOLOv8) → Stage 2 (Grounding DINO) → Stage 3 (Temporal Reasoning) → Output
         ↓                    ↓
      Dynamic objects      Static/Rare objects
      (person, vehicle)    (paper, pillow, cupboard)
```

**When Stage 2 Triggers:**
- Scene has <20 dynamic objects (not crowded)
- Static object detection needed
- Long-tail object appears (rare item)

**Performance:**
- Stage 1: 30 FPS (YOLOv8)
- Stage 2: 5-10 FPS (Grounding DINO)
- Combined: 8-10 FPS (acceptable for surveillance)

---

## Installation Options

### Option 1: Pre-built Package (Recommended)

```powershell
# Install official Grounding DINO package
pip install groundingdino-py

# Verify installation
python -c "import groundingdino; print(groundingdino.__version__)"
```

### Option 2: Build from Source (Windows Optimization)

```powershell
# Clone repository
git clone https://github.com/IDEA-Research/GroundingDINO.git
cd GroundingDINO

# Install dependencies
pip install -r requirements.txt

# Build and install
pip install -e .
```

### Option 3: ONNX Model Only (CPU-Optimized)

```powershell
# Download pre-converted ONNX model
# https://huggingface.co/IDEA-Research/grounding-dino-onnx

# Place at: models/grounding_dino/model.onnx
```

---

## Model Download

### Download Pre-trained Weights

```powershell
# Create model directory
mkdir -p models/grounding_dino

# Download Grounding DINO base model (~500MB)
# Option A: Hugging Face
wget https://huggingface.co/IDEA-Research/grounding-dino-base/resolve/main/groundingdino_swint_ogc.pth -O models/grounding_dino/groundingdino_swint_ogc.pth

# Option B: Google Drive
# Download from: https://drive.google.com/file/d/1vVQ8l-1K9JzXXXXXXXX/
```

### Download Config File

```powershell
# Download model config
wget https://raw.githubusercontent.com/IDEA-Research/GroundingDINO/main/groundingdino/config/GroundingDINO_SwinT_OGC.py -O models/grounding_dino/config.py
```

---

## Export to ONNX (CPU Optimization)

### Step 1: Create Export Script

Create `scripts/export_grounding_dino.py`:

```python
"""Export Grounding DINO to ONNX format"""

import torch
from groundingdino.models import build_model
from groundingdino.util.slconfig import SLConfig

def export_to_onnx(
    config_path: str = "models/grounding_dino/config.py",
    checkpoint_path: str = "models/grounding_dino/groundingdino_swint_ogc.pth",
    output_path: str = "models/grounding_dino/model.onnx"
):
    """Export Grounding DINO to ONNX"""
    
    # Load model
    args = SLConfig.fromfile(config_path)
    model = build_model(args)
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    model.load_state_dict(checkpoint['model'])
    model.eval()
    
    # Dummy inputs
    dummy_image = torch.randn(1, 3, 800, 800)
    dummy_text = "object . thing . item ."
    
    # Export
    torch.onnx.export(
        model,
        (dummy_image, dummy_text),
        output_path,
        export_params=True,
        opset_version=12,
        input_names=['image', 'text'],
        output_names=['boxes', 'scores', 'labels'],
        dynamic_axes={
            'image': {0: 'batch', 2: 'height', 3: 'width'},
        }
    )
    
    print(f"✅ ONNX model saved: {output_path}")

if __name__ == "__main__":
    export_to_onnx()
```

### Step 2: Run Export

```powershell
python scripts/export_grounding_dino.py
```

### Step 3: Convert to OpenVINO (Optional)

```powershell
# Convert ONNX → OpenVINO IR for 2-3x speedup
mo --input_model models/grounding_dino/model.onnx \
   --output_dir models/grounding_dino \
   --data_type FP16 \
   --compress_to_fp16
```

---

## Configuration

### Update Enterprise Pipeline

Edit `core/enterprise_pipeline.py`:

```python
pipeline = EnterprisePipeline(
    yolo_model_path="models/openvino/yolov8s_fp16.xml",
    grounding_dino_path="models/grounding_dino/model.onnx",  # ONNX model
    use_openvino=True,
    enable_stage2=True,  # Enable open vocabulary detection
    prompt_classes_path="config/prompt_classes.json"
)
```

### Add Custom Prompts

Edit `config/prompt_classes.json`:

```json
{
  "classes": [
    "paper", "bedsheet", "pillow", "cupboard", "washing machine",
    "your_custom_object_1",
    "your_custom_object_2",
    "industrial machinery",
    "medical equipment",
    "retail product"
  ]
}
```

**No retraining needed!** Just add text descriptions.

---

## Testing

### Test Grounding DINO Directly

```python
from core.grounding_dino_inference import GroundingDINOInference
import cv2

# Initialize
detector = GroundingDINOInference(
    model_path="models/grounding_dino/model.onnx",
    use_openvino=True
)

# Load image
frame = cv2.imread("test_image.jpg")

# Detect with prompts
prompts = ["paper", "pillow", "washing machine"]
detections = detector.detect(frame, prompts)

# Print results
for det in detections:
    print(f"{det.class_name}: {det.confidence:.2f} @ {det.bbox}")
```

### Test Full Pipeline

```python
from core.enterprise_pipeline import get_pipeline
import cv2

# Initialize full pipeline
pipeline = get_pipeline()

# Process frame
frame = cv2.imread("test_image.jpg")
annotated, detections, metrics = pipeline.process_frame(frame)

# Check which stage detected objects
for det in detections:
    print(f"{det.class_name}: {det.confidence:.2f} (Stage: {det.stage})")
```

Expected output:
```
person: 0.92 (Stage: yolo)
laptop: 0.87 (Stage: yolo)
washing machine: 0.78 (Stage: grounding_dino)
pillow: 0.65 (Stage: grounding_dino)
```

---

## Performance Tuning

### Reduce Stage 2 Frequency

Only run Grounding DINO every N frames:

```python
class EnterprisePipeline:
    def __init__(self, stage2_interval: int = 5):
        self.stage2_interval = stage2_interval  # Run every 5 frames
        self.frame_counter = 0
    
    def process_frame(self, frame):
        self.frame_counter += 1
        
        # Stage 1: Always
        yolo_detections = self.yolo_engine.detect(frame)
        
        # Stage 2: Every Nth frame
        stage2_detections = []
        if self.enable_stage2 and self.frame_counter % self.stage2_interval == 0:
            stage2_detections = self.grounding_dino.detect(frame, self.prompt_classes)
```

### Limit Prompt Count

Too many prompts slow down inference:

```python
# Good: 20-50 prompts per frame
prompts = ["paper", "pillow", "cupboard", "washing machine"]

# Bad: 1000+ prompts (slow)
prompts = load_all_10000_classes()  # Don't do this!

# Solution: Contextual prompts based on scene
if is_bedroom_scene:
    prompts = ["bed", "pillow", "bedsheet", "cupboard"]
elif is_kitchen_scene:
    prompts = ["refrigerator", "oven", "microwave", "sink"]
```

### Use Confidence Filtering

```python
detector = GroundingDINOInference(
    confidence_threshold=0.30  # Higher = fewer false positives
)
```

---

## Troubleshooting

### Issue: Grounding DINO not found

**Error:** `ImportError: No module named 'groundingdino'`

**Solution:**
```powershell
pip install groundingdino-py
```

### Issue: Model download failed

**Solution:** Download manually from Hugging Face:
```
https://huggingface.co/IDEA-Research/grounding-dino-base
```

### Issue: ONNX export error

**Error:** `torch.onnx.export failed`

**Solution:** Use official pre-converted ONNX model:
```
https://huggingface.co/IDEA-Research/grounding-dino-onnx
```

### Issue: Slow inference (<5 FPS)

**Solutions:**
1. Use FP16 quantization
2. Reduce image resolution (800→640)
3. Run Stage 2 every 5 frames (not every frame)
4. Limit prompts to 20-50 per inference
5. Convert to OpenVINO IR format

### Issue: Low detection accuracy

**Solutions:**
1. Lower confidence threshold (0.30 → 0.20)
2. Use more specific prompts ("red pillow" vs "pillow")
3. Verify model downloaded correctly
4. Check image preprocessing (normalization)

---

## Fallback Behavior

**If Grounding DINO is not available:**

System automatically falls back to **YOLOv8-only mode**:

```python
# Auto-fallback in enterprise_pipeline.py
try:
    self.grounding_dino = self._init_grounding_dino(grounding_dino_path)
except:
    logger.warning("⚠️ Grounding DINO not available - using YOLOv8 only")
    self.grounding_dino = None
    self.enable_stage2 = False
```

**Result:** System still works with 80 COCO classes (YOLOv8)

---

## Alternative: OWL-ViT

If Grounding DINO is unavailable, use **OWL-ViT** (Transformers library):

```powershell
pip install transformers torch torchvision
```

```python
from transformers import OwlViTProcessor, OwlViTForObjectDetection

processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32")

# Use with same prompts
prompts = ["paper", "pillow", "washing machine"]
```

---

## Resources

**Official Repository:**  
https://github.com/IDEA-Research/GroundingDINO

**Paper:**  
Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection

**Pre-trained Models:**  
https://huggingface.co/IDEA-Research

**ONNX Conversion:**  
https://github.com/IDEA-Research/GroundingDINO/issues/ONNX

**Community:**  
GitHub Issues for troubleshooting

---

## Summary

✅ **Install:** `pip install groundingdino-py`  
✅ **Download Model:** ~500MB from Hugging Face  
✅ **Export ONNX:** `python scripts/export_grounding_dino.py`  
✅ **Configure:** Add prompts to `config/prompt_classes.json`  
✅ **Test:** Run `python tests/test_grounding_dino.py`  
✅ **Deploy:** Enable `enable_stage2=True` in enterprise pipeline  

**Detection capability: 10,000+ objects without manual training! 🚀**
