# 🎯 ATS Resume Checker

A comprehensive web application that analyzes resumes for ATS (Applicant Tracking System) compatibility, providing detailed feedback and recommendations to job seekers.

## ✨ Features

### Core Functionality
- **🔍 ATS Compatibility Analysis**: Comprehensive scoring based on format, keywords, structure, and readability
- **📊 Detailed Scoring**: Category-wise analysis with specific recommendations
- **📧 Automated Email Notifications**: 
  - Congratulations emails for ATS-compatible resumes
  - Improvement suggestions for resumes needing work
- **📈 CSV Logging**: Automatic logging of all submissions for analytics
- **📱 Modern Responsive UI**: Beautiful, mobile-friendly interface
- **🎯 Job Category Targeting**: Specialized analysis for different job categories

### Advanced Features
- **📊 Admin Dashboard**: Analytics and statistics for submissions
- **🔗 REST API**: Programmatic access for integrations
- **📄 Multi-format Support**: PDF, DOC, DOCX file processing
- **🎨 Professional Templates**: Modern, responsive email templates
- **📈 Performance Tracking**: Processing time and success rate monitoring
- **🔐 Error Handling**: Comprehensive error handling and logging

## 🚀 Quick Start

### 1. Setup
```bash
# Clone or download the project
cd ATSResumeChecker

# Run the setup script (recommended)
python setup.py

# Or manual installation:
pip install -r requirements.txt
```

### 2. Configuration
Update the email settings in `config.py` or create a `.env` file:
```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 3. Run the Application
```bash
# Start the server
python app.py

# Or use the startup scripts
# Windows: start_ats_checker.bat
# Unix/Linux: ./start_ats_checker.sh
```

### 4. Access the Application
Open your browser and go to: `http://localhost:5000`

## 🏗️ Project Structure

```
ATSResumeChecker/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── setup.py              # Setup and installation script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # HTML templates
│   ├── index.html       # Main upload page
│   ├── results.html     # Analysis results page
│   ├── dashboard.html   # Admin dashboard
│   ├── 404.html         # Error page
│   └── 500.html         # Server error page
├── utils/               # Utility modules
│   ├── __init__.py
│   ├── parser.py        # Resume text extraction
│   ├── ats_checker.py   # ATS analysis logic
│   ├── email_sender.py  # Email functionality
│   └── csv_logger.py    # CSV logging system
├── resumes/             # Resume storage
│   └── uploaded_resumes/
├── logs/                # Application logs and CSV data
└── static/              # Static files (if any)
```

## 🔧 Configuration

### Email Settings
For Gmail (recommended):
1. Enable 2-factor authentication
2. Generate an App Password
3. Update `config.py` with your credentials

### File Upload Settings
- **Maximum file size**: 10MB (configurable)
- **Supported formats**: PDF, DOC, DOCX
- **Upload folder**: `resumes/uploaded_resumes/`

### ATS Scoring Thresholds
- **Pass threshold**: 75% (configurable)
- **Excellent threshold**: 85%
- **Category weights**: Customizable in `config.py`

## 📊 Scoring Categories

### 1. Format Compatibility (25%)
- Font type and size
- Document structure
- ATS-friendly formatting
- Avoid images, tables, headers/footers

### 2. Keyword Matching (30%)
- Industry-specific keywords
- Job category relevance
- Skill mentions
- Experience terms

### 3. Readability (20%)
- Text clarity and flow
- Sentence structure
- Professional language
- Grammar and spelling

### 4. Structure & Organization (15%)
- Clear section headers
- Logical flow
- Consistent formatting
- Professional layout

### 5. Contact Information (10%)
- Complete contact details
- Professional email
- Phone number format
- Location information

## 🎯 Supported Job Categories

- **General**: Default analysis
- **Software Engineer**: Tech-focused keywords
- **Data Scientist**: Data and analytics terms
- **Marketing**: Marketing and digital terms
- **Project Manager**: Management and leadership terms

## 📧 Email Features

### Congratulations Email (ATS Score ≥ 75%)
- Professional congratulations message
- ATS compatibility confirmation
- Next steps guidance
- Encouragement for job applications

### Improvement Email (ATS Score < 75%)
- Specific improvement suggestions
- Category-wise feedback
- Actionable recommendations
- Encouragement to resubmit

## 📈 Analytics & Logging

### CSV Logging
- **Submissions Log**: All upload attempts with metadata
- **Analysis Log**: Detailed scoring breakdown
- **Automatic Export**: Excel and CSV export options

### Dashboard Metrics
- Total submissions and pass rates
- Average scores and trends
- Popular job categories
- Recent activity tracking

## 🔌 API Endpoints

### POST `/api/upload`
Programmatic resume analysis
```json
{
  "file": "resume.pdf",
  "job_category": "software_engineer"
}
```

### GET `/dashboard`
Analytics dashboard for administrators

## 🛠️ Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

### Adding New Job Categories
1. Update `JOB_KEYWORDS` in `config.py`
2. Add category to the dropdown in `index.html`
3. Update analysis logic if needed

### Customizing Email Templates
- Edit templates in `utils/email_sender.py`
- Use HTML for rich formatting
- Include dynamic variables

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- 2GB RAM minimum
- Internet connection (for email features)

### Python Packages
See `requirements.txt` for complete list:
- Flask 2.3.3
- pandas ≥1.5.0
- numpy ≥1.21.0
- scikit-learn ≥1.2.0
- PyPDF2 3.0.1
- python-docx 0.8.11
- nltk 3.8.1
- textstat 0.7.3

## 🔒 Security Considerations

### Email Security
- Use app passwords, not regular passwords
- Store credentials in environment variables
- Consider using OAuth2 for production

### File Upload Security
- File type validation
- Size limitations
- Temporary file cleanup
- Secure filename handling

## 🚀 Deployment

### Production Deployment
1. Use environment variables for configuration
2. Set up proper logging
3. Use a production WSGI server (Gunicorn)
4. Implement proper error handling
5. Set up monitoring and backups

### Environment Variables
```env
FLASK_ENV=production
SECRET_KEY=your_secret_key
SENDER_EMAIL=your_production_email
SENDER_PASSWORD=your_app_password
```

## 🧪 Testing

### Manual Testing
1. Upload various resume formats
2. Test different job categories
3. Verify email functionality
4. Check analytics dashboard

### Automated Testing
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests (when available)
pytest tests/
```

## 🐛 Troubleshooting

### Common Issues

**Email not sending:**
- Check email credentials
- Verify app password for Gmail
- Check SMTP settings
- Test with `/test-email` endpoint

**File upload errors:**
- Check file size (max 10MB)
- Verify file format (PDF, DOC, DOCX)
- Ensure upload directory exists

**Import errors:**
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)
- Try running `setup.py`

### Logs and Debugging
- Check `logs/` directory for error logs
- Enable debug mode for development
- Use browser developer tools for frontend issues

## 📜 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the configuration guide

## 🎯 Future Enhancements

- [ ] Database integration for persistence
- [ ] User authentication and profiles
- [ ] Resume template recommendations
- [ ] Batch processing capabilities
- [ ] Integration with job boards
- [ ] Advanced analytics and reporting
- [ ] Mobile app development
- [ ] AI-powered improvement suggestions

---

**Made with ❤️ for job seekers everywhere**
