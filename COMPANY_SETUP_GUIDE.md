# Company CV Screening System Setup Guide

## Overview

This system has been customized for internal company recruitment. It automatically screens CVs against your company's specific criteria and sends professional emails to candidates with results.

## Key Features

✅ **Automated CV Screening**: Evaluates CVs against company-specific criteria
✅ **Professional Email Notifications**: Sends acceptance or rejection emails with detailed feedback
✅ **Customizable Job Requirements**: Configure keywords and criteria for different positions
✅ **Company Branding**: All emails and interface branded with your company details
✅ **Detailed Analytics**: Track and analyze CV submissions

## Setup Instructions

### 1. Company Configuration

Edit `config.py` and update the `COMPANY_CONFIG` section:

```python
COMPANY_CONFIG = {
    'company_name': 'Your Company Name Ltd.',  # Your actual company name
    'hr_email': 'hr@yourcompany.com',         # Your HR department email
    'company_website': 'https://www.yourcompany.com',  # Your company website
    'department': 'Human Resources',           # Department name
    'company_logo_url': '',                    # Optional: Company logo URL
    'recruitment_portal': 'https://careers.yourcompany.com'  # Your careers page
}
```

### 2. Email Configuration

Update the email settings in `config.py`:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Your email provider's SMTP server
    'smtp_port': 587,
    'sender_email': 'your-hr-email@company.com',  # HR email for sending notifications
    'sender_password': 'your-app-password',       # Email app password (not regular password)
    'sender_name': 'Your Company HR Team'
}
```

**Important**: For Gmail, use an App Password, not your regular password.

### 3. Job Requirements Configuration

Customize job requirements in `config.py` under `COMPANY_JOB_REQUIREMENTS`:

```python
COMPANY_JOB_REQUIREMENTS = {
    'software_engineer': {
        'required_keywords': [
            'python', 'java', 'javascript', 'react', 'sql', 'git'
            # Add your required technical skills
        ],
        'preferred_keywords': [
            'docker', 'aws', 'kubernetes', 'microservices'
            # Add nice-to-have skills
        ],
        'minimum_experience': 2,  # Years
        'required_education': ['bachelor', 'computer science', 'engineering'],
        'minimum_ats_score': 75  # Minimum ATS compatibility score
    },
    # Add more positions as needed
}
```

### 4. Hiring Criteria Weights

Adjust the importance of different criteria in `COMPANY_HIRING_CRITERIA`:

```python
COMPANY_HIRING_CRITERIA = {
    'ats_compatibility': 30,      # Resume format and ATS readability (30%)
    'keyword_relevance': 25,      # Job-specific keywords (25%)
    'experience_level': 20,       # Years of experience (20%)
    'education_background': 15,   # Educational qualifications (15%)
    'skills_match': 10           # Technical/soft skills alignment (10%)
}
```

## How It Works

### 1. CV Submission Process

1. Candidates visit your CV screening portal
2. They upload their CV and select job category
3. They optionally provide their email address
4. System automatically analyzes the CV

### 2. Evaluation Process

The system evaluates CVs based on:

- **ATS Compatibility** (30%): Format, readability, structure
- **Keyword Relevance** (25%): Match with required/preferred keywords
- **Experience Level** (20%): Years of relevant experience
- **Education Background** (15%): Educational qualifications
- **Skills Match** (10%): Technical and soft skills alignment

### 3. Email Notifications

#### Acceptance Emails (When CV Passes Screening)
- Congratulatory message with company branding
- Detailed score breakdown
- Clear next steps in hiring process
- Contact information for follow-up
- Company website and culture links

#### Rejection Emails (When CV Doesn't Meet Criteria)
- Professional and encouraging tone
- Specific feedback on areas for improvement
- Detailed score breakdown showing where they fell short
- Professional development tips
- Encouragement to reapply after improvement

### 4. Results Dashboard

Access `/dashboard` to view:
- Total CV submissions
- Pass/fail rates
- Common weak areas
- Analytics by job category

## Testing the System

### 1. Test Email Configuration
```bash
python test_company_recruitment.py
```

### 2. Test Complete System
1. Start the application: `python app.py`
2. Visit `http://localhost:5000`
3. Upload a test CV
4. Check email delivery and content

## Customization Options

### 1. Add New Job Categories

In `config.py`, add new entries to `COMPANY_JOB_REQUIREMENTS`:

```python
'marketing_manager': {
    'required_keywords': ['digital marketing', 'seo', 'social media'],
    'preferred_keywords': ['google analytics', 'facebook ads'],
    'minimum_experience': 3,
    'required_education': ['bachelor', 'marketing', 'business'],
    'minimum_ats_score': 70
}
```

### 2. Adjust Scoring Thresholds

Modify minimum scores in individual job requirements or global criteria weights.

### 3. Customize Email Templates

Edit `utils/company_email_sender.py` to modify:
- Email subject lines
- Message content and tone
- Company branding elements
- Additional information sections

### 4. Add Company Logo

Update `COMPANY_CONFIG['company_logo_url']` with your logo URL to include it in emails.

## Email Examples

### Acceptance Email Features:
- ✅ Professional company-branded header
- ✅ Congratulatory message with score breakdown
- ✅ Clear next steps (HR review, interview process)
- ✅ Timeline expectations
- ✅ Contact information
- ✅ Company culture links

### Rejection Email Features:
- ✅ Professional and respectful tone
- ✅ Specific feedback on areas needing improvement
- ✅ Score breakdown showing gaps
- ✅ Professional development suggestions
- ✅ Encouragement to reapply
- ✅ Links to open positions

## Security Considerations

1. **Email Credentials**: Use app passwords, not regular passwords
2. **File Uploads**: System automatically cleans up uploaded files
3. **Data Storage**: CV text and analysis results are logged for HR review
4. **Access Control**: Consider adding authentication for the dashboard

## Troubleshooting

### Email Issues
- Check SMTP settings and credentials
- Verify app password (for Gmail)
- Check spam/junk folders
- Test with `test_company_recruitment.py`

### CV Processing Issues
- Ensure file formats are supported (.pdf, .docx, .doc)
- Check file size limits (currently 10MB)
- Review error logs in console output

### Scoring Issues
- Review keyword lists for your job categories
- Adjust minimum score thresholds
- Check criteria weights in configuration

## Support

For technical support or customization requests, check:
1. Error logs in the console
2. Email delivery logs
3. Configuration settings
4. Test scripts output

---

**Ready to Deploy!** 

Once configured, your company CV screening system will:
- Automatically evaluate incoming CVs
- Send professional branded emails
- Maintain detailed records for HR review
- Provide analytics on recruitment effectiveness

Update the configurations and test thoroughly before going live with candidate submissions.
