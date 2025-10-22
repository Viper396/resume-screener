# ATS Resume Scorer 📄

A **machine learning-powered** web application that analyzes resumes using **semantic understanding** and provides an ATS (Applicant Tracking System) compatibility score with actionable feedback.

## Features

- **Resume Upload**: Supports PDF, DOCX, and TXT formats
- **🧠 ML-Powered Scoring**: Uses transformer models (sentence-BERT) for semantic analysis
  - **Semantic section detection** - understands context, not just keywords
  - **Contextual skill matching** - recognizes synonyms and related concepts
  - **Trainable model** - improves with your own labeled data
- **Analyzes 5 Key Dimensions**:
  - Section completeness (Experience, Education, Skills, etc.)
  - Keyword optimization (Technical & Soft skills)
  - Formatting quality
  - Resume length
  - Contact information
- **Detailed Feedback**: Provides actionable recommendations to improve your resume
- **Visual Results**: Interactive score visualization with breakdowns
- **Modern UI**: Clean, responsive interface with drag-and-drop support
- **GPU Acceleration**: Optional CUDA support for faster processing

## Tech Stack

### Backend
- Python 3.8+
- Flask (REST API)
- **Sentence-Transformers** (ML embeddings)
- **PyTorch** (Deep learning framework)
- **Scikit-learn** (ML training)
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)

### Frontend
- Vanilla JavaScript
- HTML5 & CSS3
- Modern responsive design

### ML Models
- **Sentence-BERT** (all-MiniLM-L6-v2) - 80MB
- **Random Forest** classifier (optional, trainable)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)
- **(Optional)** CUDA-capable GPU for faster processing
- **(Optional)** Kaggle account for downloading training datasets

### Quick Start (Local Setup)

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/ats-resume-scorer.git
cd ats-resume-scorer
```

2. **Start the backend:**

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (this will download the ML model ~80MB on first run)
pip install -r requirements.txt

# Optional: Install PyTorch with CUDA support for GPU acceleration
# For NVIDIA GPUs (RTX 3000/4000 series):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Run the Flask server
python app.py
```

The backend will start on `http://localhost:5000`

3. **Start the frontend (in a new terminal):**

```bash
cd frontend/public

# Using Python (any version)
python -m http.server 8000

# OR using Node.js
npx http-server -p 8000
```

4. **Open your browser and navigate to:**
```
http://localhost:8000
```

### Backend Setup (Detailed)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup (Detailed)

1. Navigate to the frontend directory:
```bash
cd frontend/public
```

2. Open `index.html` in your browser, or use a simple HTTP server:

**Using Python:**
```bash
python -m http.server 8000
```

**Using Node.js (http-server):**
```bash
npx http-server -p 8000
```

3. Open your browser and go to `http://localhost:8000`

## Usage

1. Start the backend server (Flask API must be running)
2. Open the frontend in your browser
3. Upload your resume (PDF, DOCX, or TXT)
4. Click "Analyze Resume"
5. Review your ATS score and recommendations
6. Improve your resume based on feedback and re-test

## ML Scoring Algorithm

The system uses **semantic similarity** and machine learning to evaluate resumes:

### How It Works

1. **Embedding Generation**: Resume text is converted to 384-dimensional embeddings using sentence-BERT
2. **Semantic Matching**: Compares resume content to ideal reference texts using cosine similarity
3. **Component Scoring**: Evaluates 5 key dimensions
4. **Optional ML Classifier**: Learns non-linear patterns from labeled data

### Scoring Components

#### 1. Sections (25% weight)
- **Semantic detection** of: Experience, Education, Skills, Projects, Certifications
- Understands variations: "Work History" = "Professional Experience" = "Employment"

#### 2. Keywords (30% weight)
- **Contextual matching** against reference skill descriptions
- Technical skills: Python, JavaScript, React, AWS, Docker, ML, etc.
- Soft skills: Leadership, Communication, Problem-solving, etc.
- Recognizes synonyms and related concepts

#### 3. Formatting (20% weight)
- Bullet points and structure
- Proper capitalization
- Clean special character usage

#### 4. Length (15% weight)
- Optimal: 300-800 words
- Acceptable: 200-1000 words

#### 5. Contact Information (10% weight)
- Email address
- Phone number  
- LinkedIn/GitHub profile

### Advantages Over Rule-Based Scoring

✅ **Semantic Understanding**: Recognizes meaning, not just keywords  
✅ **Context-Aware**: Distinguishes "managed teams" from "managed databases"  
✅ **Flexible**: Handles variations in wording and format  
✅ **Trainable**: Improves with your own labeled data

## Project Structure

