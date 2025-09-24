"""
Email sender utility for ATS Resume Checker
Sends congratulations or rejection emails based on ATS score
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
from typing import Optional, Dict, Any

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from config import get_email_config, EMAIL_TEMPLATE_VARS
except ImportError:
    # Fallback configuration
    EMAIL_TEMPLATE_VARS = {
        'company_name': 'ATS Resume Checker',
        'support_email': 'support@atsresumechecker.com',
        'website_url': 'https://www.atsresumechecker.com'
    }

logger = logging.getLogger(__name__)

class EmailSender:
    """Email sender class for ATS Resume Checker notifications"""
    
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
                'sender_name': 'ATS Resume Checker'
            }
    
    def create_congratulations_email(self, user_name: str, user_email: str, 
                                   ats_score: int, job_category: str, 
                                   detailed_analysis: Dict[str, Any]) -> MIMEMultipart:
        """Create congratulations email for passed ATS check"""
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.config['sender_name']} <{self.config['sender_email']}>"
        msg['To'] = user_email
        msg['Subject'] = f"🎉 Congratulations! Your Resume Passed Our ATS Check (Score: {ats_score}%)"
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .score-badge {{ background: #28a745; color: white; padding: 10px 20px; 
                              border-radius: 25px; font-size: 18px; font-weight: bold; 
                              display: inline-block; margin: 10px 0; }}
                .section {{ margin: 20px 0; padding: 15px; background: white; border-radius: 5px; 
                          border-left: 4px solid #28a745; }}
                .recommendation {{ background: #e8f5e8; padding: 10px; margin: 5px 0; 
                                 border-radius: 5px; border-left: 3px solid #28a745; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
                .cta-button {{ background: #28a745; color: white; padding: 12px 25px; 
                             text-decoration: none; border-radius: 5px; display: inline-block; 
                             margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Congratulations {user_name}!</h1>
                    <h2>Your Resume Passed Our ATS Check</h2>
                    <div class="score-badge">ATS Score: {ats_score}%</div>
                </div>
                
                <div class="content">
                    <p>Great news! Your resume for the <strong>{job_category}</strong> category has successfully passed our Applicant Tracking System (ATS) compatibility check.</p>
                    
                    <div class="section">
                        <h3>📊 Your Results Summary</h3>
                        <ul>
                            <li><strong>ATS Compatibility Score:</strong> {ats_score}% (Excellent!)</li>
                            <li><strong>Job Category:</strong> {job_category.title()}</li>
                            <li><strong>Status:</strong> ✅ PASSED - ATS Compatible</li>
                        </ul>
                    </div>
                    
                    <div class="section">
                        <h3>🎯 What This Means</h3>
                        <p>Your resume is well-optimized for Applicant Tracking Systems and has a high chance of:</p>
                        <ul>
                            <li>✅ Getting past initial automated screening</li>
                            <li>✅ Being seen by human recruiters</li>
                            <li>✅ Matching relevant job postings</li>
                            <li>✅ Standing out in applicant pools</li>
                        </ul>
                    </div>
        """
        
        # Add key strengths if available
        if detailed_analysis and 'strengths' in detailed_analysis:
            html_content += f"""
                    <div class="section">
                        <h3>💪 Key Strengths Identified</h3>
                        <ul>
            """
            for strength in detailed_analysis['strengths'][:5]:  # Top 5 strengths
                html_content += f"<li>{strength}</li>"
            html_content += "</ul></div>"
        
        # Add recommendations if available
        if detailed_analysis and 'recommendations' in detailed_analysis:
            html_content += f"""
                    <div class="section">
                        <h3>🚀 Further Enhancement Suggestions</h3>
                        <p>While your resume passed, here are some ways to make it even stronger:</p>
            """
            for recommendation in detailed_analysis['recommendations'][:3]:  # Top 3 recommendations
                html_content += f'<div class="recommendation">{recommendation}</div>'
            html_content += "</div>"
        
        html_content += f"""
                    <div class="section">
                        <h3>🎯 Next Steps</h3>
                        <ol>
                            <li>Start applying to positions with confidence</li>
                            <li>Tailor your resume for specific job postings</li>
                            <li>Keep your resume updated with new achievements</li>
                            <li>Consider our premium analysis for detailed insights</li>
                        </ol>
                    </div>
                    
                    <p style="text-align: center;">
                        <a href="{EMAIL_TEMPLATE_VARS['website_url']}" class="cta-button">
                            Analyze Another Resume
                        </a>
                    </p>
                    
                    <p>Best of luck with your job search!</p>
                    <p><strong>The {EMAIL_TEMPLATE_VARS['company_name']} Team</strong></p>
                </div>
                
                <div class="footer">
                    <p>This email was sent by {EMAIL_TEMPLATE_VARS['company_name']}</p>
                    <p>Questions? Contact us at {EMAIL_TEMPLATE_VARS['support_email']}</p>
                    <p>Visit us at {EMAIL_TEMPLATE_VARS['website_url']}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_content = f"""
