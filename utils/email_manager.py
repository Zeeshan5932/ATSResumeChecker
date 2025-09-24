"""
Email Management Utility for Efaida CV Screening System
Handles automatic email detection, storage, and retrieval
"""

import json
import os
import re
import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class EmailManager:
    """Manages candidate emails for Efaida recruitment system"""
    
    def __init__(self):
        """Initialize email manager with storage paths"""
        self.emails_file = "data/candidate_emails.json"
        self.emails_dir = "data"
        
        # Create data directory if it doesn't exist
        os.makedirs(self.emails_dir, exist_ok=True)
        
        # Initialize emails file if it doesn't exist
        if not os.path.exists(self.emails_file):
            self._initialize_emails_file()
    
    def _initialize_emails_file(self):
        """Initialize the emails JSON file with basic structure"""
        initial_data = {
            "metadata": {
                "created_date": datetime.now().isoformat(),
                "company": "Efaida",
                "description": "Candidate emails extracted from CV submissions",
                "total_emails": 0,
                "last_updated": datetime.now().isoformat()
            },
            "emails": []
        }
        
        with open(self.emails_file, 'w', encoding='utf-8') as file:
            json.dump(initial_data, file, indent=2, ensure_ascii=False)
        
        logger.info(f"Initialized candidate emails file: {self.emails_file}")
    
    def extract_emails_from_text(self, text: str) -> List[str]:
        """Extract all email addresses from text using regex"""
        if not text:
            return []
        
        # Enhanced email regex pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Clean and validate emails
        valid_emails = []
        for email in emails:
            email = email.lower().strip()
            # Basic validation
            if self._is_valid_email(email):
                valid_emails.append(email)
        
        # Remove duplicates while preserving order
        unique_emails = list(dict.fromkeys(valid_emails))
        
        logger.info(f"Extracted {len(unique_emails)} valid emails from CV text")
        return unique_emails
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format and filter out common false positives"""
        if not email or len(email) < 5:
            return False
        
        # Basic format check
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email):
            return False
        
        # Filter out common false positives
        invalid_patterns = [
            'example.com',
            'test.com',
            'sample.com',
            'placeholder.com',
            'dummy.com',
            'lorem.com'
        ]
        
        for pattern in invalid_patterns:
            if pattern in email:
                return False
        
        return True
    
    def store_candidate_email(self, email: str, candidate_name: str = "", 
                            cv_filename: str = "", job_category: str = "",
                            ats_score: int = 0, passed_screening: bool = False) -> bool:
        """Store candidate email with associated information"""
        if not email or not self._is_valid_email(email):
            logger.warning(f"Invalid email provided for storage: {email}")
            return False
        
        try:
            # Load existing data
            with open(self.emails_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Check if email already exists
            existing_email = self._find_existing_email(data, email)
            
            if existing_email:
                # Update existing entry
                existing_email.update({
                    "last_submission_date": datetime.now().isoformat(),
                    "submission_count": existing_email.get("submission_count", 1) + 1,
                    "latest_cv_filename": cv_filename,
                    "latest_job_category": job_category,
                    "latest_ats_score": ats_score,
                    "latest_screening_result": "passed" if passed_screening else "rejected"
                })
                
                # Update candidate name if provided and not already set
                if candidate_name and not existing_email.get("candidate_name"):
                    existing_email["candidate_name"] = candidate_name
                
                logger.info(f"Updated existing email record: {email}")
            else:
                # Add new email entry
                new_entry = {
                    "email": email,
                    "candidate_name": candidate_name,
                    "first_submission_date": datetime.now().isoformat(),
                    "last_submission_date": datetime.now().isoformat(),
                    "submission_count": 1,
                    "latest_cv_filename": cv_filename,
                    "latest_job_category": job_category,
                    "latest_ats_score": ats_score,
                    "latest_screening_result": "passed" if passed_screening else "rejected",
                    "source": "cv_extraction",
                    "status": "active"
                }
                
                data["emails"].append(new_entry)
                data["metadata"]["total_emails"] = len(data["emails"])
                logger.info(f"Added new email record: {email}")
            
            # Update metadata
            data["metadata"]["last_updated"] = datetime.now().isoformat()
            
            # Save updated data
            with open(self.emails_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Error storing candidate email: {str(e)}")
            return False
    
    def _find_existing_email(self, data: dict, email: str) -> Optional[dict]:
        """Find existing email entry in data"""
        for entry in data.get("emails", []):
            if entry.get("email", "").lower() == email.lower():
                return entry
        return None
    
    def get_all_candidate_emails(self) -> List[Dict]:
        """Get all stored candidate emails"""
        try:
            with open(self.emails_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data.get("emails", [])
        except Exception as e:
            logger.error(f"Error retrieving candidate emails: {str(e)}")
            return []
    
    def get_candidate_by_email(self, email: str) -> Optional[Dict]:
        """Get candidate information by email"""
        emails = self.get_all_candidate_emails()
        for candidate in emails:
            if candidate.get("email", "").lower() == email.lower():
                return candidate
        return None
    
    def get_emails_by_criteria(self, job_category: str = None, 
                             screening_result: str = None,
                             min_ats_score: int = None) -> List[Dict]:
        """Get emails filtered by specific criteria"""
        emails = self.get_all_candidate_emails()
        filtered_emails = []
        
        for email_data in emails:
            # Filter by job category
            if job_category and email_data.get("latest_job_category") != job_category:
                continue
            
            # Filter by screening result
            if screening_result and email_data.get("latest_screening_result") != screening_result:
                continue
            
            # Filter by minimum ATS score
            if min_ats_score is not None and email_data.get("latest_ats_score", 0) < min_ats_score:
                continue
            
            filtered_emails.append(email_data)
        
        return filtered_emails
    
    def export_emails_to_csv(self, output_file: str = "data/candidate_emails.csv") -> bool:
        """Export candidate emails to CSV format"""
        try:
            import csv
            emails = self.get_all_candidate_emails()
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                if not emails:
                    return True
                
                fieldnames = emails[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for email_data in emails:
                    writer.writerow(email_data)
            
            logger.info(f"Exported {len(emails)} emails to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting emails to CSV: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get statistics about stored emails"""
        emails = self.get_all_candidate_emails()
        
        stats = {
            "total_emails": len(emails),
            "total_submissions": sum(email.get("submission_count", 1) for email in emails),
            "passed_screening": len([e for e in emails if e.get("latest_screening_result") == "passed"]),
            "rejected_screening": len([e for e in emails if e.get("latest_screening_result") == "rejected"]),
            "job_categories": {},
            "average_ats_score": 0
        }
        
        if emails:
            # Calculate average ATS score
            total_score = sum(email.get("latest_ats_score", 0) for email in emails)
            stats["average_ats_score"] = round(total_score / len(emails), 2)
            
            # Count by job categories
            for email in emails:
                category = email.get("latest_job_category", "unknown")
                stats["job_categories"][category] = stats["job_categories"].get(category, 0) + 1
        
        return stats

