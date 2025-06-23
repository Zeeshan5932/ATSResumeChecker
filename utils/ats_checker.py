"""
ATS Checker Module
Analyzes resume for ATS compatibility and provides scoring
"""

import re
import logging
import sys
import os
from typing import Dict, List, Tuple

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from config import ATS_THRESHOLDS, ATS_CRITERIA_WEIGHTS, ATS_FORMATTING_RULES, get_job_keywords
except ImportError:
    # Fallback values if config is not available
    ATS_THRESHOLDS = {'excellent': 85, 'good': 70, 'average': 55, 'poor': 40}
    ATS_CRITERIA_WEIGHTS = {'format_compatibility': 25, 'keyword_matching': 30, 'readability': 20, 'structure_organization': 15, 'contact_information': 10}
    ATS_FORMATTING_RULES = {}
    def get_job_keywords(category='general'):
        return ["Python", "SQL", "machine learning", "project", "team", "problem-solving"]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# === Simple Functions (as requested) ===

KEYWORDS = ["Python", "SQL", "machine learning", "project", "team", "problem-solving", 
           "JavaScript", "Java", "React", "Node.js", "API", "database", "Git", "Agile"]


def check_formatting_issues(text):
    """Simple formatting check"""
    penalties = 0
    text_lower = text.lower()
    
    # Penalize for potential formatting issues
    if "table" in text_lower:
        penalties += 10
    if "graphic" in text_lower or "image" in text_lower:
        penalties += 10
    if "header" in text_lower or "footer" in text_lower:
        penalties += 5
    
    return penalties


def keyword_match_score(text):
    """Simple keyword matching"""
    text_lower = text.lower()
    count = sum(1 for kw in KEYWORDS if kw.lower() in text_lower)
    return int((count / len(KEYWORDS)) * 100)


def check_ats(text):
    """Simple ATS check function"""
    if not text or len(text.strip()) < 50:
        return 0
    
    # Basic scoring
    score = keyword_match_score(text)
    penalty = check_formatting_issues(text)
    
    # Basic length check
    word_count = len(text.split())
    if word_count < 100:
        penalty += 20
    elif word_count > 1000:
        penalty += 10
    
    final_score = max(score - penalty, 0)
    return min(final_score, 100)


def get_detailed_analysis(text, job_category='general'):
    """
    Get detailed analysis of the resume
    
    Args:
        text: Resume text content
        job_category: Job category for analysis
        
    Returns:
        Dictionary with detailed analysis
    """
    if not text or len(text.strip()) < 50:
        return {
            'overall_score': 0,
            'keyword_score': 0,
            'formatting_score': 0,
            'length_score': 0,
            'recommendations': ['Resume text is too short or empty'],
            'found_keywords': [],
            'missing_keywords': KEYWORDS[:5]
        }
    
    # Get scores
    keyword_score = keyword_match_score(text)
    formatting_penalty = check_formatting_issues(text)
    formatting_score = max(100 - formatting_penalty, 0)
    
    # Length analysis
    word_count = len(text.split())
    if 300 <= word_count <= 800:
        length_score = 100
    elif 200 <= word_count < 300 or 800 < word_count <= 1200:
        length_score = 80
    elif 100 <= word_count < 200 or 1200 < word_count <= 1500:
        length_score = 60
    else:
        length_score = 40
    
    # Overall score
    overall_score = (keyword_score * 0.4 + formatting_score * 0.3 + length_score * 0.3)
    
    # Find keywords
    text_lower = text.lower()
    found_keywords = [kw for kw in KEYWORDS if kw.lower() in text_lower]
    missing_keywords = [kw for kw in KEYWORDS if kw.lower() not in text_lower]
    
    # Generate recommendations
    recommendations = []
    
    if keyword_score < 50:
        recommendations.append(f"Include more relevant keywords. Missing: {', '.join(missing_keywords[:3])}")
    
    if formatting_penalty > 20:
        recommendations.append("Simplify formatting - avoid tables, images, and complex layouts")
    
    if word_count < 300:
        recommendations.append("Expand your resume content - add more details about your experience")
    elif word_count > 1000:
        recommendations.append("Consider condensing your resume - focus on most relevant information")
    
    if not any(contact in text_lower for contact in ['@', 'email', 'phone']):
        recommendations.append("Ensure contact information (email, phone) is clearly visible")
    
    if len(recommendations) == 0:
        recommendations.append("Great job! Your resume looks well-optimized for ATS systems.")    # Calculate contact score
    contact_score = 100 if any(contact in text_lower for contact in ['@', 'email', 'phone']) else 50
    structure_score = max(formatting_score, length_score)
    
    return {
        'overall_score': round(overall_score, 1),
        'word_count': word_count,
        'recommendations': recommendations,
        'found_keywords': found_keywords,
        'missing_keywords': missing_keywords[:10],
        'job_category': job_category,
        # Consistent nested structure for compatibility with email_sender and csv_logger
        'format_compatibility': {
            'score': formatting_score,
            'feedback': ['Good formatting' if formatting_score > 70 else 'Formatting needs improvement']
        },
        'keyword_matching': {
            'score': keyword_score,
            'feedback': [f'Found {len(found_keywords)} relevant keywords'],
            'found_keywords': found_keywords,
            'missing_keywords': missing_keywords[:5]
        },
        'readability': {
            'score': length_score,
            'feedback': [f'Word count: {word_count} words'],
            'word_count': word_count
        },
        'structure_organization': {
            'score': structure_score,
            'feedback': ['Good structure' if structure_score > 70 else 'Structure needs improvement']
        },
        'contact_information': {
            'score': contact_score,
            'feedback': ['Contact info found' if contact_score > 50 else 'Missing contact information']
        }
    }


