"""
Configuration file for ATS Resume Checker
Contains email settings, thresholds, and other configuration parameters
"""

import os
from typing import Dict, List

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),  # Change to your email provider's SMTP server
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'sender_email': os.getenv('SENDER_EMAIL', 'associatedeveloper7@gmail.com'),  # Replace with your email
    'sender_password': os.getenv('SENDER_PASSWORD', 'vwbt fkrg ebtp wlsg'),  # Use app password for Gmail
    'sender_name': os.getenv('SENDER_NAME', 'ATS Resume Checker')
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

# Company-Specific Job Requirements and Keywords
COMPANY_JOB_REQUIREMENTS = {
    'software_engineer': {
        'required_keywords': [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'git',
            'api', 'database', 'agile', 'scrum', 'docker', 'aws', 'cloud'
        ],
        'preferred_keywords': [
            'machine learning', 'data structures', 'algorithms', 'testing',
            'microservices', 'kubernetes', 'ci/cd', 'devops'
        ],
        'minimum_experience': 2,  # years
        'required_education': ['bachelor', 'computer science', 'engineering'],
        'minimum_ats_score': 75
    },
    'data_scientist': {
        'required_keywords': [
            'python', 'r', 'sql', 'machine learning', 'statistics',
            'data analysis', 'pandas', 'numpy', 'scikit-learn'
        ],
        'preferred_keywords': [
            'deep learning', 'tensorflow', 'pytorch', 'matplotlib',
            'big data', 'hadoop', 'spark', 'tableau', 'power bi'
        ],
        'minimum_experience': 1,
        'required_education': ['bachelor', 'master', 'statistics', 'mathematics', 'computer science'],
        'minimum_ats_score': 70
    },
    'marketing_specialist': {
        'required_keywords': [
            'digital marketing', 'seo', 'social media', 'content marketing',
            'campaign management', 'brand management', 'market research'
        ],
        'preferred_keywords': [
            'google analytics', 'facebook ads', 'email marketing',
            'conversion optimization', 'a/b testing', 'roi analysis'
        ],
        'minimum_experience': 1,
        'required_education': ['bachelor', 'marketing', 'communications', 'business'],
        'minimum_ats_score': 65
    },
    'project_manager': {
        'required_keywords': [
            'project management', 'agile', 'scrum', 'stakeholder management',
            'budget management', 'team leadership', 'planning', 'execution'
        ],
        'preferred_keywords': [
            'pmp', 'kanban', 'risk management', 'deliverables',
            'communication', 'timeline management', 'prince2'
        ],
        'minimum_experience': 3,
        'required_education': ['bachelor', 'project management', 'business', 'engineering'],
        'minimum_ats_score': 70
    }
}

# Company Hiring Criteria Weights (should sum to 100)
COMPANY_HIRING_CRITERIA = {
    'ats_compatibility': 30,      # Resume format and ATS readability
    'keyword_relevance': 25,      # Job-specific keywords
    'experience_level': 20,       # Years of experience
    'education_background': 15,   # Educational qualifications
    'skills_match': 10           # Technical/soft skills alignment
}

# Keywords for different job categories (for backward compatibility)
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

# Company Configuration for Internal Recruitment
COMPANY_CONFIG = {
    'company_name': 'TalentHub',  # Company name
    'hr_email': 'careers@talenthub.com',  # HR email
    'company_website': 'https://www.talenthub.com',  # Company website
    'department': 'Human Resources',
    'company_logo_url': '',  # Optional: Add your company logo URL
    'recruitment_portal': 'https://careers.talenthub.com'  # Careers page
}

# Email template variables
EMAIL_TEMPLATE_VARS = {
    'company_name': COMPANY_CONFIG['company_name'],
    'support_email': COMPANY_CONFIG['hr_email'],
    'website_url': COMPANY_CONFIG['company_website']
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

def get_company_job_requirements(job_category: str) -> Dict:
    """Get company-specific job requirements for a category"""
    if job_category.lower() in COMPANY_JOB_REQUIREMENTS:
        return COMPANY_JOB_REQUIREMENTS[job_category.lower()]
    
    # Return default requirements for unknown categories
    return {
        'required_keywords': get_job_keywords(job_category),
        'preferred_keywords': [],
        'minimum_experience': 0,
        'required_education': ['bachelor'],
        'minimum_ats_score': 60
    }

def evaluate_company_hiring_criteria(resume_data: Dict, job_category: str) -> Dict:
    """Evaluate resume against company hiring criteria"""
    requirements = get_company_job_requirements(job_category)
    
    # Calculate individual scores
    ats_score = resume_data.get('ats_score', 0)
    
    # Keyword relevance score
    found_keywords = resume_data.get('found_keywords', [])
    required_keywords = requirements['required_keywords']
    preferred_keywords = requirements['preferred_keywords']
    
    required_found = len([k for k in required_keywords if k.lower() in [f.lower() for f in found_keywords]])
    preferred_found = len([k for k in preferred_keywords if k.lower() in [f.lower() for f in found_keywords]])
    
    keyword_score = 0
    if required_keywords:
        keyword_score = (required_found / len(required_keywords)) * 70
        if preferred_keywords:
            keyword_score += (preferred_found / len(preferred_keywords)) * 30
    
    # Experience level (simplified - would need better parsing)
    experience_score = 50  # Default, would need to parse resume for actual experience
    
    # Education background (simplified)
    education_score = 50  # Default, would need to parse resume for education
    
    # Skills match
    skills_score = keyword_score  # Simplified - use keyword score as proxy
    
    # Calculate weighted final score
    final_score = (
        (ats_score * COMPANY_HIRING_CRITERIA['ats_compatibility'] / 100) +
        (keyword_score * COMPANY_HIRING_CRITERIA['keyword_relevance'] / 100) +
        (experience_score * COMPANY_HIRING_CRITERIA['experience_level'] / 100) +
        (education_score * COMPANY_HIRING_CRITERIA['education_background'] / 100) +
        (skills_score * COMPANY_HIRING_CRITERIA['skills_match'] / 100)
    )
    
    # Determine if candidate passes company criteria
    passes_criteria = (
        ats_score >= requirements['minimum_ats_score'] and
        keyword_score >= 40 and  # At least 40% keyword match
        final_score >= 60  # Overall score threshold
    )
    
    return {
        'final_score': round(final_score, 1),
        'ats_compatibility': ats_score,
        'keyword_relevance': round(keyword_score, 1),
        'experience_level': experience_score,
        'education_background': education_score,
        'skills_match': round(skills_score, 1),
        'passes_criteria': passes_criteria,
        'required_keywords_found': required_found,
        'required_keywords_total': len(required_keywords),
        'preferred_keywords_found': preferred_found,
        'preferred_keywords_total': len(preferred_keywords),
        'minimum_ats_score': requirements['minimum_ats_score']
    }