Congratulations {user_name}!

Your resume has passed our ATS compatibility check with a score of {ats_score}%!

Results Summary:
- ATS Compatibility Score: {ats_score}% (Excellent!)
- Job Category: {job_category.title()}
- Status: PASSED - ATS Compatible

What This Means:
Your resume is well-optimized for Applicant Tracking Systems and has a high chance of getting past initial automated screening and being seen by human recruiters.

Next Steps:
1. Start applying to positions with confidence
2. Tailor your resume for specific job postings
3. Keep your resume updated with new achievements

Best of luck with your job search!

The {EMAIL_TEMPLATE_VARS['company_name']} Team
Contact: {EMAIL_TEMPLATE_VARS['support_email']}
Website: {EMAIL_TEMPLATE_VARS['website_url']}
        """
        
        # Attach both versions
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        return msg
    
    def create_rejection_email(self, user_name: str, user_email: str, 
                             ats_score: int, job_category: str, 
                             detailed_analysis: Dict[str, Any]) -> MIMEMultipart:
        """Create rejection email for failed ATS check with improvement suggestions"""
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.config['sender_name']} <{self.config['sender_email']}>"
        msg['To'] = user_email
        msg['Subject'] = f"📋 Your Resume Analysis Results - Improvement Opportunities (Score: {ats_score}%)"
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .score-badge {{ background: #dc3545; color: white; padding: 10px 20px; 
                              border-radius: 25px; font-size: 18px; font-weight: bold; 
                              display: inline-block; margin: 10px 0; }}
                .section {{ margin: 20px 0; padding: 15px; background: white; border-radius: 5px; 
                          border-left: 4px solid #dc3545; }}
                .improvement {{ background: #fff3cd; padding: 10px; margin: 5px 0; 
                              border-radius: 5px; border-left: 3px solid #ffc107; }}
                .urgent {{ background: #f8d7da; padding: 10px; margin: 5px 0; 
                         border-radius: 5px; border-left: 3px solid #dc3545; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
                .cta-button {{ background: #007bff; color: white; padding: 12px 25px; 
                             text-decoration: none; border-radius: 5px; display: inline-block; 
                             margin: 10px 0; }}
                .tip {{ background: #d1ecf1; padding: 10px; margin: 5px 0; 
                       border-radius: 5px; border-left: 3px solid #17a2b8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📋 Resume Analysis Complete</h1>
                    <h2>Hi {user_name}, Let's Improve Your Resume!</h2>
                    <div class="score-badge">ATS Score: {ats_score}%</div>
                </div>
                
                <div class="content">
                    <p>Thank you for using our ATS Resume Checker! Your resume for the <strong>{job_category}</strong> category has been analyzed, and we've identified several opportunities to improve its ATS compatibility.</p>
                    
                    <div class="section">
                        <h3>📊 Your Current Results</h3>
                        <ul>
                            <li><strong>ATS Compatibility Score:</strong> {ats_score}%</li>
                            <li><strong>Job Category:</strong> {job_category.title()}</li>
                            <li><strong>Status:</strong> ❌ Needs Improvement</li>
                            <li><strong>Target Score:</strong> 75%+ for optimal ATS compatibility</li>
                        </ul>
                    </div>
                    
                    <div class="section">
                        <h3>🎯 What This Means</h3>
                        <p>Your resume may face challenges with Applicant Tracking Systems, which could mean:</p>
                        <ul>
                            <li>⚠️ Reduced visibility to recruiters</li>
                            <li>⚠️ Lower ranking in search results</li>
                            <li>⚠️ Missed opportunities for interviews</li>
                        </ul>
                        <p><strong>But don't worry!</strong> With some targeted improvements, you can significantly boost your ATS compatibility.</p>
                    </div>
        """
        
        # Add critical issues if available
        if detailed_analysis and 'weaknesses' in detailed_analysis:
            html_content += f"""
                    <div class="section">
                        <h3>🚨 Critical Areas to Address</h3>
            """
            for weakness in detailed_analysis['weaknesses'][:4]:  # Top 4 critical issues
                html_content += f'<div class="urgent">• {weakness}</div>'
            html_content += "</div>"
        
        # Add improvement recommendations
        if detailed_analysis and 'recommendations' in detailed_analysis:
            html_content += f"""
                    <div class="section">
                        <h3>🚀 Priority Improvements</h3>
                        <p>Focus on these key areas to boost your ATS score:</p>
            """
            for i, recommendation in enumerate(detailed_analysis['recommendations'][:5], 1):
                html_content += f'<div class="improvement"><strong>{i}.</strong> {recommendation}</div>'
            html_content += "</div>"
        
        # Add general tips
        html_content += f"""
                    <div class="section">
                        <h3>💡 Quick ATS Optimization Tips</h3>
                        <div class="tip">✅ Use standard section headers (Experience, Education, Skills)</div>
                        <div class="tip">✅ Include relevant keywords from job postings</div>
                        <div class="tip">✅ Use simple, clean formatting without images or tables</div>
                        <div class="tip">✅ Save as .docx or .pdf format</div>
                        <div class="tip">✅ Spell out abbreviations and include both versions</div>
                    </div>
                    
                    <div class="section">
                        <h3>🎯 Next Steps</h3>
                        <ol>
                            <li>Review and implement the priority improvements above</li>
                            <li>Update your resume with relevant keywords for your target role</li>
                            <li>Test your updated resume with our checker again</li>
                            <li>Consider our detailed analysis service for personalized guidance</li>
                        </ol>
                    </div>
                    
                    <p style="text-align: center;">
                        <a href="{EMAIL_TEMPLATE_VARS['website_url']}" class="cta-button">
                            Test Your Updated Resume
                        </a>
                    </p>
                    
                    <p>Remember: Every successful professional has faced resume challenges. With the right optimizations, your resume can stand out and get you the interviews you deserve!</p>
                    <p><strong>The {EMAIL_TEMPLATE_VARS['company_name']} Team</strong></p>
                </div>
                
                <div class="footer">
                    <p>This email was sent by {EMAIL_TEMPLATE_VARS['company_name']}</p>
                    <p>Questions? Contact us at {EMAIL_TEMPLATE_VARS['support_email']}</p>
                    <p>Visit us at {EMAIL_TEMPLATE_VARS['website_url']}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_content = f"""
