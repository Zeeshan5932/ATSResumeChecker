"""
Configuration file for ATS Resume Checker
Contains email settings, thresholds, and other configuration parameters
"""

import os
from typing import Dict, List

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Change to your email provider's SMTP server
    'smtp_port': 587,
    'sender_email': 'associatedeveloper7@gmail.com',  # Replace with your email
    'sender_password': 'zeeshan49418249',  # Use app password for Gmail
    'sender_name': 'ATS Resume Checker'
}

# Simple email configuration variables (for backward compatibility)
EMAIL_SENDER = EMAIL_CONFIG['sender_email']
EMAIL_PASSWORD = EMAIL_CONFIG['sender_password']
SMTP_SERVER = EMAIL_CONFIG['smtp_server']
SMTP_PORT = EMAIL_CONFIG['smtp_port']

# ATS Scoring Thresholds
ATS_THRESHOLDS = {
    'excellent': 85,
    'good': 70,
    'average': 55,
    'poor': 40
}

# File Configuration
FILE_CONFIG = {
    'max_file_size': 10 * 1024 * 1024,  # 10MB in bytes
    'allowed_extensions': ['.pdf', '.docx', '.doc'],
    'upload_folder': 'resumes/uploaded_resumes'
}

# ATS Criteria Weights (should sum to 100)
ATS_CRITERIA_WEIGHTS = {
    'format_compatibility': 25,
    'keyword_matching': 30,
    'readability': 20,
    'structure_organization': 15,
    'contact_information': 10
}

# Keywords for different job categories
JOB_KEYWORDS = {
    'software_engineer': [
        'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'git',
        'api', 'database', 'agile', 'scrum', 'docker', 'aws', 'cloud',
        'machine learning', 'data structures', 'algorithms', 'testing'
    ],
    'data_scientist': [
        'python', 'r', 'sql', 'machine learning', 'deep learning', 'tensorflow',
        'pytorch', 'pandas', 'numpy', 'matplotlib', 'scikit-learn', 'statistics',
        'data analysis', 'data visualization', 'big data', 'hadoop', 'spark'
    ],
    'marketing': [
        'digital marketing', 'seo', 'sem', 'social media', 'content marketing',
        'google analytics', 'facebook ads', 'email marketing', 'campaign management',
        'brand management', 'market research', 'roi', 'conversion optimization'
    ],
    'project_manager': [
        'project management', 'agile', 'scrum', 'kanban', 'pmp', 'risk management',
        'stakeholder management', 'budget management', 'timeline', 'deliverables',
        'team leadership', 'communication', 'planning', 'execution'
    ]
}

# Common ATS-friendly formatting rules
ATS_FORMATTING_RULES = {
    'avoid_headers_footers': True,
    'avoid_images': True,
    'avoid_tables': True,
    'avoid_text_boxes': True,
    'use_standard_fonts': ['Arial', 'Calibri', 'Times New Roman', 'Helvetica'],
    'max_font_size': 12,
    'min_font_size': 10,
    'use_bullet_points': True,
    'clear_section_headers': True
}

# Email template variables
EMAIL_TEMPLATE_VARS = {
    'company_name': 'ATS Resume Checker',
    'support_email': 'support@atsresumechecker.com',
    'website_url': 'https://www.atsresumechecker.com'
}

def get_email_config() -> Dict:
    """Get email configuration with environment variable override"""
    config = EMAIL_CONFIG.copy()
    
    # Override with environment variables if available
    config['sender_email'] = os.getenv('SENDER_EMAIL', config['sender_email'])
    config['sender_password'] = os.getenv('SENDER_PASSWORD', config['sender_password'])
    config['smtp_server'] = os.getenv('SMTP_SERVER', config['smtp_server'])
    config['smtp_port'] = int(os.getenv('SMTP_PORT', str(config['smtp_port'])))
    
    return config

def get_job_keywords(job_category: str = 'general') -> List[str]:
    """Get keywords for a specific job category"""
    if job_category.lower() in JOB_KEYWORDS:
        return JOB_KEYWORDS[job_category.lower()]
    
    # Return a general set of keywords if category not found
    general_keywords = [
        'experience', 'skills', 'education', 'leadership', 'team', 'project',
        'management', 'communication', 'problem solving', 'analytical',
        'creative', 'innovative', 'results', 'achievements', 'professional'
    ]
    return general_keywords
