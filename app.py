import os
import uuid
from flask import Flask, request, render_template, redirect, url_for, session, flash, send_file
from werkzeug.utils import secure_filename
import json
from utils.pdf_processor import extract_text_from_pdf, create_enhanced_resume
from utils.gemini_client import analyze_resume
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['resume']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(filepath)
        
        # Analyze resume using Gemini API
        try:
            analysis = analyze_resume(resume_text)
            
            # Store results in session
            session['analysis'] = analysis
            session['original_filename'] = filename
            session['filepath'] = filepath
            
            return redirect(url_for('results'))
        except Exception as e:
            flash(f'Error analyzing resume: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Only PDF files are allowed')
        return redirect(url_for('index'))

@app.route('/results')
def results():
    if 'analysis' not in session:
        flash('Please upload a resume first')
        return redirect(url_for('index'))
    
    return render_template('results.html', 
                          analysis=session['analysis'],
                          filename=session['original_filename'])

@app.route('/download')
def download():
    if 'analysis' not in session or 'filepath' not in session:
        flash('Please upload a resume first')
        return redirect(url_for('index'))
    
    # Create enhanced resume
    enhanced_filename = f"enhanced_{session['original_filename']}"
    enhanced_filepath = os.path.join(app.config['UPLOAD_FOLDER'], enhanced_filename)
    
    create_enhanced_resume(session['analysis'], enhanced_filepath)
    
    return send_file(enhanced_filepath, as_attachment=True, download_name=enhanced_filename)

@app.errorhandler(413)
def too_large(e):
    flash('File size exceeds the limit (16MB)')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