Hi {user_name},

Your resume has been analyzed for ATS compatibility with a score of {ats_score}%.

Current Results:
- ATS Compatibility Score: {ats_score}%
- Job Category: {job_category.title()}
- Status: Needs Improvement
- Target Score: 75%+ for optimal ATS compatibility

What This Means:
Your resume may face challenges with Applicant Tracking Systems, but with targeted improvements, you can significantly boost your ATS compatibility.

Quick ATS Optimization Tips:
✅ Use standard section headers (Experience, Education, Skills)
✅ Include relevant keywords from job postings
✅ Use simple, clean formatting without images or tables
✅ Save as .docx or .pdf format
✅ Spell out abbreviations and include both versions

Next Steps:
1. Review and implement the suggested improvements
2. Update your resume with relevant keywords
3. Test your updated resume with our checker again

Remember: With the right optimizations, your resume can stand out and get you the interviews you deserve!

The {EMAIL_TEMPLATE_VARS['company_name']} Team
Contact: {EMAIL_TEMPLATE_VARS['support_email']}
Website: {EMAIL_TEMPLATE_VARS['website_url']}
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
            
            logger.info(f"Email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_ats_result_email(self, user_name: str, user_email: str, 
                            ats_score: int, job_category: str, 
                            detailed_analysis: Dict[str, Any], passed_ats: bool) -> bool:
        """Send appropriate email based on ATS result"""
        
        if not user_email or '@' not in user_email:
            logger.warning("Invalid email address provided")
            return False
        
        try:
            if passed_ats:
                msg = self.create_congratulations_email(
                    user_name, user_email, ats_score, job_category, detailed_analysis
                )
                logger.info(f"Sending congratulations email to {user_email}")
            else:
                msg = self.create_rejection_email(
                    user_name, user_email, ats_score, job_category, detailed_analysis
                )
                logger.info(f"Sending improvement suggestions email to {user_email}")
            
            return self.send_email(msg)
            
        except Exception as e:
            logger.error(f"Error creating/sending ATS result email: {str(e)}")
            return False

# Create global email sender instance
email_sender = EmailSender()

def send_ats_notification(user_name: str, user_email: str, ats_score: int, 
                         job_category: str, detailed_analysis: Dict[str, Any], 
                         passed_ats: bool) -> bool:
    """Convenience function to send ATS notification email"""
    return email_sender.send_ats_result_email(
        user_name, user_email, ats_score, job_category, detailed_analysis, passed_ats
    )
