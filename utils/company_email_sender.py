"""
Company Recruitment Email Sender
Sends professional recruitment emails for internal hiring process
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys
from typing import Optional, Dict, Any

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from config import get_email_config, COMPANY_CONFIG
except ImportError:
    # Fallback configuration
    COMPANY_CONFIG = {
        'company_name': 'Your Company',
        'hr_email': 'hr@yourcompany.com',
        'company_website': 'https://www.yourcompany.com',
        'department': 'Human Resources',
        'recruitment_portal': 'https://careers.yourcompany.com'
    }

logger = logging.getLogger(__name__)

class CompanyRecruitmentEmailSender:
    """Company recruitment email sender for CV screening process"""
    
    def __init__(self):
        """Initialize email sender with configuration"""
        try:
            self.config = get_email_config()
        except:
            # Fallback configuration
            self.config = {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'sender_email': 'associatedeveloper7@gmail.com',
                'sender_password': 'zeeshan49418249',
                'sender_name': f"{COMPANY_CONFIG['company_name']} HR Team"
            }
    
    def create_acceptance_email(self, candidate_name: str, candidate_email: str, 
                              position: str, company_scores: Dict[str, Any]) -> MIMEMultipart:
        """Create acceptance email for candidates who pass screening"""
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.config['sender_name']} <{self.config['sender_email']}>"
        msg['To'] = candidate_email
        msg['Subject'] = f"🎉 Congratulations! Your Application for {position.title()} Position - Next Steps"
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 700px; margin: 0 auto; background: #ffffff; }}
                .header {{ background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%); color: white; padding: 40px 30px; text-align: center; }}
                .logo {{ font-size: 2rem; font-weight: bold; margin-bottom: 10px; }}
                .content {{ padding: 40px 30px; }}
                .score-section {{ background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 25px 0; border-left: 5px solid #28a745; }}
                .score-item {{ display: flex; justify-content: space-between; margin: 10px 0; }}
                .score-label {{ font-weight: 600; color: #495057; }}
                .score-value {{ font-weight: bold; color: #28a745; }}
                .next-steps {{ background: #e8f5e8; padding: 25px; border-radius: 10px; margin: 25px 0; }}
                .step {{ margin: 15px 0; padding: 10px 0; border-bottom: 1px solid #d4edda; }}
                .step:last-child {{ border-bottom: none; }}
                .cta-section {{ text-align: center; margin: 30px 0; }}
                .cta-button {{ background: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block; }}
                .footer {{ background: #f8f9fa; padding: 30px; text-align: center; color: #6c757d; border-top: 1px solid #dee2e6; }}
                .contact-info {{ margin: 20px 0; padding: 20px; background: #fff3cd; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">{COMPANY_CONFIG['company_name']}</div>
                    <h1>🎉 Application Approved!</h1>
                    <p>Your CV has successfully passed our initial screening</p>
                </div>
                
                <div class="content">
                    <h2>Dear {candidate_name},</h2>
                    
                    <p>Congratulations! We are pleased to inform you that your application for the <strong>{position.title()}</strong> position at <strong>{COMPANY_CONFIG['company_name']}</strong> has successfully passed our automated CV screening process.</p>
                    
                    <div class="score-section">
                        <h3>📊 Your Screening Results</h3>
                        <div class="score-item">
                            <span class="score-label">Overall Score:</span>
                            <span class="score-value">{company_scores['final_score']}/100</span>
                        </div>
                        <div class="score-item">
                            <span class="score-label">ATS Compatibility:</span>
                            <span class="score-value">{company_scores['ats_compatibility']}/100</span>
                        </div>
                        <div class="score-item">
                            <span class="score-label">Keyword Relevance:</span>
                            <span class="score-value">{company_scores['keyword_relevance']}/100</span>
                        </div>
                        <div class="score-item">
                            <span class="score-label">Required Keywords Found:</span>
                            <span class="score-value">{company_scores['required_keywords_found']}/{company_scores['required_keywords_total']}</span>
                        </div>
                        <div class="score-item">
                            <span class="score-label">Status:</span>
                            <span class="score-value">✅ QUALIFIED</span>
                        </div>
                    </div>
                    
                    <div class="next-steps">
                        <h3>🚀 Next Steps in Our Hiring Process</h3>
                        <div class="step">
                            <strong>1. HR Review (1-2 business days)</strong><br>
                            Our HR team will conduct a detailed review of your application.
                        </div>
                        <div class="step">
                            <strong>2. Initial Interview Invitation</strong><br>
                            If selected, you'll receive an interview invitation within 3-5 business days.
                        </div>
                        <div class="step">
                            <strong>3. Technical/Behavioral Assessment</strong><br>
                            Position-specific evaluation based on the role requirements.
                        </div>
                        <div class="step">
                            <strong>4. Final Decision</strong><br>
                            We'll notify you of the final decision within 1-2 weeks.
                        </div>
                    </div>
                    
                    <div class="contact-info">
                        <h3>📞 Contact Information</h3>
                        <p>If you have any questions about your application or our process, please don't hesitate to contact us:</p>
                        <p><strong>HR Department:</strong> {COMPANY_CONFIG['hr_email']}<br>
                        <strong>Company Website:</strong> {COMPANY_CONFIG['company_website']}</p>
                    </div>
                    
                    <div class="cta-section">
                        <p>While you wait, feel free to learn more about our company and culture:</p>
                        <a href="{COMPANY_CONFIG['company_website']}" class="cta-button">Visit Our Website</a>
                    </div>
                    
                    <p>Thank you for your interest in joining our team. We look forward to potentially working with you!</p>
                    
                    <p>Best regards,<br>
                    <strong>{COMPANY_CONFIG['department']}</strong><br>
                    {COMPANY_CONFIG['company_name']}</p>
                </div>
                
                <div class="footer">
                    <p>This is an automated message from {COMPANY_CONFIG['company_name']} recruitment system.</p>
                    <p>Please do not reply to this email. For inquiries, contact {COMPANY_CONFIG['hr_email']}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_content = f"""
