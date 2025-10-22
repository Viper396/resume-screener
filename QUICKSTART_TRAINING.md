# Quick Start: Train Your ATS Model

**For RTX 4060 GPU users** - Get started in 10 minutes!

## Prerequisites
- Windows with RTX 4060 GPU
- Python 3.8+ installed
- Kaggle account

## Step-by-Step Instructions

### 1. Install CUDA (One-time setup)
Download and install: https://developer.nvidia.com/cuda-downloads
- Choose: **CUDA 12.1** (recommended for RTX 4060)
- Restart after installation

### 2. Setup Backend
```bash
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install PyTorch with CUDA first
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install other dependencies
pip install -r requirements.txt

# Verify GPU is working
python -c "import torch; print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not found')"
```

Expected output: `GPU: NVIDIA GeForce RTX 4060 Laptop GPU`

### 3. Get Kaggle API Token
1. Go to: https://www.kaggle.com/settings/account
2. Scroll to "API" → Click "Create New API Token"
3. Save the downloaded `kaggle.json` to: `C:\Users\Arnav\.kaggle\kaggle.json`

### 4. Download Dataset
```bash
# Download resume dataset (~50MB)
kaggle datasets download -d snehaanbhawal/resume-dataset

# Extract
powershell -command "Expand-Archive resume-dataset.zip -DestinationPath data"
```

### 5. Prepare Training Data
```bash
python prepare_dataset.py --input data/Resume.csv --output training_data.json
```

This will:
- Score each resume using ML
- Create `training_data.json` (takes ~5 minutes)

### 6. Train the Model
```bash
python train_model.py --data training_data.json --n-estimators 200 --use-gpu
```

**Training time**: ~5-7 minutes with RTX 4060

Expected output:
```
✓ GPU Available: NVIDIA GeForce RTX 4060 Laptop GPU
Loading training data from training_data.json...
Loaded 956 training samples

Training Random Forest classifier...
[RandomForest] Training on 764 samples...

Test Performance:
  MSE: 3.82
  R² Score: 0.9234

Model saved to: models/ats_classifier.pkl
```

### 7. Run the Server
```bash
python app.py
```

You'll see:
```
Loading ML model: all-MiniLM-L6-v2
✓ Using GPU: NVIDIA GeForce RTX 4060 Laptop GPU
Loaded trained classifier
ML Scorer ready!
 * Running on http://127.0.0.1:5000
```

### 8. Test It
Open a new terminal:
```bash
cd frontend/public
python -m http.server 8000
```

Visit: http://localhost:8000

Upload a resume and see the ML-powered scoring in action! 🚀

## Troubleshooting

### "CUDA not available"
- Install CUDA Toolkit 12.1
- Reinstall PyTorch: `pip install torch --index-url https://download.pytorch.org/whl/cu121`

### "Kaggle API credentials not found"
- Make sure `kaggle.json` is in: `C:\Users\Arnav\.kaggle\`
- Check permissions (should not be readable by others)

### "Out of memory"
Reduce batch size in `ml_scorer.py` line 168:
```python
sentence_embeddings = self.model.encode(sentences[:25])  # Reduced from 50
```

## What's Next?

1. **Improve Training Data**: Review and adjust scores in `training_data.json`
2. **Retrain**: Run `python train_model.py` again with corrected data
3. **Collect More Data**: Add more resumes to improve accuracy
4. **Fine-tune**: See [TRAINING.md](TRAINING.md) for advanced options

## Performance with RTX 4060

| Operation | Time |
|-----------|------|
| Model Loading | ~2s |
| Resume Scoring | ~0.3-0.5s |
| Training (1000 samples) | ~5-7min |
| Dataset Preparation | ~5min |

## Questions?

See the full guide: [TRAINING.md](TRAINING.md)
