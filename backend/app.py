from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from ml_scorer import MLATSScorer

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize ML-based scorer
print("Initializing ML-based ATS Scorer...")
scorer = MLATSScorer()
print("ML Scorer ready!")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/score-resume', methods=['POST'])
def score_resume():
    try:
        # Check if file or text is provided
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extract text from file
                text = scorer.extract_text_from_file(filepath)
                
                # Clean up uploaded file
                os.remove(filepath)
            else:
                return jsonify({'error': 'Invalid file type. Allowed: txt, pdf, docx'}), 400
        elif 'text' in request.form:
            text = request.form['text']
        else:
            return jsonify({'error': 'No resume data provided'}), 400
        
        # Score the resume
        result = scorer.score_resume(text)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
