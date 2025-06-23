"""
Flask Web Application for ATS Resume Checker
Enhanced with JSON logging and modern UI - No email functionality
"""

import os
import logging
import time
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import sys

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

try:
    from utils.parser import parse_resume
    from utils.ats_checker import check_ats, get_detailed_analysis
    from utils.json_logger import log_resume_submission, log_resume_analysis, get_dashboard_data
    from utils.intelligent_agent import IntelligentATSAgent
except ImportError:
    from parser import parse_resume
    from ats_checker import check_ats, get_detailed_analysis
    from json_logger import log_resume_submission, log_resume_analysis, get_dashboard_data
    from intelligent_agent import IntelligentATSAgent

from config import FILE_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'ats_resume_checker_secret_key_2025'
app.config['MAX_CONTENT_LENGTH'] = FILE_CONFIG['max_file_size']

# Initialize Intelligent ATS Agent
intelligent_agent = IntelligentATSAgent()

# Configure upload folder
UPLOAD_FOLDER = FILE_CONFIG['upload_folder']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in [ext.lstrip('.') for ext in FILE_CONFIG['allowed_extensions']]

def save_complete_analysis_to_json(filename, analysis_data):
    """Save complete analysis data to individual JSON file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = "data/individual_analyses"
        os.makedirs(data_dir, exist_ok=True)
        
        # Generate safe filename
        safe_filename = secure_filename(filename)
        timestamp = int(time.time())
        json_filename = f"{safe_filename}_{timestamp}.json"
        json_path = os.path.join(data_dir, json_filename)
        
        # Save analysis data
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(analysis_data, file, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Saved complete analysis to: {json_path}")
        
    except Exception as e:
        logger.error(f"Failed to save analysis to JSON: {str(e)}")

@app.route('/')
def index():
    """Main upload page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis with JSON logging"""
    start_time = time.time()
    
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        
        # Check if file was actually selected
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            flash(f'File type not allowed. Please upload: {", ".join(FILE_CONFIG["allowed_extensions"])}', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Calculate file size
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        
        # Get optional parameters
        job_category = request.form.get('job_category', 'general')
        user_email = request.form.get('email', '').strip()
        
        logger.info(f"Processing uploaded file: {filename} ({file_size_mb:.2f} MB)")
        
        # Parse resume
        resume_text, extracted_email, user_name = parse_resume(file_path)
        
        if not resume_text:
            flash('Could not extract text from the resume. Please check the file format.', 'error')
            os.remove(file_path)  # Clean up
            
            # Log failed submission
            log_resume_submission(
                filename=filename,
                user_name=user_name or "Unknown",
                user_email=user_email or extracted_email or "",
                job_category=job_category,
                file_size_mb=file_size_mb,
                ats_score=0,
                passed_ats=False,
                status="failed_parsing"
            )
            
            return redirect(url_for('index'))
        
        # Use provided email or extracted email
        final_email = user_email if user_email else extracted_email
          # Perform ATS analysis
        ats_score = check_ats(resume_text)
        detailed_analysis = get_detailed_analysis(resume_text, job_category)
        
        # Use Intelligent Agent for enhanced analysis
        agent_analysis = intelligent_agent.generate_smart_recommendations(resume_text)
        
        # Merge traditional analysis with agent analysis
        enhanced_analysis = {
            **detailed_analysis,
            'intelligent_agent': agent_analysis,
            'detected_category': agent_analysis.get('detected_category', job_category),
            'agent_recommendations': agent_analysis.get('recommendations', [])
        }
        
        # Determine if resume passed ATS check
        passed_ats = ats_score >= 75
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Log submission to JSON
        log_resume_submission(
            filename=filename,
            user_name=user_name or "",
            user_email=final_email or "",
            job_category=job_category,
            file_size_mb=file_size_mb,
            ats_score=ats_score,
            passed_ats=passed_ats,
            status="completed"
        )
          # Log detailed analysis to JSON
        log_resume_analysis(
            filename=filename,
            user_name=user_name or "",
            ats_score=ats_score,
            job_category=job_category,
            detailed_analysis=enhanced_analysis,
            processing_time=processing_time
        )
          # Save complete analysis to individual JSON file
        save_complete_analysis_to_json(filename, {
            'filename': filename,
            'user_name': user_name,
            'user_email': final_email,
            'job_category': job_category,
            'file_size_mb': round(file_size_mb, 2),
            'resume_text': resume_text,
            'ats_score': ats_score,
            'passed_ats': passed_ats,
            'detailed_analysis': enhanced_analysis,
            'processing_time': round(processing_time, 2),
            'timestamp': time.time()
        })
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass        # Prepare results for template
        results = {
            'filename': filename,
            'user_name': user_name,
            'ats_score': ats_score,
            'detailed_analysis': enhanced_analysis,
            'job_category': job_category,
            'passed_ats': passed_ats,
            'processing_time': round(processing_time, 2),
            'file_size_mb': round(file_size_mb, 2)
        }
        
        return render_template('results_new.html', **results)
        
    except RequestEntityTooLarge:
        flash(f'File too large. Maximum size allowed: {FILE_CONFIG["max_file_size"] // (1024*1024)}MB', 'error')
        return redirect(url_for('index'))
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        
        # Log failed submission if we have basic info
        try:
            filename = request.files.get('file', type('MockFile', (), {'filename': 'unknown'})).filename
            job_category = request.form.get('job_category', 'general')
            user_email = request.form.get('email', '').strip()
            
            log_resume_submission(
                filename=filename or "unknown",
                user_name="",
                user_email=user_email,
                job_category=job_category,
                file_size_mb=0,
                ats_score=0,
                passed_ats=False,
                status="error"
            )
        except:
            pass
            
        flash(f'An error occurred while processing your resume: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """API endpoint for file upload and text extraction"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save and parse file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Parse resume
        resume_text, word_count, format_issues = parse_resume(file_path)
        
        # Clean up file
        try:
            os.remove(file_path)
        except:
            pass
        
        if not resume_text:
            return jsonify({'error': 'Could not extract text from resume'}), 400
        
        return jsonify({
            'success': True,
            'resume_text': resume_text,
            'word_count': word_count,
            'format_issues': format_issues,
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"API upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Admin dashboard showing analytics"""
    try:
        dashboard_data = get_dashboard_data()
        return render_template('dashboard.html', data=dashboard_data)
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        flash('Unable to load dashboard data', 'error')
        return redirect(url_for('index'))

@app.route('/agent-test')
def agent_test():
    """Test page for the intelligent agent"""
    return render_template('agent_test.html')

@app.route('/compare-job', methods=['POST'])
def compare_with_job():
    """Compare resume with job posting using intelligent agent"""
    try:
        if 'file' not in request.files or 'job_description' not in request.form:
            return jsonify({'error': 'Missing file or job description'}), 400
        
        file = request.files['file']
        job_description = request.form.get('job_description', '').strip()
        
        if file.filename == '' or not job_description:
            return jsonify({'error': 'File and job description are required'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save and parse file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Parse resume
        resume_text, _, _ = parse_resume(file_path)
        
        # Clean up file
        try:
            os.remove(file_path)
        except:
            pass
        
        if not resume_text:
            return jsonify({'error': 'Could not extract text from resume'}), 400
        
        # Use intelligent agent for job comparison
        analysis = intelligent_agent.generate_smart_recommendations(resume_text, job_description)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'filename': filename
        })
        
    except Exception as e:
        logger.error(f"Job comparison error: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/agent-analyze', methods=['POST'])
def api_agent_analyze():
    """API endpoint for intelligent agent analysis"""
    try:
        data = request.get_json()
        if not data or 'resume_text' not in data:
            return jsonify({'error': 'Resume text is required'}), 400
        
        resume_text = data['resume_text']
        job_description = data.get('job_description', None)
        
        # Perform intelligent analysis
        analysis = intelligent_agent.generate_smart_recommendations(resume_text, job_description)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"API agent analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    flash(f'File too large. Maximum size: {FILE_CONFIG["max_file_size"] // (1024*1024)}MB', 'error')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {str(e)}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("Starting ATS Resume Checker Web Application...")
    print("=" * 50)
    print("Features:")
    print("- Resume upload and analysis")
    print("- ATS compatibility scoring")
    print("- Detailed feedback and recommendations")
    print("- Email notifications")
    print("- Multiple job categories")
    print("=" * 50)
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
