# ML-Based ATS Resume Scorer

This implementation replaces the rule-based scoring system with a machine learning approach using transformer models.

## Overview

The ML scorer uses two main techniques:

1. **Semantic Similarity**: Uses sentence-transformers (MiniLM model) to understand resume content semantically
2. **Custom Classifier**: Optional Random Forest model that learns from labeled data

## Features

- **Semantic Analysis**: Understands meaning, not just keyword matching
- **Better Section Detection**: Identifies sections using semantic similarity
- **Skill Matching**: Compares resume content to ideal skill descriptions
- **Trainable**: Improves with more labeled data

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# This will download the ML model (~80MB) on first run
```

## Usage

### Basic Usage (Zero-Shot)

The ML scorer works immediately without training:

```python
from ml_scorer import MLATSScorer

scorer = MLATSScorer()
result = scorer.score_resume(resume_text)
```

### Training a Custom Model (Optional)

To improve accuracy with your own data:

1. **Prepare training data** (`training_data.json`):
```json
[
  {
    "text": "Full resume text here...",
    "scores": {
      "sections": 85,
      "keywords": 75,
      "formatting": 90,
      "length": 100,
      "contact_info": 80
    },
    "overall_score": 84.5
  }
]
```

2. **Train the model**:
```bash
python train_model.py
```

3. **The model is automatically loaded** when the scorer initializes

### Generate Synthetic Training Data

For testing purposes:

```bash
python train_model.py  # Will auto-generate synthetic data if none exists
```

## How It Works

### 1. Semantic Section Detection

Instead of simple keyword matching, the ML scorer:
- Encodes each sentence in the resume
- Compares against section header embeddings
- Uses cosine similarity to identify sections

### 2. Skill Scoring

The scorer maintains reference texts for ideal skills:
- Technical skills (Python, React, AWS, etc.)
- Soft skills (Leadership, Communication, etc.)

It compares the resume's semantic content to these references.

### 3. Custom Classifier (Optional)

After training:
- Takes the 5 component scores as input
- Learns non-linear relationships
- Produces more nuanced overall scores

## Model Details

### Sentence Transformer
- **Model**: `all-MiniLM-L6-v2`
- **Size**: ~80MB
- **Speed**: ~100 sentences/second
- **Embeddings**: 384 dimensions

### Random Forest (if trained)
- **Type**: Regressor
- **Trees**: 100
- **Features**: 5 (component scores)

## Advantages Over Rule-Based

1. **Semantic Understanding**: Recognizes synonyms and related concepts
   - "Software Engineer" ≈ "Developer" ≈ "Programmer"
   
2. **Flexible Section Detection**: Handles variations
   - "Work Experience" = "Professional Background" = "Employment"
   
3. **Contextual Skills**: Understands skills in context
   - Distinguishes between "managed teams" and "managed databases"

4. **Trainable**: Gets better with more data

## Performance

First run will download the model (~80MB). Subsequent runs:
- **Load time**: ~2-3 seconds
- **Scoring time**: ~0.5-1 second per resume

## Customization

### Change the Transformer Model

```python
scorer = MLATSScorer(model_name='paraphrase-multilingual-MiniLM-L12-v2')
```

Options:
- `all-MiniLM-L6-v2` - Fast, good quality (default)
- `all-mpnet-base-v2` - Better quality, slower
- `paraphrase-multilingual-*` - Multilingual support

### Add Custom Reference Texts

Edit `ml_scorer.py`:

```python
self.reference_texts = {
    'technical_skills': [
        'Your custom reference texts here',
        'Add domain-specific skills',
    ],
    # ...
}
```

## Training Tips

1. **Collect Real Data**: Get actual resumes with scores
2. **Diverse Examples**: Include various formats and industries
3. **Balanced Scores**: Include good and bad examples
4. **Size**: Aim for 100+ labeled samples minimum

## Troubleshooting

### Model Download Issues
```bash
# Pre-download the model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Memory Issues
Use a smaller model:
```python
scorer = MLATSScorer(model_name='paraphrase-MiniLM-L3-v2')
```

### Slow Performance
- Use CPU if GPU causes issues
- Consider caching embeddings for repeated evaluations

## Future Enhancements

- [ ] Fine-tune transformer on resume data
- [ ] Add job description matching
- [ ] Multi-language support
- [ ] Resume ranking/comparison
- [ ] Explanation of scores (SHAP values)

## Comparison: Rule-Based vs ML

| Feature | Rule-Based | ML-Based |
|---------|-----------|----------|
| Section Detection | Exact keyword match | Semantic similarity |
| Skill Recognition | Fixed keyword list | Contextual understanding |
| Trainability | Fixed rules | Learns from data |
| Speed | Very fast (~0.1s) | Fast (~1s) |
| Setup | Instant | Model download |
| Accuracy | Good | Better |

## License

Same as main project (MIT)