Dear {candidate_name},

Congratulations! Your application for the {position.title()} position at {COMPANY_CONFIG['company_name']} has successfully passed our automated CV screening process.

Your Screening Results:
- Overall Score: {company_scores['final_score']}/100
- ATS Compatibility: {company_scores['ats_compatibility']}/100
- Keyword Relevance: {company_scores['keyword_relevance']}/100
- Required Keywords Found: {company_scores['required_keywords_found']}/{company_scores['required_keywords_total']}
- Status: ✅ QUALIFIED

Next Steps:
1. HR Review (1-2 business days)
2. Initial Interview Invitation (3-5 business days if selected)
3. Technical/Behavioral Assessment
4. Final Decision (1-2 weeks)

Contact Information:
HR Department: {COMPANY_CONFIG['hr_email']}
Company Website: {COMPANY_CONFIG['company_website']}

Thank you for your interest in joining our team!

Best regards,
{COMPANY_CONFIG['department']}
{COMPANY_CONFIG['company_name']}
        """
        
        # Attach both versions
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        return msg
    
    def create_rejection_email(self, candidate_name: str, candidate_email: str, 
                             position: str, company_scores: Dict[str, Any],
                             feedback_areas: list) -> MIMEMultipart:
        """Create rejection email with constructive feedback"""
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.config['sender_name']} <{self.config['sender_email']}>"
        msg['To'] = candidate_email
        msg['Subject'] = f"Application Update for {position.title()} Position at {COMPANY_CONFIG['company_name']}"
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 700px; margin: 0 auto; background: #ffffff; }}
                .header {{ background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; padding: 40px 30px; text-align: center; }}
                .logo {{ font-size: 2rem; font-weight: bold; margin-bottom: 10px; }}
                .content {{ padding: 40px 30px; }}
                .score-section {{ background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 25px 0; border-left: 5px solid #dc3545; }}
                .score-item {{ display: flex; justify-content: space-between; margin: 10px 0; }}
                .score-label {{ font-weight: 600; color: #495057; }}
                .score-value {{ font-weight: bold; color: #dc3545; }}
                .feedback-section {{ background: #fff3cd; padding: 25px; border-radius: 10px; margin: 25px 0; border-left: 5px solid #ffc107; }}
                .feedback-item {{ margin: 15px 0; padding: 15px; background: white; border-radius: 8px; border-left: 3px solid #ffc107; }}
                .improvement-tips {{ background: #e8f4fd; padding: 25px; border-radius: 10px; margin: 25px 0; }}
                .tip {{ margin: 10px 0; padding: 10px; background: white; border-radius: 5px; }}
                .cta-section {{ text-align: center; margin: 30px 0; }}
                .cta-button {{ background: #007bff; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block; }}
                .footer {{ background: #f8f9fa; padding: 30px; text-align: center; color: #6c757d; border-top: 1px solid #dee2e6; }}
                .encouragement {{ background: #d1ecf1; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">{COMPANY_CONFIG['company_name']}</div>
                    <h1>Application Update</h1>
                    <p>Thank you for your interest in our {position.title()} position</p>
                </div>
                
                <div class="content">
                    <h2>Dear {candidate_name},</h2>
                    
                    <p>Thank you for submitting your application for the <strong>{position.title()}</strong> position at <strong>{COMPANY_CONFIG['company_name']}</strong>. We appreciate the time and effort you put into your application.</p>
                    
                    <p>After careful review of your CV through our automated screening process, we have decided not to move forward with your application at this time. However, we believe in providing constructive feedback to help you in your career journey.</p>
                    
                    <div class="score-section">
                        <h3>📊 Your Application Assessment</h3>
                        <div class="score-item">
                            <span class="score-label">Overall Score:</span>
                            <span class="score-value">{company_scores['final_score']}/100</span>
                        </div>
                        <div class="score-item">
                            <span class="score-label">Required Score:</span>
                            <span class="score-value">60/100</span>
                        </div>
                        <div class="score-item">
                            <span class="score-label">ATS Compatibility:</span>
                            <span class="score-value">{company_scores['ats_compatibility']}/100</span>
                        </div>
                        <div class="score-item">
                            <span class="score-label">Keyword Relevance:</span>
                            <span class="score-value">{company_scores['keyword_relevance']}/100</span>
                        </div>
                        <div class="score-item">
                            <span class="score-label">Required Keywords Found:</span>
                            <span class="score-value">{company_scores['required_keywords_found']}/{company_scores['required_keywords_total']}</span>
                        </div>
                    </div>
                    
                    <div class="feedback-section">
                        <h3>💡 Areas for Improvement</h3>
                        <p>Based on our assessment, here are specific areas where you can strengthen your CV:</p>
        """
        
        # Add feedback areas
        for area in feedback_areas:
            html_content += f'<div class="feedback-item">• {area}</div>'
        
        html_content += f"""
                    </div>
                    
                    <div class="improvement-tips">
                        <h3>🚀 Professional Development Tips</h3>
                        <div class="tip">✅ <strong>Keyword Optimization:</strong> Research job descriptions in your field and incorporate relevant industry keywords into your CV.</div>
                        <div class="tip">✅ <strong>Format Enhancement:</strong> Use a clean, ATS-friendly format with clear section headings and bullet points.</div>
                        <div class="tip">✅ <strong>Skills Development:</strong> Consider gaining experience in the technologies and skills most relevant to your target role.</div>
                        <div class="tip">✅ <strong>Quantify Achievements:</strong> Include specific metrics and results in your experience descriptions.</div>
                        <div class="tip">✅ <strong>Professional Summary:</strong> Add a compelling summary that highlights your key qualifications and career goals.</div>
                    </div>
                    
                    <div class="encouragement">
                        <h3>🌟 We Encourage You to Apply Again</h3>
                        <p>We believe in continuous improvement and would welcome a future application from you. Please consider reapplying once you've addressed the feedback areas above.</p>
                    </div>
                    
                    <div class="cta-section">
                        <p>Stay connected with us for future opportunities:</p>
                        <a href="{COMPANY_CONFIG['recruitment_portal']}" class="cta-button">View Open Positions</a>
                    </div>
                    
                    <p>We wish you the best of luck in your career endeavors and hope to see an improved application from you in the future.</p>
                    
                    <p>Best regards,<br>
                    <strong>{COMPANY_CONFIG['department']}</strong><br>
                    {COMPANY_CONFIG['company_name']}</p>
                </div>
                
                <div class="footer">
                    <p>This is an automated message from {COMPANY_CONFIG['company_name']} recruitment system.</p>
                    <p>For inquiries about this decision, contact {COMPANY_CONFIG['hr_email']}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_content = f"""
