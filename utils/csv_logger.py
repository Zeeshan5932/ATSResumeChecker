"""
CSV Logger Module
Handles logging of resume submissions and analysis results to CSV files
"""

import os
import csv
import logging
from datetime import datetime
from typing import Dict, Any, List
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVLogger:
    def __init__(self, log_directory="logs"):
        """
        Initialize CSV Logger
        
        Args:
            log_directory: Directory to store CSV log files
        """
        self.log_directory = log_directory
        self.submissions_file = os.path.join(log_directory, "resume_submissions.csv")
        self.analysis_file = os.path.join(log_directory, "analysis_results.csv")
        
        # Create log directory if it doesn't exist
        os.makedirs(log_directory, exist_ok=True)
        
        # Initialize CSV files with headers if they don't exist
        self._initialize_csv_files()
    
    def _initialize_csv_files(self):
        """Initialize CSV files with appropriate headers"""
        # Submissions log headers
        submissions_headers = [
            'timestamp', 'filename', 'user_name', 'user_email', 'job_category',
            'file_size_mb', 'ats_score', 'passed_ats', 'email_sent', 'status'
        ]
        
        # Analysis log headers
        analysis_headers = [
            'timestamp', 'filename', 'user_name', 'ats_score', 'job_category',
            'format_compatibility_score', 'keyword_matching_score', 'readability_score',
            'structure_organization_score', 'contact_information_score',
            'total_recommendations', 'email_sent', 'processing_time_seconds'
        ]
        
        # Create submissions file if it doesn't exist
        if not os.path.exists(self.submissions_file):
            with open(self.submissions_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(submissions_headers)
            logger.info(f"Created submissions log file: {self.submissions_file}")
        
        # Create analysis file if it doesn't exist
        if not os.path.exists(self.analysis_file):
            with open(self.analysis_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(analysis_headers)
            logger.info(f"Created analysis log file: {self.analysis_file}")
    
    def log_submission(self, submission_data: Dict[str, Any]):
        """
        Log a resume submission
        
        Args:
            submission_data: Dictionary containing submission information
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Prepare submission row
            submission_row = [
                timestamp,
                submission_data.get('filename', ''),
                submission_data.get('user_name', ''),
                submission_data.get('user_email', ''),
                submission_data.get('job_category', ''),
                submission_data.get('file_size_mb', 0),
                submission_data.get('ats_score', 0),
                submission_data.get('passed_ats', False),
                submission_data.get('email_sent', False),
                submission_data.get('status', 'processed')
            ]
            
            # Write to submissions CSV
            with open(self.submissions_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(submission_row)
            
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
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            detailed_analysis = analysis_data.get('detailed_analysis', {})
            
            # Extract individual scores
            format_score = detailed_analysis.get('format_compatibility', {}).get('score', 0)
            keyword_score = detailed_analysis.get('keyword_matching', {}).get('score', 0)
            readability_score = detailed_analysis.get('readability', {}).get('score', 0)
            structure_score = detailed_analysis.get('structure_organization', {}).get('score', 0)
            contact_score = detailed_analysis.get('contact_information', {}).get('score', 0)
            
            # Count total recommendations
            total_recommendations = 0
            for category_analysis in detailed_analysis.values():
                if isinstance(category_analysis, dict) and 'recommendations' in category_analysis:
                    total_recommendations += len(category_analysis['recommendations'])
            
            # Prepare analysis row
            analysis_row = [
                timestamp,
                analysis_data.get('filename', ''),
                analysis_data.get('user_name', ''),
                analysis_data.get('ats_score', 0),
                analysis_data.get('job_category', ''),
                format_score,
                keyword_score,
                readability_score,
                structure_score,
                contact_score,
                total_recommendations,
                analysis_data.get('email_sent', False),
                analysis_data.get('processing_time', 0)
            ]
            
            # Write to analysis CSV
            with open(self.analysis_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(analysis_row)
            
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
            if not os.path.exists(self.submissions_file):
                return {'error': 'No submissions log found'}
            
            df = pd.read_csv(self.submissions_file)
            
            if df.empty:
                return {'total_submissions': 0}
            
            summary = {
                'total_submissions': len(df),
                'total_passed': len(df[df['passed_ats'] == True]),
                'total_failed': len(df[df['passed_ats'] == False]),
                'pass_rate': (len(df[df['passed_ats'] == True]) / len(df) * 100) if len(df) > 0 else 0,
                'average_score': df['ats_score'].mean() if 'ats_score' in df.columns else 0,
                'emails_sent': len(df[df['email_sent'] == True]),
                'top_job_categories': df['job_category'].value_counts().head(5).to_dict() if 'job_category' in df.columns else {},
                'submissions_last_24h': len(df[pd.to_datetime(df['timestamp']) > (datetime.now() - pd.Timedelta(days=1))]) if 'timestamp' in df.columns else 0,
                'submissions_last_week': len(df[pd.to_datetime(df['timestamp']) > (datetime.now() - pd.Timedelta(days=7))]) if 'timestamp' in df.columns else 0
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
            if not os.path.exists(self.submissions_file):
                return []
            
            df = pd.read_csv(self.submissions_file)
            
            if df.empty:
                return []
            
            # Sort by timestamp and get recent submissions
            df_sorted = df.sort_values('timestamp', ascending=False).head(limit)
            
            return df_sorted.to_dict('records')
            
        except Exception as e:
            logger.error(f"Failed to get recent submissions: {str(e)}")
            return []
    
    def export_data(self, start_date: str = None, end_date: str = None, 
                   export_format: str = 'csv') -> str:
        """
        Export data within date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            export_format: Export format ('csv' or 'excel')
            
        Returns:
            Path to exported file
        """
        try:
            if not os.path.exists(self.submissions_file):
                raise ValueError("No submissions data found")
            
            df = pd.read_csv(self.submissions_file)
            
            if df.empty:
                raise ValueError("No data to export")
            
            # Filter by date range if provided
            if start_date or end_date:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                if start_date:
                    df = df[df['timestamp'] >= start_date]
                
                if end_date:
                    df = df[df['timestamp'] <= end_date]
            
            # Generate export filename
            timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if export_format.lower() == 'excel':
                export_path = os.path.join(self.log_directory, f'export_{timestamp_str}.xlsx')
                df.to_excel(export_path, index=False)
            else:
                export_path = os.path.join(self.log_directory, f'export_{timestamp_str}.csv')
                df.to_csv(export_path, index=False)
            
            logger.info(f"Data exported to: {export_path}")
            return export_path
            
        except Exception as e:
            logger.error(f"Failed to export data: {str(e)}")
            raise
    
    def cleanup_old_logs(self, days_to_keep: int = 90):
        """
        Clean up old log entries
        
        Args:
            days_to_keep: Number of days of logs to keep
        """
        try:
            cutoff_date = datetime.now() - pd.Timedelta(days=days_to_keep)
            
            for file_path in [self.submissions_file, self.analysis_file]:
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path)
                    
                    if not df.empty and 'timestamp' in df.columns:
                        df['timestamp'] = pd.to_datetime(df['timestamp'])
                        df_filtered = df[df['timestamp'] >= cutoff_date]
                        
                        # Save filtered data
                        df_filtered.to_csv(file_path, index=False)
                        
                        removed_count = len(df) - len(df_filtered)
                        if removed_count > 0:
                            logger.info(f"Cleaned up {removed_count} old entries from {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old logs: {str(e)}")


# Convenience functions for easy usage
def log_resume_submission(filename: str, user_name: str = "", user_email: str = "", 
                         job_category: str = "", file_size_mb: float = 0,
                         ats_score: int = 0, passed_ats: bool = False,
                         email_sent: bool = False, status: str = "processed"):
    """
    Simple function to log a resume submission
    """
    logger_instance = CSVLogger()
    
    submission_data = {
        'filename': filename,
        'user_name': user_name,
        'user_email': user_email,
        'job_category': job_category,
        'file_size_mb': file_size_mb,
        'ats_score': ats_score,
        'passed_ats': passed_ats,
        'email_sent': email_sent,
        'status': status
    }
    
    logger_instance.log_submission(submission_data)


def log_resume_analysis(filename: str, user_name: str = "", ats_score: int = 0,
                       job_category: str = "", detailed_analysis: Dict = None,
                       email_sent: bool = False, processing_time: float = 0):
    """
    Simple function to log analysis results
    """
    logger_instance = CSVLogger()
    
    analysis_data = {
        'filename': filename,
        'user_name': user_name,
        'ats_score': ats_score,
        'job_category': job_category,
        'detailed_analysis': detailed_analysis or {},
        'email_sent': email_sent,
        'processing_time': processing_time
    }
    
    logger_instance.log_analysis(analysis_data)


def get_dashboard_data() -> Dict[str, Any]:
    """
    Get data for admin dashboard
    """
    logger_instance = CSVLogger()
    return logger_instance.get_submissions_summary()
