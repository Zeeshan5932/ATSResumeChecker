import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional
import os
from config import get_email_config, EMAIL_TEMPLATE_VARS, EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Simple Function (as requested) ===

def send_congrats_email(name, recipient):
    """Simple congratulations email function"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "🎉 Congratulations on Your Resume!"
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 30px 20px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .content {{ padding: 30px; }}
                .success-badge {{ background: #10b981; color: white; padding: 15px; border-radius: 50px; text-align: center; margin: 20px 0; font-weight: bold; }}
                .highlight {{ background: #f0fdf4; border-left: 4px solid #10b981; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 14px; }}
                .btn {{ display: inline-block; background: #10b981; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Congratulations!</h1>
                    <p>Your Resume is ATS-Compatible</p>
                </div>
                <div class="content">
                    <p>Hi <strong>{name}</strong>,</p>
                    
                    <div class="success-badge">
                        ✅ ATS COMPATIBLE
                    </div>
                    
                    <p>Excellent news! Your resume has successfully passed our ATS (Applicant Tracking System) compatibility check.</p>
                    
                    <div class="highlight">
                        <h3>🎯 What this means for you:</h3>
                        <ul>
                            <li>Your resume can be easily read by most ATS systems</li>
                            <li>Hiring managers are more likely to see your application</li>
                            <li>You have a better chance of getting past the initial screening</li>
                            <li>Your skills and experience will be properly recognized</li>
                        </ul>
                    </div>
                    
                    <p>You're now one step closer to landing your next big opportunity! Keep applying with confidence.</p>
                    
                    <p><strong>Next Steps:</strong></p>
                    <ul>
                        <li>Start applying to positions that match your skills</li>
                        <li>Consider tailoring your resume for specific job categories</li>
                        <li>Keep your resume updated with new skills and experiences</li>
                    </ul>
                    
                    <p>Best of luck with your job search!</p>
                    <p>Sincerely,<br><strong>The ATS Resume Checker Team</strong></p>
                </div>
                <div class="footer">
                    <p>© 2025 ATS Resume Checker | Helping job seekers succeed</p>
                    <p>Need help? Contact us at support@atsresumechecker.com</p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
            
        logger.info(f"Congratulations email sent successfully to {recipient}")
        
    except Exception as e:
        logger.error(f"Failed to send congratulations email to {recipient}: {str(e)}")
        raise


def send_rejection_email(name, recipient, ats_score, detailed_analysis):
    """Send rejection email with improvement suggestions"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "📋 Your Resume Analysis Results - Improvement Needed"
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient

        suggestions = []

        if detailed_analysis:
            # Get general recommendations from the main analysis
            if detailed_analysis.get('recommendations'):
                suggestions.extend(detailed_analysis['recommendations'][:6])
            else:
                # Fallback: generate suggestions based on low scores
                analysis_categories = ['format_compatibility', 'keyword_matching', 'readability', 'structure_organization', 'contact_information']
                for category in analysis_categories:
                    if category in detailed_analysis:
                        analysis = detailed_analysis[category]
                        if isinstance(analysis, dict):  # If it's a dictionary, access the 'score' key
                            score = analysis.get('score', 0)
                        else:  # If it's a float (direct score), assign it directly
                            score = analysis
                        
                        if score < 70:
                            if category == 'format_compatibility':
                                suggestions.append("Use a simple, clean format without tables or images")
                            elif category == 'keyword_matching':
                                suggestions.append("Include more relevant keywords for your field")
                            elif category == 'readability':
                                suggestions.append("Improve text clarity and use bullet points")
                            elif category == 'structure_organization':
                                suggestions.append("Organize sections clearly (Contact, Experience, Education, Skills)")
                            elif category == 'contact_information':
                                suggestions.append("Ensure contact information is clearly visible")

        suggestions_html = ""
        for i, suggestion in enumerate(suggestions[:6], 1):  # Limit to 6 suggestions
            suggestions_html += f"<li>{suggestion}</li>"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #f59e0b, #d97706); color: white; padding: 30px 20px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .content {{ padding: 30px; }}
                .score-badge {{ background: #f59e0b; color: white; padding: 15px; border-radius: 50px; text-align: center; margin: 20px 0; font-weight: bold; }}
                .improvement-section {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .tips-section {{ background: #f0f9ff; border-left: 4px solid #3b82f6; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 14px; }}
                .btn {{ display: inline-block; background: #3b82f6; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
                .highlight {{ color: #d97706; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📋 Resume Analysis Results</h1>
                    <p>Room for Improvement Detected</p>
                </div>
                <div class="content">
                    <p>Hi <strong>{name}</strong>,</p>
                    
                    <div class="score-badge">
                        📊 ATS Score: {ats_score}%
                    </div>
                    
                    <p>Thank you for using our ATS Resume Checker! While your resume shows potential, our analysis indicates that some improvements could help you get better results with Applicant Tracking Systems.</p>
                    
                    <div class="improvement-section">
                        <h3>🎯 Key Areas for Improvement:</h3>
                        {"<ul>" + suggestions_html + "</ul>" if suggestions_html else "<p>Focus on standard formatting, clear section headers, and relevant keywords for your target industry.</p>"}
                    </div>
                    
                    <div class="tips-section">
                        <h3>💡 Quick Tips to Boost Your ATS Score:</h3>
                        <ul>
                            <li><strong>Use Standard Fonts:</strong> Stick to Arial, Calibri, or Times New Roman</li>
                            <li><strong>Include Keywords:</strong> Match job posting keywords in your experience section</li>
                            <li><strong>Clear Section Headers:</strong> Use standard headers like "Experience," "Education," "Skills"</li>
                            <li><strong>Save as PDF:</strong> Ensure your formatting stays consistent</li>
                            <li><strong>Contact Information:</strong> Include phone, email, and location at the top</li>
                            <li><strong>No Graphics/Tables:</strong> Keep formatting simple and text-based</li>
                        </ul>
                    </div>
                    
                    <p><strong>Don't get discouraged!</strong> These improvements will significantly increase your chances of getting past ATS systems and landing interviews.</p>
                    
                    <p>Feel free to resubmit your updated resume for another analysis. We're here to help you succeed!</p>
                    
                    <p>Best regards,<br><strong>The ATS Resume Checker Team</strong></p>
                </div>
                <div class="footer">
                    <p>© 2025 ATS Resume Checker | Helping job seekers succeed</p>
                    <p>Need help? Contact us at support@atsresumechecker.com</p>
                </div>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
            
        logger.info(f"Improvement email sent successfully to {recipient}")
        
    except Exception as e:
        logger.error(f"Failed to send improvement email to {recipient}: {str(e)}")
        raise