Dear {candidate_name},

Thank you for submitting your application for the {position.title()} position at {COMPANY_CONFIG['company_name']}.

After careful review, we have decided not to move forward with your application at this time. However, we want to provide constructive feedback:

Your Application Assessment:
- Overall Score: {company_scores['final_score']}/100 (Required: 60/100)
- ATS Compatibility: {company_scores['ats_compatibility']}/100
- Keyword Relevance: {company_scores['keyword_relevance']}/100
- Required Keywords Found: {company_scores['required_keywords_found']}/{company_scores['required_keywords_total']}

Areas for Improvement:
"""
        
        for area in feedback_areas:
            text_content += f"• {area}\n"
        
        text_content += f"""
Professional Development Tips:
✅ Research and incorporate relevant industry keywords
✅ Use a clean, ATS-friendly CV format
✅ Develop skills relevant to your target role
✅ Quantify your achievements with specific metrics
✅ Add a compelling professional summary

We encourage you to apply again once you've addressed these areas.

Best regards,
{COMPANY_CONFIG['department']}
{COMPANY_CONFIG['company_name']}

Contact: {COMPANY_CONFIG['hr_email']}
Careers: {COMPANY_CONFIG['recruitment_portal']}
        """
        
        # Attach both versions
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        return msg
    
    def send_email(self, msg: MIMEMultipart) -> bool:
        """Send email using SMTP"""
        try:
            # Create SMTP session
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()  # Enable TLS encryption
            
            # Login and send email
            server.login(self.config['sender_email'], self.config['sender_password'])
            
            sender_email = self.config['sender_email']
            recipient_email = msg['To']
            
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            
            logger.info(f"Recruitment email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send recruitment email: {str(e)}")
            return False
    
    def send_recruitment_decision(self, candidate_name: str, candidate_email: str,
                                position: str, company_scores: Dict[str, Any],
                                passed_screening: bool, feedback_areas: list = None) -> bool:
        """Send recruitment decision email"""
        
        if not candidate_email or '@' not in candidate_email:
            logger.warning("Invalid email address provided")
            return False
        
        try:
            if passed_screening:
                msg = self.create_acceptance_email(
                    candidate_name, candidate_email, position, company_scores
                )
                logger.info(f"Sending acceptance email to {candidate_email}")
            else:
                feedback_areas = feedback_areas or [
                    "CV format needs improvement for ATS compatibility",
                    "Missing key skills/keywords for the position",
                    "Professional experience could be better highlighted"
                ]
                msg = self.create_rejection_email(
                    candidate_name, candidate_email, position, company_scores, feedback_areas
                )
                logger.info(f"Sending rejection email with feedback to {candidate_email}")
            
            return self.send_email(msg)
            
        except Exception as e:
            logger.error(f"Error creating/sending recruitment email: {str(e)}")
            return False

# Create global recruitment email sender instance
recruitment_email_sender = CompanyRecruitmentEmailSender()

def send_recruitment_notification(candidate_name: str, candidate_email: str, position: str,
                                company_scores: Dict[str, Any], passed_screening: bool,
                                feedback_areas: list = None) -> bool:
    """Convenience function to send recruitment notification email"""
    return recruitment_email_sender.send_recruitment_decision(
        candidate_name, candidate_email, position, company_scores, passed_screening, feedback_areas
    )
