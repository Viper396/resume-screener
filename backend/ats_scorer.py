import re
import os
from collections import Counter
import PyPDF2
import docx

class ATSScorer:
    def __init__(self):
        # Common ATS-friendly keywords by category
        self.technical_skills = {
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 'docker',
            'kubernetes', 'git', 'api', 'machine learning', 'data analysis', 'tensorflow',
            'pytorch', 'pandas', 'numpy', 'scikit-learn', 'html', 'css', 'typescript',
            'angular', 'vue', 'mongodb', 'postgresql', 'redis', 'elasticsearch'
        }
        
        self.soft_skills = {
            'leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
            'project management', 'agile', 'scrum', 'collaboration', 'critical thinking'
        }
        
        # Essential resume sections
        self.required_sections = [
            'experience', 'education', 'skills', 'work', 'employment'
        ]
        
        self.optional_sections = [
            'projects', 'certifications', 'awards', 'publications', 'summary'
        ]

        # Common terms that are too generic to be useful for JD matching.
        self.jd_stopwords = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the', 'to', 'with',
            'will', 'you', 'your', 'we', 'our', 'they', 'this', 'those', 'these',
            'have', 'has', 'had', 'must', 'should', 'can', 'ability', 'experience',
            'year', 'years', 'work', 'working', 'role', 'team', 'job', 'required',
            'preferred', 'plus', 'etc'
        }
    
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
    
    def score_resume(self, text, job_description=None):
        """Main scoring function"""
        text_lower = text.lower()
        
        # Calculate individual scores
        section_score = self._score_sections(text_lower)
        keyword_score = self._score_keywords(text_lower)
        formatting_score = self._score_formatting(text)
        length_score = self._score_length(text)
        contact_score = self._score_contact_info(text)
        
        # Weighted total score
        total_score = (
            section_score * 0.25 +
            keyword_score * 0.30 +
            formatting_score * 0.20 +
            length_score * 0.15 +
            contact_score * 0.10
        )

        jd_match = None
        if job_description and job_description.strip():
            jd_match = self._score_job_description_match(text_lower, job_description.lower())
            # JD match becomes the most important factor when provided.
            total_score = (total_score * 0.55) + (jd_match['match_percentage'] * 0.45)
        
        # Generate feedback
        feedback = self._generate_feedback(
            section_score, keyword_score, formatting_score, 
            length_score, contact_score, text_lower, jd_match
        )
        
        result = {
            'overall_score': round(total_score, 1),
            'breakdown': {
                'sections': round(section_score, 1),
                'keywords': round(keyword_score, 1),
                'formatting': round(formatting_score, 1),
                'length': round(length_score, 1),
                'contact_info': round(contact_score, 1)
            },
            'feedback': feedback,
            'grade': self._get_grade(total_score)
        }

        if jd_match:
            result['breakdown']['jd_match'] = round(jd_match['match_percentage'], 1)
            result['jd_match'] = {
                'match_percentage': round(jd_match['match_percentage'], 1),
                'matched_keywords': jd_match['matched_keywords'],
                'missing_keywords': jd_match['missing_keywords'],
                'total_keywords_considered': jd_match['total_keywords_considered']
            }

        return result

    def _extract_jd_keywords(self, jd_text):
        """Extract meaningful keywords and short phrases from job description text."""
        tokens = re.findall(r'[a-zA-Z][a-zA-Z0-9+#.\-]{1,}', jd_text)
        filtered_tokens = [
            token for token in tokens
            if token not in self.jd_stopwords and len(token) >= 3
        ]

        # Capture short multi-word phrases that often appear in job descriptions.
        phrase_matches = re.findall(r'([a-zA-Z][a-zA-Z0-9+#.\-]{2,}\s+[a-zA-Z][a-zA-Z0-9+#.\-]{2,})', jd_text)
        filtered_phrases = [
            phrase.strip() for phrase in phrase_matches
            if all(part not in self.jd_stopwords for part in phrase.split())
        ]

        token_counter = Counter(filtered_tokens)
        phrase_counter = Counter(filtered_phrases)

        prioritized_tokens = [word for word, _ in token_counter.most_common(40)]
        prioritized_phrases = [phrase for phrase, _ in phrase_counter.most_common(20)]

        # Deduplicate while preserving order.
        combined = []
        seen = set()
        for item in prioritized_phrases + prioritized_tokens:
            if item not in seen:
                seen.add(item)
                combined.append(item)

        return combined[:50]

    def _score_job_description_match(self, resume_text, jd_text):
        """Compute keyword match percentage between resume and job description."""
        jd_keywords = self._extract_jd_keywords(jd_text)
        if not jd_keywords:
            return {
                'match_percentage': 0.0,
                'matched_keywords': [],
                'missing_keywords': [],
                'total_keywords_considered': 0
            }

        matched = [keyword for keyword in jd_keywords if keyword in resume_text]
        missing = [keyword for keyword in jd_keywords if keyword not in resume_text]
        match_percentage = (len(matched) / len(jd_keywords)) * 100

        return {
            'match_percentage': match_percentage,
            'matched_keywords': matched[:20],
            'missing_keywords': missing[:20],
            'total_keywords_considered': len(jd_keywords)
        }
    
    def _score_sections(self, text):
        """Check for essential resume sections"""
        found_required = sum(1 for section in self.required_sections if section in text)
        found_optional = sum(1 for section in self.optional_sections if section in text)
        
        required_score = (found_required / len(self.required_sections)) * 70
        optional_score = (found_optional / len(self.optional_sections)) * 30
        
        return min(required_score + optional_score, 100)
    
    def _score_keywords(self, text):
        """Score based on relevant keywords"""
        technical_found = sum(1 for skill in self.technical_skills if skill in text)
        soft_found = sum(1 for skill in self.soft_skills if skill in text)
        
        # Score based on variety of skills
        technical_score = min((technical_found / 10) * 60, 60)
        soft_score = min((soft_found / 5) * 40, 40)
        
        return technical_score + soft_score
    
    def _score_formatting(self, text):
        """Score formatting and structure"""
        score = 100
        
        # Check for bullet points
        if not ('•' in text or '-' in text or '*' in text):
            score -= 20
        
        # Check for proper capitalization
        lines = text.split('\n')
        capitalized_lines = sum(1 for line in lines if line and line[0].isupper())
        if capitalized_lines < len([l for l in lines if l]) * 0.3:
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
                          length_score, contact_score, text, jd_match=None):
        """Generate actionable feedback"""
        feedback = []

        if jd_match is not None:
            if jd_match['match_percentage'] < 50:
                feedback.append(
                    "Low JD match: Add more job-specific keywords from the description to your resume."
                )
            elif jd_match['match_percentage'] < 75:
                feedback.append(
                    "Moderate JD match: Tailor your resume with more exact terms used in the job description."
                )
            elif jd_match['match_percentage'] >= 90:
                feedback.append(
                    "Excellent JD match: Your resume aligns strongly with the job description keywords."
                )
        
        if section_score < 70:
            feedback.append("Add missing sections like Experience, Education, or Skills.")
        
        if keyword_score < 60:
            feedback.append("Include more relevant technical and soft skills keywords.")
        
        if formatting_score < 70:
            feedback.append("Improve formatting with bullet points and proper capitalization.")
        
        if length_score < 70:
            word_count = len(text.split())
            if word_count < 300:
                feedback.append("Resume is too short. Add more details about your experience.")
            else:
                feedback.append("Resume is too long. Keep it concise (300-800 words).")
        
        if contact_score < 70:
            feedback.append("Ensure your resume includes email, phone, and LinkedIn/GitHub links.")
        
        if not feedback:
            feedback.append("Great job! Your resume is well-optimized for ATS systems.")
        
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
