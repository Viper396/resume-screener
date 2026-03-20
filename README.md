# ATS Resume Scorer

A practical ATS-style resume analyzer that now supports **Job Description matching**.
Upload your resume, paste a JD, and get:

- overall ATS score
- detailed score breakdown
- JD keyword match percentage
- matched and missing JD keywords
- actionable recommendations

## What Changed Recently

- Added **Job Description Matching** as a first-class feature.
- Migrated frontend from vanilla HTML/CSS/JS to **React + Vite + Tailwind CSS**.
- Refactored frontend into reusable components and service/util layers.

## Tech Stack

### Backend
- Python 3.8+
- Flask + Flask-CORS
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)

### Frontend
- React (Vite)
- Tailwind CSS (via `@tailwindcss/vite`)

## Project Structure

```text
resume-screener/
├── backend/
│   ├── app.py
│   ├── ats_scorer.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── constants/
    │   ├── services/
    │   └── utils/
    ├── package.json
    └── vite.config.js
```

## Local Setup

### 1. Backend

```bash
cd backend

# Optional but recommended
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Backend runs at `http://localhost:5000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## Usage

1. Start backend and frontend.
2. Open the frontend URL.
3. Upload a resume (`.pdf`, `.docx`, `.txt`).
4. Paste the target job description.
5. Click **Analyze Resume**.
6. Review overall score, breakdown, and JD keyword matching details.

## API

### `GET /api/health`

Health check endpoint.

Example response:

```json
{
  "status": "healthy"
}
```

### `POST /api/score-resume`

Analyze and score a resume.

Form fields:

- `file`: resume file (`pdf`, `docx`, `txt`) OR `text`
- `job_description`: pasted job description text

Example response:

```json
{
  "overall_score": 82.4,
  "breakdown": {
    "jd_match": 76.3,
    "sections": 84.0,
    "keywords": 79.0,
    "formatting": 88.0,
    "length": 100.0,
    "contact_info": 70.0
  },
  "jd_match": {
    "match_percentage": 76.3,
    "matched_keywords": ["python", "sql"],
    "missing_keywords": ["docker", "kubernetes"],
    "total_keywords_considered": 38
  },
  "feedback": [
    "Moderate JD match: Tailor your resume with more exact terms used in the job description."
  ],
  "grade": "B"
}
```

## Configuration

Frontend reads backend URL from:

- `VITE_API_URL` (optional)

If not set, it defaults to `http://localhost:5000`.

## Troubleshooting

### "Failed to fetch"

Usually means backend is not running or not reachable.

Check:

1. Backend process is running on port `5000`.
2. `http://localhost:5000/api/health` returns healthy.
3. Frontend is using the correct API URL.

### Resume upload/parsing errors

- Keep files under 16MB.
- Use supported formats (`pdf`, `docx`, `txt`).
- Some scanned/image-heavy PDFs may parse poorly.

## License

MIT License.