```
ats-resume-scorer/
├── backend/
│   ├── app.py                # Flask API server
│   ├── ml_scorer.py          # 🧠 ML-based scorer (NEW)
│   ├── ats_scorer.py         # Legacy rule-based scorer
│   ├── train_model.py        # Model training script
│   ├── prepare_dataset.py    # Dataset preparation
│   ├── requirements.txt      # Python dependencies
│   ├── ML_README.md          # ML documentation
│   └── models/               # Trained models (generated)
├── frontend/
│   └── public/
│       ├── index.html        # Main HTML file
│       ├── styles.css        # Styling
│       └── script.js         # Frontend logic
├── TRAINING.md               # 📚 Complete training guide
└── README.md                 # This file
```

## API Endpoints

### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy"
}
```

### `POST /api/score-resume`
Analyze and score a resume

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (PDF, DOCX, or TXT)

**Response:**
```json
{
  "overall_score": 85.5,
  "breakdown": {
    "sections": 90.0,
    "keywords": 78.0,
    "formatting": 85.0,
    "length": 100.0,
    "contact_info": 70.0
  },
  "feedback": [
    "Include more relevant technical and soft skills keywords.",
    "Ensure your resume includes email, phone, and LinkedIn/GitHub links."
  ],
  "grade": "B",
  "ml_powered": true
}
```

## Training the ML Model

### Quick Start

The ML scorer works out-of-the-box with semantic similarity. To improve it with custom training:

**Step 1: Download Resume Dataset**
```bash
cd backend

# Install Kaggle CLI
pip install kaggle

# Download dataset (requires Kaggle API token)
kaggle datasets download -d snehaanbhawal/resume-dataset
unzip resume-dataset.zip -d data/
```

**Step 2: Prepare Training Data**
```bash
python prepare_dataset.py --input data/Resume.csv --output training_data.json
```

**Step 3: Train the Model**
```bash
# Basic training
python train_model.py

# With GPU acceleration (RTX 4060)
python train_model.py --data training_data.json --n-estimators 200 --use-gpu
```

**Step 4: Restart Server**
```bash
python app.py  # The trained model loads automatically
```

### Detailed Training Instructions

For complete training guide with GPU optimization, dataset recommendations, and troubleshooting:

**📚 See [TRAINING.md](TRAINING.md)** - Complete step-by-step guide for RTX 4060

**Recommended Datasets:**
- [Resume Dataset (Kaggle)](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset) - 1000+ resumes
- [Resume Corpus (Kaggle)](https://www.kaggle.com/datasets/dhainjeamita/resume-dataset) - 2400+ resumes

## Customization

### ML Model Customization

**Change the transformer model:**
```python
# In backend/ml_scorer.py
scorer = MLATSScorer(model_name='all-mpnet-base-v2')  # Better quality, slower
```

**Add custom reference texts:**
```python
# In backend/ml_scorer.py, modify reference_texts
self.reference_texts = {
    'technical_skills': [
        'Your domain-specific skills here',
        'Add industry-specific keywords',
    ]
}
```

### Legacy Rule-Based Scorer

To use the old rule-based scorer:
```python
# In backend/app.py, change:
from ml_scorer import MLATSScorer
# to:
from ats_scorer import ATSScorer
```

**Adding keywords (rule-based):**
Edit `backend/ats_scorer.py`:
- `self.technical_skills` - Technical keywords
- `self.soft_skills` - Soft skill keywords

## Troubleshooting

### ML Model Issues

**Model download fails:**
```bash
# Pre-download the model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

**GPU not detected:**
```bash
# Verify CUDA installation
python -c "import torch; print(torch.cuda.is_available())"

# Reinstall PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Out of memory:**
```python
# Use smaller model in ml_scorer.py
scorer = MLATSScorer(model_name='paraphrase-MiniLM-L3-v2')
```

### CORS Issues
If you encounter CORS errors, ensure:
1. Flask-CORS is installed
2. Backend is running on port 5000
3. Frontend API_URL matches backend URL

### File Upload Errors
- Check file size (max 16MB)
- Verify file format (PDF, DOCX, TXT only)
- Ensure uploads directory has write permissions

### PDF Parsing Issues
Some PDFs may not parse correctly if they contain:
- Scanned images without OCR
- Complex layouts
- Password protection

**Solution:** Convert to TXT or recreate as a simple DOCX

## Performance

| Metric | CPU | GPU (RTX 4060) |
|--------|-----|----------------|
| Model Load Time | ~3s | ~2s |
| First Score | ~2s | ~0.5s |
| Subsequent Scores | ~1s | ~0.3s |
| Training (1000 samples) | ~10min | ~5min |

## Future Enhancements

- [x] ML-powered semantic scoring
- [x] GPU acceleration support
- [x] Trainable model with custom datasets
- [ ] Fine-tune transformer on resume-specific data
- [ ] Support for more file formats
- [ ] Job description matching & ATS comparison
- [ ] Resume comparison feature
- [ ] Export detailed reports as PDF
- [ ] Industry-specific scoring profiles
- [ ] Resume templates and examples
- [ ] Multi-language support

## License

MIT License - Feel free to use and modify for your projects

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the GitHub repository.
