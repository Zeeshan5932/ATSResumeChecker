"""
JSON Logger Module
Handles logging of resume submissions and analysis results to JSON files
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JSONLogger:
    def __init__(self, log_directory="data"):
        """
        Initialize JSON Logger
        
        Args:
            log_directory: Directory to store JSON log files
        """
        self.log_directory = log_directory
        self.submissions_file = os.path.join(log_directory, "resume_submissions.json")
        self.analysis_file = os.path.join(log_directory, "analysis_results.json")
        
        # Create log directory if it doesn't exist
        os.makedirs(log_directory, exist_ok=True)
        
        # Initialize JSON files if they don't exist
        self._initialize_json_files()
    
    def _initialize_json_files(self):
        """Initialize JSON files with empty arrays if they don't exist"""
        for file_path in [self.submissions_file, self.analysis_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump([], file, indent=2)
                logger.info(f"Created JSON log file: {file_path}")
    
    def _read_json_file(self, file_path: str) -> List[Dict]:
        """Read and return data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _write_json_file(self, file_path: str, data: List[Dict]):
        """Write data to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False, default=str)
    
    def log_submission(self, submission_data: Dict[str, Any]):
        """
        Log a resume submission
        
        Args:
            submission_data: Dictionary containing submission information
        """
        try:
            # Add timestamp
            submission_data['timestamp'] = datetime.now().isoformat()
            submission_data['id'] = f"sub_{int(datetime.now().timestamp())}"
            
            # Read existing data
            existing_data = self._read_json_file(self.submissions_file)
            
            # Add new submission
            existing_data.append(submission_data)
            
            # Write back to file
            self._write_json_file(self.submissions_file, existing_data)
            
            logger.info(f"Logged submission for {submission_data.get('filename', 'unknown file')}")
            
        except Exception as e:
            logger.error(f"Failed to log submission: {str(e)}")
    
    def log_analysis(self, analysis_data: Dict[str, Any]):
        """
        Log detailed analysis results
        
        Args:
            analysis_data: Dictionary containing analysis information
        """
        try:
            # Add timestamp and ID
            analysis_data['timestamp'] = datetime.now().isoformat()
            analysis_data['id'] = f"analysis_{int(datetime.now().timestamp())}"
            
            # Read existing data
            existing_data = self._read_json_file(self.analysis_file)
            
            # Add new analysis
            existing_data.append(analysis_data)
            
            # Write back to file
            self._write_json_file(self.analysis_file, existing_data)
            
            logger.info(f"Logged analysis for {analysis_data.get('filename', 'unknown file')}")
            
        except Exception as e:
            logger.error(f"Failed to log analysis: {str(e)}")
    
    def get_submissions_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics from submissions log
        
        Returns:
            Dictionary containing summary statistics
        """
        try:
            submissions = self._read_json_file(self.submissions_file)
            
            if not submissions:
                return {'total_submissions': 0}
            
            total_submissions = len(submissions)
            passed_submissions = sum(1 for sub in submissions if sub.get('passed_ats', False))
            failed_submissions = total_submissions - passed_submissions
            
            # Calculate average score
            scores = [sub.get('ats_score', 0) for sub in submissions if sub.get('ats_score') is not None]
            average_score = sum(scores) / len(scores) if scores else 0
            
            # Count by job category
            job_categories = {}
            for sub in submissions:
                category = sub.get('job_category', 'unknown')
                job_categories[category] = job_categories.get(category, 0) + 1
            
            # Recent submissions (last 24 hours and week)
            now = datetime.now()
            submissions_24h = sum(1 for sub in submissions 
                                if (now - datetime.fromisoformat(sub.get('timestamp', '1970-01-01'))).days == 0)
            submissions_week = sum(1 for sub in submissions 
                                 if (now - datetime.fromisoformat(sub.get('timestamp', '1970-01-01'))).days <= 7)
            
            summary = {
                'total_submissions': total_submissions,
                'total_passed': passed_submissions,
                'total_failed': failed_submissions,
                'pass_rate': (passed_submissions / total_submissions * 100) if total_submissions > 0 else 0,
                'average_score': round(average_score, 1),
                'top_job_categories': dict(sorted(job_categories.items(), key=lambda x: x[1], reverse=True)[:5]),
                'submissions_last_24h': submissions_24h,
                'submissions_last_week': submissions_week
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate submissions summary: {str(e)}")
            return {'error': str(e)}
    
    def get_recent_submissions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent submissions
        
        Args:
            limit: Number of recent submissions to return
            
        Returns:
            List of recent submissions
        """
        try:
            submissions = self._read_json_file(self.submissions_file)
            
            if not submissions:
                return []
            
            # Sort by timestamp (newest first) and limit
            sorted_submissions = sorted(submissions, 
                                      key=lambda x: x.get('timestamp', ''), 
                                      reverse=True)
            
            return sorted_submissions[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get recent submissions: {str(e)}")
            return []


# Convenience functions for easy usage
def log_resume_submission(filename: str, user_name: str = "", user_email: str = "", 
                         job_category: str = "", file_size_mb: float = 0,
                         ats_score: int = 0, passed_ats: bool = False,
                         status: str = "processed"):
    """
    Simple function to log a resume submission
    """
    logger_instance = JSONLogger()
    
    submission_data = {
        'filename': filename,
        'user_name': user_name,
        'user_email': user_email,
        'job_category': job_category,
        'file_size_mb': file_size_mb,
        'ats_score': ats_score,
        'passed_ats': passed_ats,
        'status': status
    }
    
    logger_instance.log_submission(submission_data)


def log_resume_analysis(filename: str, user_name: str = "", ats_score: int = 0,
                       job_category: str = "", detailed_analysis: Dict = None,
                       processing_time: float = 0):
    """
    Simple function to log analysis results
    """
    logger_instance = JSONLogger()
    
    analysis_data = {
        'filename': filename,
        'user_name': user_name,
        'ats_score': ats_score,
        'job_category': job_category,
        'detailed_analysis': detailed_analysis or {},
        'processing_time': processing_time
    }
    
    logger_instance.log_analysis(analysis_data)


def get_dashboard_data() -> Dict[str, Any]:
    """
    Get data for admin dashboard
    """
    logger_instance = JSONLogger()
    return logger_instance.get_submissions_summary()
