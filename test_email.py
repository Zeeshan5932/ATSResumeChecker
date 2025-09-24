"""
Test script for email functionality
Run this to test if email sending is working correctly
"""

import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.email_sender import send_ats_notification

def test_email_functionality():
    """Test both congratulations and rejection emails"""
    
    print("Testing ATS Resume Checker Email Functionality")
    print("=" * 50)
    
    # Test data
    test_user_name = "John Doe"
    test_user_email = "zeeshanoffical01@gmail.com"  # Replace with your email for testing
    
    # Test passed ATS (congratulations email)
    print("\n1. Testing Congratulations Email (ATS Passed)...")
    test_analysis_passed = {
        'strengths': [
            'Well-structured resume with clear sections',
            'Good use of relevant keywords',
            'Professional formatting',
            'Strong contact information',
            'Appropriate file format'
        ],
        'recommendations': [
            'Consider adding more specific metrics to achievements',
            'Include industry-specific certifications',
            'Update skills section with latest technologies'
        ]
    }
    
    success1 = send_ats_notification(
        user_name=test_user_name,
        user_email=test_user_email,
        ats_score=85,
        job_category="software_engineer",
        detailed_analysis=test_analysis_passed,
        passed_ats=True
    )
    
    print(f"Congratulations email sent: {'✅ Success' if success1 else '❌ Failed'}")
    
    # Test failed ATS (rejection/improvement email)
    print("\n2. Testing Improvement Suggestions Email (ATS Failed)...")
    test_analysis_failed = {
        'weaknesses': [
            'Resume format may not be ATS-compatible',
            'Missing important keywords for the job category',
            'Contact information could be improved',
            'Text readability issues detected'
        ],
        'recommendations': [
            'Use a simpler, more standard resume format',
            'Include more relevant keywords from job postings',
            'Ensure contact information is clearly formatted',
            'Improve text structure and readability',
            'Consider using bullet points for better organization'
        ]
    }
    
    success2 = send_ats_notification(
        user_name=test_user_name,
        user_email=test_user_email,
        ats_score=45,
        job_category="data_scientist",
        detailed_analysis=test_analysis_failed,
        passed_ats=False
    )
    
    print(f"Improvement suggestions email sent: {'✅ Success' if success2 else '❌ Failed'}")
    
    print("\n" + "=" * 50)
    print("Email Test Summary:")
    print(f"Congratulations Email: {'✅ Success' if success1 else '❌ Failed'}")
    print(f"Improvement Email: {'✅ Success' if success2 else '❌ Failed'}")
    
    if success1 and success2:
        print("\n🎉 All email tests passed! Email functionality is working correctly.")
    elif success1 or success2:
        print("\n⚠️ Some email tests failed. Check your email configuration.")
    else:
        print("\n❌ All email tests failed. Please check your email configuration.")
        print("\nCommon issues:")
        print("- Incorrect email credentials")
        print("- SMTP server settings incorrect")
        print("- Email provider blocking less secure apps")
        print("- Network connectivity issues")
    
    print("\nNote: Make sure to check your spam/junk folder for test emails.")

if __name__ == "__main__":
    print("⚠️ IMPORTANT: Update test_user_email variable with your actual email before running!")
    print("Current test email:", "test@example.com")
    
    proceed = input("\nHave you updated the test email address? (y/n): ").strip().lower()
    if proceed == 'y':
        test_email_functionality()
    else:
        print("Please update the test_user_email variable in this script first.")
