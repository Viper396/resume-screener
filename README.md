# ATS Resume Scorer 📄

A machine learning-powered web application that analyzes resumes and provides an ATS (Applicant Tracking System) compatibility score with actionable feedback.

## Features

- **Resume Upload**: Supports PDF, DOCX, and TXT formats
- **ML-Based Scoring**: Analyzes resumes across 5 key dimensions:
  - Section completeness (Experience, Education, Skills, etc.)
  - Keyword optimization (Technical & Soft skills)
  - Formatting quality
  - Resume length
  - Contact information
- **Detailed Feedback**: Provides actionable recommendations to improve your resume
- **Visual Results**: Interactive score visualization with breakdowns
- **Modern UI**: Clean, responsive interface with drag-and-drop support

## Tech Stack

### Backend
- Python 3.8+
- Flask (REST API)
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)

### Frontend
- Vanilla JavaScript
- HTML5 & CSS3
- Modern responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd ats-resume-scorer/backend
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

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd ats-resume-scorer/frontend/public
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

4. Select the public folder from the available options

## Usage

1. Start the backend server (Flask API must be running)
2. Open the frontend in your browser
3. Upload your resume (PDF, DOCX, or TXT)
4. Click "Analyze Resume"
5. Review your ATS score and recommendations
6. Improve your resume based on feedback and re-test

## Scoring Algorithm

The ATS scoring system evaluates resumes based on:

### 1. Sections (25% weight)
- Required: Experience, Education, Skills
- Optional: Projects, Certifications, Awards, Summary

### 2. Keywords (30% weight)
- Technical skills (Python, JavaScript, React, etc.)
- Soft skills (Leadership, Communication, etc.)

### 3. Formatting (20% weight)
- Proper use of bullet points
- Capitalization
- Special character usage

### 4. Length (15% weight)
- Optimal: 300-800 words
- Acceptable: 200-1000 words

### 5. Contact Information (10% weight)
- Email address
- Phone number
- LinkedIn/GitHub profile

## Project Structure

```
ats-resume-scorer/
├── backend/
│   ├── app.py              # Flask API server
│   ├── ats_scorer.py       # ML scoring logic
│   └── requirements.txt    # Python dependencies
└── frontend/
    └── public/
        ├── index.html      # Main HTML file
        ├── styles.css      # Styling
        └── script.js       # Frontend logic
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
  "grade": "B"
}
```

## Customization

### Adding More Keywords
Edit `backend/ats_scorer.py` and add keywords to:
- `self.technical_skills` - Technical skill keywords
- `self.soft_skills` - Soft skill keywords

### Adjusting Weights
Modify the weights in the `score_resume` method:
```python
total_score = (
    section_score * 0.25 +      # Sections weight
    keyword_score * 0.30 +      # Keywords weight
    formatting_score * 0.20 +   # Formatting weight
    length_score * 0.15 +       # Length weight
    contact_score * 0.10        # Contact info weight
)
```

## Troubleshooting

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

## Future Enhancements

- [ ] Add machine learning model training on real ATS data
- [ ] Support for more file formats
- [ ] Job-specific keyword recommendations
- [ ] Resume comparison feature
- [ ] Export detailed reports as PDF
- [ ] Industry-specific scoring profiles
- [ ] Resume templates and examples

## License

MIT License - Feel free to use and modify for your projects

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the GitHub repository.
