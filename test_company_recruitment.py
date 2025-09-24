"""
Test script for company recruitment email functionality
Run this to test if company recruitment emails are working correctly
"""

import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.company_email_sender import send_recruitment_notification
from config import COMPANY_CONFIG

def test_company_recruitment_emails():
    """Test both acceptance and rejection emails for company recruitment"""
    
    print(f"Testing {COMPANY_CONFIG['company_name']} Recruitment Email System")
    print("=" * 60)
    
    # Test data
    test_candidate_name = "John Smith"
    test_candidate_email = "test@example.com"  # Replace with your email for testing
    test_position = "software_engineer"
    
    # Test passed company screening (acceptance email)
    print("\n1. Testing Acceptance Email (Company Screening Passed)...")
    company_scores_passed = {
        'final_score': 75.5,
        'ats_compatibility': 82,
        'keyword_relevance': 78,
        'experience_level': 70,
        'education_background': 85,
        'skills_match': 75,
        'passes_criteria': True,
        'required_keywords_found': 8,
        'required_keywords_total': 10,
        'preferred_keywords_found': 5,
        'preferred_keywords_total': 8,
        'minimum_ats_score': 75
    }
    
    success1 = send_recruitment_notification(
        candidate_name=test_candidate_name,
        candidate_email=test_candidate_email,
        position=test_position,
        company_scores=company_scores_passed,
        passed_screening=True,
        feedback_areas=[]
    )
    
    print(f"Acceptance email sent: {'✅ Success' if success1 else '❌ Failed'}")
    
    # Test failed company screening (rejection email)
    print("\n2. Testing Rejection Email (Company Screening Failed)...")
    company_scores_failed = {
        'final_score': 45.2,
        'ats_compatibility': 60,
        'keyword_relevance': 35,
        'experience_level': 40,
        'education_background': 50,
        'skills_match': 38,
        'passes_criteria': False,
        'required_keywords_found': 3,
        'required_keywords_total': 10,
        'preferred_keywords_found': 1,
        'preferred_keywords_total': 8,
        'minimum_ats_score': 75
    }
    
    feedback_areas = [
        "CV format needs improvement for ATS compatibility",
        "Missing key technical skills for software engineering position",
        "Professional experience should better highlight relevant programming languages",
        "Consider adding more specific project details and achievements"
    ]
    
    success2 = send_recruitment_notification(
        candidate_name=test_candidate_name,
        candidate_email=test_candidate_email,
        position=test_position,
        company_scores=company_scores_failed,
        passed_screening=False,
        feedback_areas=feedback_areas
    )
    
    print(f"Rejection email sent: {'✅ Success' if success2 else '❌ Failed'}")
    
    print("\n" + "=" * 60)
    print("Company Recruitment Email Test Summary:")
    print(f"Company: {COMPANY_CONFIG['company_name']}")
    print(f"HR Email: {COMPANY_CONFIG['hr_email']}")
    print(f"Acceptance Email: {'✅ Success' if success1 else '❌ Failed'}")
    print(f"Rejection Email: {'✅ Success' if success2 else '❌ Failed'}")
    
    if success1 and success2:
        print("\n🎉 All recruitment email tests passed! Company email system is working correctly.")
        print("\n📧 Email Content Overview:")
        print("✅ Acceptance emails include: score breakdown, next steps, contact info")
        print("✅ Rejection emails include: detailed feedback, improvement tips, encouragement")
    elif success1 or success2:
        print("\n⚠️ Some email tests failed. Check your email configuration.")
    else:
        print("\n❌ All email tests failed. Please check your email configuration.")
        print("\nCommon issues:")
        print("- Incorrect email credentials in config.py")
        print("- SMTP server settings incorrect")
        print("- Email provider blocking less secure apps")
        print("- Network connectivity issues")
    
    print("\n📝 Configuration Check:")
    print(f"Company Name: {COMPANY_CONFIG['company_name']}")
    print(f"HR Email: {COMPANY_CONFIG['hr_email']}")
    print(f"Website: {COMPANY_CONFIG['company_website']}")
    
    print("\n⚠️ Note: Make sure to:")
    print("1. Check your spam/junk folder for test emails")
    print("2. Update COMPANY_CONFIG in config.py with your actual company details")
    print("3. Update email credentials for your SMTP server")

def show_company_config():
    """Display current company configuration"""
    print("Current Company Configuration:")
    print("=" * 40)
    for key, value in COMPANY_CONFIG.items():
        print(f"{key}: {value}")
    print("=" * 40)

if __name__ == "__main__":
    print("🏢 Company Recruitment Email System Test")
    print("=" * 60)
    
    show_company_config()
    
    print("\n⚠️ IMPORTANT: Update test_candidate_email variable with your actual email before running!")
    print("Current test email:", "test@example.com")
    print("\nAlso ensure COMPANY_CONFIG in config.py is updated with your company details.")
    
    proceed = input("\nHave you updated the configurations? (y/n): ").strip().lower()
    if proceed == 'y':
        test_company_recruitment_emails()
    else:
        print("Please update the configurations first:")
        print("1. test_candidate_email variable in this script")
        print("2. COMPANY_CONFIG in config.py")
        print("3. Email credentials in config.py")
