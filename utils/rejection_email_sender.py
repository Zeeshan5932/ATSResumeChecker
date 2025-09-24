"""
Enhanced Rejection Email Sender
Sends professional rejection emails with clear reasons and improvement suggestions
"""

import smtplib
import logging
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List
from pathlib import Path
from jinja2 import Template

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from config import get_email_config, COMPANY_CONFIG
except ImportError:
    # Fallback configuration
    COMPANY_CONFIG = {
        'hr_email': 'hr@example.com',
        'department': 'Human Resources',
        'recruitment_portal': 'https://careers.example.com'
    }

logger = logging.getLogger(__name__)

class EnhancedRejectionEmailSender:
    """Enhanced email sender for CV rejection emails"""
    
    def __init__(self):
        """Initialize email sender with configuration"""
        try:
            self.config = get_email_config()
        except:
            # Fallback configuration
            self.config = {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'sender_email': 'your-email@gmail.com',
                'sender_password': 'your-app-password',
                'sender_name': 'HR Team'
            }
        
        # Load rejection email template
        template_path = os.path.join(os.path.dirname(__file__), 'rejection_email_template.html')
        with open(template_path, 'r', encoding='utf-8') as file:
            self.rejection_template = Template(file.read())
    
    def create_rejection_email(self, 
                               candidate_name: str, 
                               candidate_email: str,
                               position: str,
                               company_scores: Dict[str, Any],
                               feedback_areas: List[str]) -> MIMEMultipart:
        """Create an enhanced rejection email using template"""
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{self.config['sender_name']} <{self.config['sender_email']}>"
        msg['To'] = candidate_email
        msg['Subject'] = f"Application Status Update for {position} Position"
        
        # Template context
        context = {
            'candidate_name': candidate_name,
            'position': position,
            'company_scores': company_scores,
            'feedback_areas': feedback_areas,
            'hr_email': COMPANY_CONFIG['hr_email'],
            'department': COMPANY_CONFIG['department'],
            'recruitment_portal': COMPANY_CONFIG['recruitment_portal']
        }
        
        # Render HTML content from template
        html_content = self.rejection_template.render(**context)
        
        # Create plain text version
        text_content = f"""
Application Status Update

Hello {candidate_name},

Thank you for your interest in the {position} position. We've carefully reviewed your application.

Unfortunately, your CV did not meet our current requirements for this position.

Why Your CV Was Not Selected:
- Your Score: {company_scores['final_score']}/100
- Minimum Required: 60/100

Your application didn't meet our requirements in the following areas:
"""
        
        for area in feedback_areas:
            text_content += f"• {area}\n"
        
        text_content += f"""
How to Improve Your CV:
✓ Match Keywords: Add relevant industry-specific terms from job descriptions
✓ Quantify Achievements: Use numbers and metrics to demonstrate impact
✓ Optimize for ATS: Use simple formatting and standard section headings
✓ Focus on Skills Gap: Address any missing skills through courses or projects

We encourage you to enhance your CV based on this feedback and consider applying for future positions.

Best regards,
{COMPANY_CONFIG['department']}

For inquiries, please contact {COMPANY_CONFIG['hr_email']}
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
            
            logger.info(f"Rejection email sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send rejection email: {str(e)}")
            return False
    
    def send_rejection_notification(self, 
                                   candidate_name: str, 
                                   candidate_email: str,
                                   position: str,
                                   company_scores: Dict[str, Any],
                                   feedback_areas: List[str] = None) -> bool:
        """Send rejection notification email"""
        
        if not candidate_email or '@' not in candidate_email:
            logger.warning("Invalid email address provided")
            return False
        
        try:
            # Default feedback if none provided
            feedback_areas = feedback_areas or [
                "Your CV format lacks ATS compatibility",
                "Key skills and keywords for the position are missing",
                "Your experience isn't clearly aligned with the position requirements"
            ]
            
            msg = self.create_rejection_email(
                candidate_name, candidate_email, position, company_scores, feedback_areas
            )
            
            logger.info(f"Sending enhanced rejection email to {candidate_email}")
            return self.send_email(msg)
            
        except Exception as e:
            logger.error(f"Error creating/sending rejection email: {str(e)}")
            return False

# Create global instance for easy access
rejection_email_sender = EnhancedRejectionEmailSender()

def send_rejection_notification(candidate_name: str, 
                              candidate_email: str, 
                              position: str,
                              company_scores: Dict[str, Any],
                              feedback_areas: List[str] = None) -> bool:
    """Convenience function to send rejection notification email"""
    return rejection_email_sender.send_rejection_notification(
        candidate_name, candidate_email, position, company_scores, feedback_areas
    )