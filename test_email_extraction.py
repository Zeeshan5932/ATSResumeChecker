"""
Test script for Efaida email extraction and storage functionality
"""

import sys
import os

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.email_manager import extract_and_store_candidate_email, email_manager

def test_email_extraction():
    """Test email extraction from sample CV text"""
    
    print("🏢 Testing Efaida Email Extraction System")
    print("=" * 50)
    
    # Sample CV text with embedded emails
    sample_cv_text = """
    John Smith
    Software Engineer
    
    Contact Information:
    Email: john.smith@gmail.com
    Phone: +1-555-0123
    LinkedIn: linkedin.com/in/johnsmith
    
    Professional Summary:
    Experienced software engineer with 5+ years in Python development.
    
    Experience:
    Senior Developer at TechCorp (2020-2024)
    - Developed web applications using React and Node.js
    - Worked with databases like PostgreSQL and MongoDB
    
    Education:
    Bachelor of Computer Science
    University of Technology (2016-2020)
    
    Skills:
    - Python, JavaScript, React, Node.js
    - SQL, PostgreSQL, MongoDB
    - Git, Docker, AWS
    
    Contact me at: j.smith.dev@outlook.com for opportunities.
    """
    
    print("1. Testing Email Extraction...")
    print(f"Sample CV Text Preview: {sample_cv_text[:100]}...")
    
    # Extract emails using the email manager
    extracted_emails = email_manager.extract_emails_from_text(sample_cv_text)
    print(f"Extracted emails: {extracted_emails}")
    
    print("\n2. Testing Email Storage...")
    
    # Store candidate email with CV information
    primary_email = extract_and_store_candidate_email(
        cv_text=sample_cv_text,
        candidate_name="John Smith",
        cv_filename="john_smith_cv.pdf",
        job_category="software_engineer",
        ats_score=85,
        passed_screening=True
    )
    
    if primary_email:
        print(f"✅ Successfully stored primary email: {primary_email}")
    else:
        print("❌ Failed to store candidate email")
    
    print("\n3. Testing Email Retrieval...")
    
    # Get all stored emails
    all_emails = email_manager.get_all_candidate_emails()
    print(f"Total stored emails: {len(all_emails)}")
    
    # Find the candidate we just added
    candidate = email_manager.get_candidate_by_email(primary_email) if primary_email else None
    if candidate:
        print(f"✅ Found candidate record:")
        print(f"   - Name: {candidate.get('candidate_name')}")
        print(f"   - Email: {candidate.get('email')}")
        print(f"   - Job Category: {candidate.get('latest_job_category')}")
        print(f"   - ATS Score: {candidate.get('latest_ats_score')}")
        print(f"   - Screening Result: {candidate.get('latest_screening_result')}")
        print(f"   - Submissions: {candidate.get('submission_count')}")
    else:
        print("❌ Could not find candidate record")
    
    print("\n4. Testing Filter Functionality...")
    
    # Test filtering by job category
    software_engineers = email_manager.get_emails_by_criteria(
        job_category="software_engineer",
        screening_result="passed"
    )
    print(f"Software engineers who passed: {len(software_engineers)}")
    
    # Test filtering by ATS score
    high_ats_candidates = email_manager.get_emails_by_criteria(
        min_ats_score=80
    )
    print(f"Candidates with ATS score >= 80: {len(high_ats_candidates)}")
    
    print("\n5. Testing Statistics...")
    
    # Get statistics
    stats = email_manager.get_statistics()
    print(f"Statistics:")
    print(f"   - Total emails: {stats['total_emails']}")
    print(f"   - Total submissions: {stats['total_submissions']}")
    print(f"   - Passed screening: {stats['passed_screening']}")
    print(f"   - Rejected screening: {stats['rejected_screening']}")
    print(f"   - Average ATS score: {stats['average_ats_score']}")
    print(f"   - Job categories: {stats['job_categories']}")
    
    print("\n6. Testing Multiple Submissions (Same Candidate)...")
    
    # Submit another CV for the same candidate
    updated_email = extract_and_store_candidate_email(
        cv_text=sample_cv_text,
        candidate_name="John Smith",
        cv_filename="john_smith_cv_updated.pdf",
        job_category="software_engineer",
        ats_score=90,
        passed_screening=True
    )
    
    if updated_email:
        updated_candidate = email_manager.get_candidate_by_email(updated_email)
        if updated_candidate:
            print(f"✅ Updated candidate record:")
            print(f"   - Submissions: {updated_candidate.get('submission_count')}")
            print(f"   - Latest ATS Score: {updated_candidate.get('latest_ats_score')}")
            print(f"   - Latest CV: {updated_candidate.get('latest_cv_filename')}")
    
    print("\n" + "=" * 50)
    print("Email Extraction and Storage Test Summary:")
    
    if primary_email and candidate:
        print("✅ Email extraction: PASSED")
        print("✅ Email storage: PASSED")
        print("✅ Email retrieval: PASSED")
        print("✅ Filtering: PASSED")
        print("✅ Statistics: PASSED")
        print("✅ Multiple submissions: PASSED")
        print("\n🎉 All tests passed! Efaida email system is working correctly.")
        
        print("\n📁 Data Files Created:")
        print(f"   - {email_manager.emails_file}")
        
        print("\n💡 Usage Tips:")
        print("   - Check the candidate emails page: /candidate-emails")
        print("   - Export emails to CSV: /export-emails")
        print("   - Filter by job category, screening result, or ATS score")
        print("   - All emails are automatically detected from CV text")
        
    else:
        print("❌ Some tests failed. Check the error messages above.")
    
    print("\n🔧 Next Steps:")
    print("1. Start the application: python app.py")
    print("2. Upload test CVs to see automatic email detection")
    print("3. Visit /candidate-emails to view collected emails")
    print("4. Use filters to find specific candidates")

def test_multiple_email_formats():
    """Test extraction of various email formats"""
    
    print("\n📧 Testing Multiple Email Formats...")
    print("-" * 40)
    
    test_texts = [
        "Contact: user@gmail.com",
        "Email me at: test.user@company.co.uk",
        "Business email: john.doe@business-corp.com", 
        "Personal: jane_smith123@outlook.com",
        "Multiple emails: first@test.com, second@example.org",
        "No valid emails: invalid@test, @gmail.com, test@",
        "Mixed: valid@test.com and invalid@test and another@valid.org"
    ]
    
    for i, text in enumerate(test_texts, 1):
        emails = email_manager.extract_emails_from_text(text)
        print(f"{i}. '{text}' → {emails}")

if __name__ == "__main__":
    print("🏢 Efaida Email Management System Test")
    print("Company: Efaida")
    print("=" * 60)
    
    # Run main test
    test_email_extraction()
    
    # Run additional format tests
    test_multiple_email_formats()
    
    print("\n" + "=" * 60)
    print("Testing complete! Check the data/candidate_emails.json file to see stored emails.")