# Global email manager instance
email_manager = EmailManager()

def extract_and_store_candidate_email(cv_text: str, candidate_name: str = "",
                                    cv_filename: str = "", job_category: str = "",
                                    ats_score: int = 0, passed_screening: bool = False) -> Optional[str]:
    """
    Extract email from CV text and store candidate information
    Returns the primary email if found, None otherwise
    """
    emails = email_manager.extract_emails_from_text(cv_text)
    
    if emails:
        # Use the first email as primary
        primary_email = emails[0]
        
        # Store the primary email with candidate info
        success = email_manager.store_candidate_email(
            email=primary_email,
            candidate_name=candidate_name,
            cv_filename=cv_filename,
            job_category=job_category,
            ats_score=ats_score,
            passed_screening=passed_screening
        )
        
        if success:
            logger.info(f"Successfully stored candidate email: {primary_email}")
            return primary_email
        else:
            logger.error(f"Failed to store candidate email: {primary_email}")
    
    return None

def get_candidate_emails_for_job(job_category: str, passed_only: bool = True) -> List[str]:
    """Get list of candidate emails for a specific job category"""
    screening_result = "passed" if passed_only else None
    candidates = email_manager.get_emails_by_criteria(
        job_category=job_category,
        screening_result=screening_result
    )
    return [candidate["email"] for candidate in candidates]

def get_email_statistics() -> Dict:
    """Get statistics about candidate emails"""
    return email_manager.get_statistics()
