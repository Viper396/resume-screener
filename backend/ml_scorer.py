import re
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import torch
import PyPDF2
import docx

class MLATSScorer:
    def __init__(self, model_name='all-MiniLM-L6-v2', use_gpu=True):
        """
        Initialize ML-based ATS scorer
        Uses sentence transformers for semantic similarity
        
        Args:
            model_name: Sentence transformer model to use
            use_gpu: Whether to use GPU if available
        """
        print(f"Loading ML model: {model_name}")
        
        # Detect and configure device
        if use_gpu and torch.cuda.is_available():
            self.device = 'cuda'
            print(f"✓ Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self.device = 'cpu'
            print("Using CPU")
        
        self.model = SentenceTransformer(model_name, device=self.device)
        
        # Reference embeddings for different resume aspects
        self.reference_texts = {
            'technical_skills': [
                'Proficient in Python, Java, JavaScript, React, Node.js, and SQL',
                'Experience with AWS, Docker, Kubernetes, and cloud technologies',
                'Machine learning expertise with TensorFlow, PyTorch, scikit-learn',
                'Full-stack development with modern frameworks and databases',
                'Data analysis and visualization with Pandas, NumPy, Matplotlib'
            ],
            'soft_skills': [
                'Strong leadership and team collaboration abilities',
                'Excellent communication and presentation skills',
                'Problem-solving and analytical thinking capabilities',
                'Project management and agile methodology experience',
                'Cross-functional teamwork and stakeholder management'
            ],
            'experience': [
                'Software Engineer with 3+ years of experience building scalable applications',
                'Led development teams and managed complex technical projects',
                'Developed and deployed production systems serving millions of users',
                'Contributed to open-source projects and technical communities',
                'Designed system architecture and implemented best practices'
            ],
            'education': [
                'Bachelor of Science in Computer Science',
                'Master of Engineering in Software Engineering',
                'Relevant certifications and continuous learning',
                'Strong academic background with honors and achievements'
            ]
        }
        
        # Pre-compute reference embeddings
        self.reference_embeddings = {}
        for category, texts in self.reference_texts.items():
            self.reference_embeddings[category] = self.model.encode(texts)
        
        # Try to load trained classifier if available
        self.classifier = None
        self.load_classifier()
    
    def load_classifier(self):
        """Load pre-trained classifier if available"""
        classifier_path = 'models/ats_classifier.pkl'
        if os.path.exists(classifier_path):
            try:
                with open(classifier_path, 'rb') as f:
                    self.classifier = pickle.load(f)
                print("Loaded trained classifier")
            except Exception as e:
                print(f"Could not load classifier: {e}")
    
    def extract_text_from_file(self, filepath):
        """Extract text from PDF, DOCX, or TXT files"""
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.pdf':
            return self._extract_from_pdf(filepath)
        elif ext == '.docx':
            return self._extract_from_docx(filepath)
        elif ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _extract_from_pdf(self, filepath):
        """Extract text from PDF"""
        text = ""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    def _extract_from_docx(self, filepath):
        """Extract text from DOCX"""
        try:
            doc = docx.Document(filepath)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
        return text
    
    def score_resume(self, text):
        """
        Main ML-based scoring function
        Uses semantic similarity and learned patterns
        """
        # Extract features from resume
        features = self._extract_ml_features(text)
        
        # Calculate individual component scores
        section_score = self._ml_score_sections(text, features)
        keyword_score = self._ml_score_keywords(text, features)
        formatting_score = self._score_formatting(text)
        length_score = self._score_length(text)
        contact_score = self._score_contact_info(text)
        
        # Use trained classifier if available, otherwise use weighted sum
        if self.classifier:
            # Prepare feature vector for classifier
            feature_vector = np.array([
                section_score, keyword_score, formatting_score, 
                length_score, contact_score
            ]).reshape(1, -1)
            total_score = self.classifier.predict(feature_vector)[0]
        else:
            # Fallback to weighted sum
            total_score = (
                section_score * 0.25 +
                keyword_score * 0.30 +
                formatting_score * 0.20 +
                length_score * 0.15 +
                contact_score * 0.10
            )
        
        # Generate feedback
        feedback = self._generate_feedback(
            section_score, keyword_score, formatting_score,
            length_score, contact_score, text
        )
        
        return {
            'overall_score': round(total_score, 1),
            'breakdown': {
                'sections': round(section_score, 1),
                'keywords': round(keyword_score, 1),
                'formatting': round(formatting_score, 1),
                'length': round(length_score, 1),
                'contact_info': round(contact_score, 1)
            },
            'feedback': feedback,
            'grade': self._get_grade(total_score),
            'ml_powered': True
        }
    
    def _extract_ml_features(self, text):
        """Extract semantic features using ML embeddings"""
        # Split text into sentences for better semantic analysis
        sentences = [s.strip() for s in re.split(r'[.!?\n]+', text) if len(s.strip()) > 10]
        
        if not sentences:
            return {'embeddings': None, 'sentence_embeddings': None}
        
        # Get embeddings for the entire text and individual sentences
        full_embedding = self.model.encode([text])[0]
        sentence_embeddings = self.model.encode(sentences[:50])  # Limit to first 50 sentences
        
        return {
            'full_embedding': full_embedding,
            'sentence_embeddings': sentence_embeddings,
            'sentences': sentences[:50]
        }
    
    def _ml_score_sections(self, text, features):
        """Score sections using semantic similarity"""
        if features['full_embedding'] is None:
            return 0
        
        text_lower = text.lower()
        score = 0
        
        # Check for section headers using semantic similarity
        section_indicators = [
            'professional experience', 'work experience', 'employment history',
            'education', 'academic background',
            'skills', 'technical skills', 'core competencies',
            'projects', 'personal projects',
            'certifications', 'awards', 'achievements'
        ]
        
        # Use ML to detect sections
        section_embeddings = self.model.encode(section_indicators)
        sentence_embeddings = features['sentence_embeddings']
        
        # Calculate similarity between sentences and section indicators
        similarities = cosine_similarity(sentence_embeddings, section_embeddings)
        max_similarities = similarities.max(axis=0)
        
        # Count sections with high similarity (likely section headers)
        sections_found = (max_similarities > 0.6).sum()
        
        # Base score on number of sections found
        score = min((sections_found / 5) * 100, 100)
        
        return score
    
    def _ml_score_keywords(self, text, features):
        """Score keywords using semantic similarity with reference skills"""
        if features['full_embedding'] is None:
            return 0
        
        full_embedding = features['full_embedding'].reshape(1, -1)
        
        # Calculate similarity with technical skills references
        tech_similarities = cosine_similarity(
            full_embedding, 
            self.reference_embeddings['technical_skills']
        )
        tech_score = float(tech_similarities.max()) * 60
        
        # Calculate similarity with soft skills references
        soft_similarities = cosine_similarity(
            full_embedding,
            self.reference_embeddings['soft_skills']
        )
        soft_score = float(soft_similarities.max()) * 40
        
        return min(tech_score + soft_score, 100)
    
    def _score_formatting(self, text):
        """Score formatting and structure"""
        score = 100
        
        # Check for bullet points
        if not ('•' in text or '-' in text or '*' in text):
            score -= 20
        
        # Check for proper capitalization
        lines = text.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        if non_empty_lines:
            capitalized_lines = sum(1 for line in non_empty_lines if line[0].isupper())
            if capitalized_lines < len(non_empty_lines) * 0.3:
                score -= 15
        
        # Check for excessive special characters
        special_chars = len(re.findall(r'[^\w\s.,;:()\-•*]', text))
        if special_chars > 50:
            score -= 15
        
        return max(score, 0)
    
    def _score_length(self, text):
        """Score resume length (word count)"""
        word_count = len(text.split())
        
        if 300 <= word_count <= 800:
            return 100
        elif 200 <= word_count < 300 or 800 < word_count <= 1000:
            return 80
        elif 100 <= word_count < 200 or 1000 < word_count <= 1200:
            return 60
        else:
            return 40
    
    def _score_contact_info(self, text):
        """Check for contact information"""
        score = 0
        
        # Email
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            score += 40
        
        # Phone
        if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text):
            score += 30
        
        # LinkedIn or professional link
        if 'linkedin' in text.lower() or 'github' in text.lower():
            score += 30
        
        return score
    
    def _generate_feedback(self, section_score, keyword_score, formatting_score,
                          length_score, contact_score, text):
        """Generate actionable feedback"""
        feedback = []
        
        if section_score < 70:
            feedback.append("Add clear section headers like Experience, Education, Skills, and Projects.")
        
        if keyword_score < 60:
            feedback.append("Include more relevant technical skills and professional competencies that match industry standards.")
        
        if formatting_score < 70:
            feedback.append("Improve formatting with bullet points and consistent capitalization.")
        
        if length_score < 70:
            word_count = len(text.split())
            if word_count < 300:
                feedback.append("Resume is too short. Add more details about your experience and achievements.")
            else:
                feedback.append("Resume is too long. Keep it concise (300-800 words).")
        
        if contact_score < 70:
            feedback.append("Ensure your resume includes email, phone number, and professional profile links (LinkedIn/GitHub).")
        
        if not feedback:
            feedback.append("Excellent! Your resume is well-optimized for ATS systems with strong semantic content.")
        
        return feedback
    
    def _get_grade(self, score):
        """Convert score to letter grade"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
