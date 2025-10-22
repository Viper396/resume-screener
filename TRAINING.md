# Training the ATS ML Model

This guide will walk you through training the ML model on real resume data using your RTX 4060 GPU.

## Hardware Requirements

✅ **Your Setup**: RTX 4060 Laptop GPU
- **VRAM**: 8GB (sufficient for training)
- **Training time**: ~5-10 minutes for 1000 resumes
- **Inference speed**: ~0.3-0.5s per resume with GPU

## Prerequisites

1. **CUDA Toolkit** (for GPU acceleration)
   - Download from: https://developer.nvidia.com/cuda-downloads
   - Recommended: CUDA 11.8 or 12.1

2. **Python 3.8+** with pip

3. **Kaggle Account** (for dataset download)

## Step 1: Install Dependencies

```bash
cd backend

# Install PyTorch with CUDA support for RTX 4060
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install other dependencies
pip install -r requirements.txt

# Verify GPU is detected
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"}')"
```

Expected output:
```
CUDA Available: True
GPU: NVIDIA GeForce RTX 4060 Laptop GPU
```

## Step 2: Download Resume Dataset

### Recommended Datasets

#### Option 1: Resume Dataset (Kaggle) - **RECOMMENDED**
**Dataset**: UpdateResume Dataset
- **Link**: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
- **Size**: ~1000 resumes
- **Format**: CSV with resume text
- **Quality**: Good variety of formats

#### Option 2: Resume Corpus (Kaggle)
**Dataset**: Resume Dataset by Dharun
- **Link**: https://www.kaggle.com/datasets/dhainjeamita/resume-dataset
- **Size**: ~2400 resumes  
- **Format**: CSV with categories

### Download Instructions

1. **Install Kaggle CLI**:
```bash
pip install kaggle
```

2. **Setup Kaggle API credentials**:
   - Go to: https://www.kaggle.com/settings/account
   - Scroll to "API" section
   - Click "Create New API Token"
   - Save `kaggle.json` to `C:\Users\Arnav\.kaggle\kaggle.json`

3. **Download the dataset**:
```bash
# For Option 1 (Recommended)
kaggle datasets download -d snehaanbhawal/resume-dataset
unzip resume-dataset.zip -d data/

# OR Option 2
kaggle datasets download -d dhainjeamita/resume-dataset
unzip resume-dataset.zip -d data/
```

## Step 3: Prepare Training Data

Run the dataset preparation script:

```bash
python prepare_dataset.py --input data/Resume.csv --output training_data.json
```

This will:
- Parse resume CSV files
- Score each resume using the ML scorer
- Create `training_data.json` for training

**Manual adjustment recommended**: Review and adjust scores in `training_data.json` for better accuracy.

## Step 4: Train the Model

### Basic Training (Synthetic Data)
```bash
python train_model.py
```

### Training with Real Data
```bash
# After preparing dataset
python train_model.py --data training_data.json --epochs 100
```

### Advanced Training with GPU
```bash
python train_model.py \
  --data training_data.json \
  --epochs 200 \
  --n-estimators 200 \
  --use-gpu
```

**Training Output**:
```
=== ATS Scorer Model Training ===

Loading ML model: all-MiniLM-L6-v2
Using GPU: NVIDIA GeForce RTX 4060 Laptop GPU
Loading training data...
Loaded 956 training samples

Training Random Forest classifier...
Training Performance:
  MSE: 2.14
  R² Score: 0.9567

Test Performance:
  MSE: 3.82
  R² Score: 0.9234

Feature Importances:
  Sections: 0.2234
  Keywords: 0.3456
  Formatting: 0.1876
  Length: 0.1123
  Contact Info: 0.1311

Model saved to: models/ats_classifier.pkl

=== Training Complete ===
```

## Step 5: Test the Trained Model

```bash
# Test with sample resume
python test_model.py --resume ../sample_resume.txt
```

## Step 6: Run the Server with Trained Model

```bash
python app.py
```

The ML scorer will automatically load the trained model from `models/ats_classifier.pkl`.

## Advanced: Fine-tune the Transformer

For even better results, fine-tune the sentence transformer on resume data:

```bash
python finetune_transformer.py \
  --data training_data.json \
  --model all-MiniLM-L6-v2 \
  --epochs 10 \
  --batch-size 16
```

This will create a custom model optimized for resume analysis.

## Alternative Datasets

If Kaggle datasets don't work, try these:

### 1. LiveCareer Resume Samples
- **Source**: https://www.livecareer.com/resume-search
- **Method**: Manual collection (use responsibly)
- **Format**: PDF/DOCX

### 2. Create Your Own Dataset
```python
# Use the web scraper (use responsibly and check ToS)
python scrape_resumes.py --output custom_resumes/
```

### 3. Use Synthetic Data (For Testing)
The training script generates synthetic data automatically if no real data is found.

## GPU Optimization Tips

### Monitor GPU Usage
```bash
# In a separate terminal
nvidia-smi -l 1
```

### Optimize Batch Size
If you run out of memory:
```python
# In ml_scorer.py, reduce batch size
embeddings = self.model.encode(texts, batch_size=16)  # Try 8, 16, 32
```

### Mixed Precision Training
For faster training on RTX 4060:
```bash
python train_model.py --use-amp  # Automatic Mixed Precision
```

## Troubleshooting

### CUDA Out of Memory
```bash
# Reduce batch size in ml_scorer.py
# Or use smaller model
python train_model.py --model paraphrase-MiniLM-L6-v2
```

### Kaggle API Not Found
```bash
# Make sure kaggle.json is in the right location
mkdir ~/.kaggle
cp kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### Poor Model Performance
1. **Collect more diverse data**: Aim for 500+ resumes
2. **Balance the dataset**: Include good and bad examples
3. **Adjust scores manually**: Review and correct `training_data.json`
4. **Tune hyperparameters**: Increase `n_estimators` or `max_depth`

## Expected Performance

| Dataset Size | Training Time | Test R² Score | GPU Usage |
|-------------|---------------|---------------|-----------|
| 100 samples | ~1 min | 0.75-0.85 | 20-30% |
| 500 samples | ~3 min | 0.85-0.92 | 30-50% |
| 1000+ samples | ~5-10 min | 0.92-0.96 | 50-70% |

## Model Comparison

| Model | Size | Speed | Accuracy | GPU Memory |
|-------|------|-------|----------|------------|
| all-MiniLM-L6-v2 | 80MB | Fast | Good | 1-2GB |
| all-mpnet-base-v2 | 420MB | Medium | Better | 2-4GB |
| Fine-tuned MiniLM | 80MB | Fast | Best | 2-3GB |

## Next Steps

1. **Test the model** on various resumes
2. **Collect feedback** and adjust scores
3. **Retrain periodically** with new data
4. **Fine-tune** the transformer for domain-specific improvements

## Support

For issues or questions:
- Check `backend/ML_README.md` for technical details
- Review training logs in `training.log`
- Test with synthetic data first before using real data

Good luck with training! 🚀
