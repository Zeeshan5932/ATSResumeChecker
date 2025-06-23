"""
ATS Resume Checker Utilities Package
Contains modules for resume parsing, ATS analysis, and email sending
"""

from .parser import ResumeParser
from .ats_checker import ATSChecker
from .email_sender import EmailSender

__version__ = "1.0.0"
__author__ = "ATS Resume Checker Team"

__all__ = [
    'ResumeParser',
    'ATSChecker', 
    'EmailSender'
]