# === Advanced Class (existing functionality) ===

class ATSChecker:
    def __init__(self):
        """Initialize ATS Checker with configuration"""
        self.thresholds = ATS_THRESHOLDS
        self.criteria_weights = ATS_CRITERIA_WEIGHTS
        self.formatting_rules = ATS_FORMATTING_RULES
    
    def check_format_compatibility(self, parsed_resume: Dict) -> Dict:
        """
        Check resume format compatibility with ATS systems
        
        Args:
            parsed_resume: Parsed resume data
            
        Returns:
            Dictionary with format compatibility score and feedback
        """
        score = 0
        feedback = []
        max_score = 100
        
        text = parsed_resume.get('raw_text', '')
        
        # Check for problematic elements
        issues = []
        
        # Check for images/graphics (indicated by certain patterns)
        if re.search(r'(image|img|picture|photo|graphic)', text.lower()):
            issues.append("Possible images detected - ATS may not process these")
            score -= 20
        
        # Check for tables (indicated by tab characters or specific patterns)
        if '\t' in text or re.search(r'\|.*\|', text):
            issues.append("Possible tables detected - may cause parsing issues")
            score -= 15
        
        # Check for text boxes or columns (irregular spacing patterns)
        lines = text.split('\n')
        irregular_spacing = sum(1 for line in lines if len(line.split()) > 20)
        if irregular_spacing > len(lines) * 0.3:
            issues.append("Irregular text spacing detected - may indicate complex formatting")
            score -= 10
        
        # Check for standard font usage (can't be perfectly determined from text)
        # We'll assume good formatting if text is clean
        clean_text_ratio = len(re.sub(r'[^\w\s]', '', text)) / len(text) if text else 0
        if clean_text_ratio < 0.7:
            issues.append("High number of special characters - may indicate formatting issues")
            score -= 10
        
        # Positive checks
        if parsed_resume.get('name'):
            score += 15
            feedback.append("✓ Clear name identification")
        
        if parsed_resume.get('email'):
            score += 15
            feedback.append("✓ Email address found")
        
        if parsed_resume.get('phone'):
            score += 10
            feedback.append("✓ Phone number found")
        
        # Check for clear section structure
        if len(parsed_resume.get('education', [])) > 0:
            score += 10
            feedback.append("✓ Education section identified")
        
        if len(parsed_resume.get('experience', [])) > 0:
            score += 15
            feedback.append("✓ Experience section identified")
        
        if len(parsed_resume.get('skills', [])) > 0:
            score += 10
            feedback.append("✓ Skills section identified")
        
        # Ensure score is within bounds
        score = max(0, min(100, score + 50))  # Base score of 50
        
        # Add issues to feedback
        feedback.extend([f"⚠ {issue}" for issue in issues])
        
        return {
            'score': score,
            'feedback': feedback,
            'issues': issues
        }
    
    def check_keyword_matching(self, parsed_resume: Dict, job_category: str = 'general') -> Dict:
        """
        Check how well the resume matches relevant keywords
        
        Args:
            parsed_resume: Parsed resume data
            job_category: Job category for keyword matching
            
        Returns:
            Dictionary with keyword matching score and analysis
        """
        text = parsed_resume.get('raw_text', '').lower()
        keywords = [kw.lower() for kw in get_job_keywords(job_category)]
        
        found_keywords = []
        missing_keywords = []
        
        for keyword in keywords:
            if keyword in text:
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        # Calculate score based on keyword match percentage
        match_percentage = len(found_keywords) / len(keywords) * 100 if keywords else 0
        score = min(100, match_percentage * 1.2)  # Slight bonus for good matches
        
        feedback = [
            f"✓ Found {len(found_keywords)} out of {len(keywords)} relevant keywords",
            f"Match rate: {match_percentage:.1f}%"
        ]
        
        if found_keywords:
            feedback.append(f"✓ Matched keywords: {', '.join(found_keywords[:10])}")
        
        if missing_keywords and len(missing_keywords) <= 10:
            feedback.append(f"⚠ Consider adding: {', '.join(missing_keywords[:5])}")
        
        return {
            'score': score,
            'feedback': feedback,
            'found_keywords': found_keywords,
            'missing_keywords': missing_keywords,
            'match_percentage': match_percentage
        }
    
    def check_readability(self, parsed_resume: Dict) -> Dict:
        """
        Check resume readability and text quality
        
        Args:
            parsed_resume: Parsed resume data
            
        Returns:
            Dictionary with readability score and feedback
        """
        text = parsed_resume.get('raw_text', '')
        score = 0
        feedback = []
        
        if not text:
            return {'score': 0, 'feedback': ['No text found']}
        
        # Basic readability metrics
        word_count = parsed_resume.get('word_count', 0)
        sentences = text.split('.')
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Optimal word count (300-800 words)
        if 300 <= word_count <= 800:
            score += 30
            feedback.append(f"✓ Good word count: {word_count} words")
        elif word_count < 300:
            score += 15
            feedback.append(f"⚠ Word count low: {word_count} words (consider adding more detail)")
        else:
            score += 20
            feedback.append(f"⚠ Word count high: {word_count} words (consider condensing)")
        
        # Average sentence length
        if sentence_count > 0:
            avg_sentence_length = word_count / sentence_count
            if 10 <= avg_sentence_length <= 20:
                score += 25
                feedback.append("✓ Good average sentence length")
            else:
                score += 15
                feedback.append("⚠ Consider varying sentence length for better readability")
        
        # Check for bullet points (good for ATS)
        bullet_indicators = ['•', '·', '-', '*']
        has_bullets = any(indicator in text for indicator in bullet_indicators)
        if has_bullets:
            score += 20
            feedback.append("✓ Uses bullet points effectively")
        else:
            score += 5
            feedback.append("⚠ Consider using bullet points for better organization")
        
        # Check for excessive special characters
        special_char_ratio = len(re.sub(r'[a-zA-Z0-9\s]', '', text)) / len(text)
        if special_char_ratio < 0.1:
            score += 15
            feedback.append("✓ Clean text with minimal special characters")
        else:
            score += 5
            feedback.append("⚠ High ratio of special characters may cause parsing issues")
        
        # Check for proper capitalization
        capitalized_words = len(re.findall(r'\b[A-Z][a-z]+', text))
        total_words = len(text.split())
        if total_words > 0 and capitalized_words / total_words > 0.1:
            score += 10
            feedback.append("✓ Proper capitalization usage")
        
        return {
            'score': min(100, score),
            'feedback': feedback,
            'word_count': word_count,
            'sentence_count': sentence_count
        }
    
    def check_structure_organization(self, parsed_resume: Dict) -> Dict:
        """
        Check resume structure and organization
        
        Args:
            parsed_resume: Parsed resume data
            
        Returns:
            Dictionary with structure score and feedback
        """
        score = 0
        feedback = []
        
        # Check for essential sections
        has_contact = bool(parsed_resume.get('email') or parsed_resume.get('phone'))
        has_experience = len(parsed_resume.get('experience', [])) > 0
        has_education = len(parsed_resume.get('education', [])) > 0
        has_skills = len(parsed_resume.get('skills', [])) > 0
        
        section_score = 0
        if has_contact:
            section_score += 25
            feedback.append("✓ Contact information present")
        else:
            feedback.append("⚠ Missing contact information")
        
        if has_experience:
            section_score += 30
            feedback.append("✓ Experience section present")
        else:
            feedback.append("⚠ Missing experience section")
        
        if has_education:
            section_score += 25
            feedback.append("✓ Education section present")
        else:
            feedback.append("⚠ Missing education section")
        
        if has_skills:
            section_score += 20
            feedback.append("✓ Skills section present")
        else:
            feedback.append("⚠ Missing skills section")
        
        score += section_score
        
        return {
            'score': min(100, score),
            'feedback': feedback,
            'sections_found': {
                'contact': has_contact,
                'experience': has_experience,
                'education': has_education,
                'skills': has_skills
            }
        }
    
    def check_contact_information(self, parsed_resume: Dict) -> Dict:
        """
        Check quality and completeness of contact information
        
        Args:
            parsed_resume: Parsed resume data
            
        Returns:
            Dictionary with contact info score and feedback
        """
        score = 0
        feedback = []
        
        name = parsed_resume.get('name')
        email = parsed_resume.get('email')
        phone = parsed_resume.get('phone')
        
        if name:
            score += 40
            feedback.append(f"✓ Name found: {name}")
        else:
            feedback.append("⚠ Name not clearly identified")
        
        if email:
            score += 40
            feedback.append(f"✓ Email found: {email}")
            # Validate email format
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
            if re.match(email_pattern, email):
                score += 10
                feedback.append("✓ Email format is valid")
            else:
                feedback.append("⚠ Email format may be invalid")
        else:
            feedback.append("⚠ Email address not found")
        
        if phone:
            score += 20
            feedback.append(f"✓ Phone found: {phone}")
        else:
            feedback.append("⚠ Phone number not found")
        
        return {
            'score': min(100, score),
            'feedback': feedback,
            'contact_details': {
                'name': name,
                'email': email,
                'phone': phone
            }
        }
    
    def calculate_overall_score(self, individual_scores: Dict) -> Dict:
        """
        Calculate weighted overall ATS score
        
        Args:
            individual_scores: Dictionary of individual criterion scores
            
        Returns:
            Dictionary with overall score and rating
        """
        weighted_score = 0
        
        for criterion, weight in self.criteria_weights.items():
            score = individual_scores.get(criterion, {}).get('score', 0)
            weighted_score += (score * weight / 100)
        
        # Determine rating based on thresholds
        if weighted_score >= self.thresholds['excellent']:
            rating = 'Excellent'
            rating_description = 'Your resume is highly ATS-compatible and likely to pass through automated screening systems.'
        elif weighted_score >= self.thresholds['good']:
            rating = 'Good'
            rating_description = 'Your resume has good ATS compatibility with room for minor improvements.'
        elif weighted_score >= self.thresholds['average']:
            rating = 'Average'
            rating_description = 'Your resume may face some challenges with ATS systems. Consider implementing the suggested improvements.'
        elif weighted_score >= self.thresholds['poor']:
            rating = 'Poor'
            rating_description = 'Your resume may have difficulty passing through ATS systems. Significant improvements are recommended.'
        else:
            rating = 'Very Poor'
            rating_description = 'Your resume is likely to be rejected by ATS systems. Major revisions are necessary.'
        
        return {
            'overall_score': round(weighted_score, 1),
            'rating': rating,
            'rating_description': rating_description,
            'individual_scores': individual_scores
        }
    
    def analyze_resume(self, parsed_resume: Dict, job_category: str = 'general') -> Dict:
        """
        Perform comprehensive ATS analysis of the resume
        
        Args:
            parsed_resume: Parsed resume data
            job_category: Job category for keyword matching
            
        Returns:
            Complete ATS analysis results
        """
        try:
            # Perform individual checks
            format_check = self.check_format_compatibility(parsed_resume)
            keyword_check = self.check_keyword_matching(parsed_resume, job_category)
            readability_check = self.check_readability(parsed_resume)
            structure_check = self.check_structure_organization(parsed_resume)
            contact_check = self.check_contact_information(parsed_resume)
            
            individual_scores = {
                'format_compatibility': format_check,
                'keyword_matching': keyword_check,
                'readability': readability_check,
                'structure_organization': structure_check,
                'contact_information': contact_check
            }
            
            # Calculate overall score
            overall_analysis = self.calculate_overall_score(individual_scores)
            
            # Compile recommendations
            recommendations = self._generate_recommendations(individual_scores, overall_analysis)
            
            result = {
                'success': True,
                'overall_analysis': overall_analysis,
                'detailed_analysis': individual_scores,
                'recommendations': recommendations,
                'job_category': job_category
            }
            
            logger.info(f"ATS analysis completed. Overall score: {overall_analysis['overall_score']}")
            return result
            
        except Exception as e:
            logger.error(f"Error during ATS analysis: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_recommendations(self, individual_scores: Dict, overall_analysis: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Format recommendations
        format_score = individual_scores.get('format_compatibility', {}).get('score', 0)
        if format_score < 70:
            recommendations.extend([
                "Use a simple, clean format without tables, text boxes, or images",
                "Stick to standard fonts like Arial, Calibri, or Times New Roman",
                "Avoid headers and footers that may not be parsed correctly"
            ])
        
        # Keyword recommendations
        keyword_score = individual_scores.get('keyword_matching', {}).get('score', 0)
        if keyword_score < 60:
            missing_keywords = individual_scores.get('keyword_matching', {}).get('missing_keywords', [])
            if missing_keywords:
                recommendations.append(f"Include relevant keywords: {', '.join(missing_keywords[:5])}")
            recommendations.append("Tailor your resume to include industry-specific terminology")
        
        # Readability recommendations
        readability_score = individual_scores.get('readability', {}).get('score', 0)
        if readability_score < 70:
            recommendations.extend([
                "Use bullet points to organize information clearly",
                "Keep sentences concise and easy to read",
                "Aim for 300-800 words total"
            ])
        
        # Structure recommendations
        structure_score = individual_scores.get('structure_organization', {}).get('score', 0)
        if structure_score < 70:
            sections = individual_scores.get('structure_organization', {}).get('sections_found', {})
            if not sections.get('contact'):
                recommendations.append("Ensure contact information is clearly visible at the top")
            if not sections.get('experience'):
                recommendations.append("Include a detailed work experience section")
            if not sections.get('skills'):
                recommendations.append("Add a skills section with relevant technical and soft skills")
        
        # Contact information recommendations
        contact_score = individual_scores.get('contact_information', {}).get('score', 0)
        if contact_score < 70:
            recommendations.extend([
                "Include your full name, email, and phone number",
                "Use a professional email address",
                "Ensure contact information is at the top of the resume"
            ])
        
        # Overall recommendations
        overall_score = overall_analysis.get('overall_score', 0)
        if overall_score < 60:
            recommendations.insert(0, "Consider a major revision focusing on ATS compatibility")
        elif overall_score < 80:
            recommendations.insert(0, "Your resume is good but could benefit from minor improvements")
        
        return recommendations[:10]  # Limit to top 10 recommendations
