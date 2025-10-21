const API_URL = 'http://localhost:5000';

let selectedFile = null;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeFile = document.getElementById('removeFile');
const scoreBtn = document.getElementById('scoreBtn');
const btnText = document.getElementById('btnText');
const loader = document.getElementById('loader');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const resetBtn = document.getElementById('resetBtn');

// Drag and drop handlers
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// File input handler
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

// Handle file selection
function handleFileSelect(file) {
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    
    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please upload PDF, DOCX, or TXT files.');
        return;
    }
    
    if (file.size > 16 * 1024 * 1024) {
        showError('File size exceeds 16MB limit.');
        return;
    }
    
    selectedFile = file;
    fileName.textContent = file.name;
    fileInfo.style.display = 'flex';
    uploadArea.style.display = 'none';
    scoreBtn.disabled = false;
    hideError();
}

// Remove file
removeFile.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    uploadArea.style.display = 'block';
    scoreBtn.disabled = true;
});

// Score resume
scoreBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    btnText.style.display = 'none';
    loader.style.display = 'inline-block';
    scoreBtn.disabled = true;
    hideError();
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        const response = await fetch(`${API_URL}/api/score-resume`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to score resume');
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        showError(error.message);
        btnText.style.display = 'inline';
        loader.style.display = 'none';
        scoreBtn.disabled = false;
    }
});

// Display results
function displayResults(data) {
    // Hide upload section
    document.querySelector('.upload-section').style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Animate score circle
    const score = data.overall_score;
    const circumference = 565;
    const offset = circumference - (score / 100) * circumference;
    
    setTimeout(() => {
        document.getElementById('scoreCircle').style.strokeDashoffset = offset;
        document.getElementById('scoreNumber').textContent = score;
        document.getElementById('scoreGrade').textContent = data.grade;
    }, 100);
    
    // Update breakdown bars
    updateBreakdownBar('sectionsBar', 'sectionsScore', data.breakdown.sections);
    updateBreakdownBar('keywordsBar', 'keywordsScore', data.breakdown.keywords);
    updateBreakdownBar('formattingBar', 'formattingScore', data.breakdown.formatting);
    updateBreakdownBar('lengthBar', 'lengthScore', data.breakdown.length);
    updateBreakdownBar('contactBar', 'contactScore', data.breakdown.contact_info);
    
    // Display feedback
    const feedbackList = document.getElementById('feedbackList');
    feedbackList.innerHTML = '';
    data.feedback.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        feedbackList.appendChild(li);
    });
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Update breakdown bar
function updateBreakdownBar(barId, scoreId, value) {
    setTimeout(() => {
        document.getElementById(barId).style.width = `${value}%`;
        document.getElementById(scoreId).textContent = value;
    }, 100);
}

// Reset
resetBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    uploadArea.style.display = 'block';
    scoreBtn.disabled = true;
    btnText.style.display = 'inline';
    loader.style.display = 'none';
    resultsSection.style.display = 'none';
    document.querySelector('.upload-section').style.display = 'block';
    hideError();
    
    // Reset animations
    document.getElementById('scoreCircle').style.strokeDashoffset = 565;
    document.querySelectorAll('.progress-fill').forEach(bar => {
        bar.style.width = '0';
    });
});

// Error handling
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}
