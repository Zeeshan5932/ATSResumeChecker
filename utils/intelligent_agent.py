"""
Intelligent ATS Agent Module
Automatically detects job categories and provides smart resume analysis
"""

import re
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class IntelligentATSAgent:
    def __init__(self):
        # Define comprehensive keywords for each job category
        self.job_categories = {
            'education': [
                'curriculum', 'classroom', 'student', 'teaching', 'lesson', 'teacher', 'school', 
                'syllabus', 'assessment', 'pedagogy', 'learning', 'education', 'instructor',
                'tutoring', 'academic', 'grade', 'course', 'training', 'workshop'
            ],
            'art': [
                'creative', 'design', 'visual', 'portfolio', 'exhibition', 'art', 'gallery', 
                'photography', 'painting', 'graphic', 'illustration', 'artistic', 'aesthetic',
                'drawing', 'sculpture', 'media', 'digital art', 'adobe', 'photoshop'
            ],
            'tech': [
                'python', 'sql', 'api', 'javascript', 'programming', 'machine learning', 
                'java', 'react', 'node.js', 'git', 'software', 'developer', 'coding',
                'database', 'algorithm', 'framework', 'backend', 'frontend', 'devops'
            ],
            'healthcare': [
                'patient', 'clinical', 'medical', 'treatment', 'health', 'nurse', 'doctor', 
                'hospital', 'therapy', 'diagnosis', 'care', 'pharmaceutical', 'surgery',
                'healthcare', 'medical records', 'patient care'
            ],
            'finance': [
                'financial', 'accounting', 'budget', 'analysis', 'audit', 'investment', 
                'tax', 'banking', 'finance', 'economics', 'portfolio', 'risk', 'trading',
                'financial planning', 'excel', 'financial modeling'
            ],
            'marketing': [
                'marketing', 'advertising', 'branding', 'campaign', 'social media', 'seo',
                'content', 'digital marketing', 'analytics', 'conversion', 'lead generation'
            ],
            'sales': [
                'sales', 'client', 'customer', 'revenue', 'negotiation', 'pipeline',
                'crm', 'quota', 'relationship', 'business development'
            ]        }
        
        # Weight multipliers for different sections
        self.section_weights = {
            'title': 3.0,      # Job titles carry more weight
            'skills': 2.0,     # Skills section is important
            'experience': 1.5, # Work experience descriptions
            'summary': 1.5,    # Professional summary
            'general': 1.0     # General text
        }

    def auto_detect_job_category(self, resume_text: str) -> Tuple[str, Dict[str, int]]:
        """
        Automatically detect the most relevant job category based on keyword matches.
        Returns tuple of (category, scores_dict)
        """
        scores = {}
        resume_lower = resume_text.lower()
        
        for category, keywords in self.job_categories.items():
            score = 0
            for keyword in keywords:
                # Count occurrences of each keyword
                count = resume_lower.count(keyword.lower())
                score += count
            scores[category] = score
        
        # Get the category with highest score
        best_category = max(scores, key=scores.get) if scores else 'general'
        
        # If no keywords found, return 'general'
        if scores[best_category] == 0:
            best_category = 'general'
            
        logger.info(f"Category detection scores: {scores}")
        logger.info(f"Detected category: {best_category}")
        
        return best_category, scores

    def analyze_resume(self, resume_text: str, target_category: Optional[str] = None) -> Dict:
        """
        Analyze resume using detected or provided job category.
        Returns detailed analysis with scoring and recommendations.
        """
        if not target_category:
            target_category, category_scores = self.auto_detect_job_category(resume_text)
        else:
            _, category_scores = self.auto_detect_job_category(resume_text)
            
        keywords = self.job_categories.get(target_category, [])
        resume_lower = resume_text.lower()
        
        # Find matching keywords
        found_keywords = []
        missing_keywords = []
        
        for keyword in keywords:
            if keyword.lower() in resume_lower:
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        # Calculate keyword match percentage
        total_keywords = len(keywords)
        found_count = len(found_keywords)
        keyword_match_percentage = (found_count / total_keywords * 100) if total_keywords > 0 else 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            target_category, found_keywords, missing_keywords, keyword_match_percentage
        )
        
        return {
            'detected_category': target_category,
            'category_scores': category_scores,
            'found_keywords': found_keywords,
            'missing_keywords': missing_keywords[:10],  # Limit to top 10 missing
            'keyword_match_percentage': round(keyword_match_percentage, 1),
            'recommendations': recommendations,
            'total_keywords_in_category': total_keywords,
            'found_keywords_count': found_count
        }

    def _generate_recommendations(self, category: str, found_keywords: List[str], 
                                missing_keywords: List[str], match_percentage: float) -> List[str]:
        """Generate specific recommendations based on analysis results."""
        recommendations = []
        
        if match_percentage < 30:
            recommendations.append(f"❌ Low keyword match ({match_percentage:.1f}%). Consider adding more {category}-specific terms.")
            
        if match_percentage < 50:
            # Prioritize most important missing keywords
            priority_missing = missing_keywords[:5]
            if priority_missing:
                recommendations.append(f"📝 Add these important {category} keywords: {', '.join(priority_missing)}")
                
        if match_percentage >= 70:
            recommendations.append(f"✅ Good keyword coverage ({match_percentage:.1f}%) for {category} field.")
            
        # Category-specific recommendations
        if category == 'tech' and 'git' not in [k.lower() for k in found_keywords]:
            recommendations.append("💻 Add version control experience (Git, GitHub)")
            
        if category == 'education' and 'curriculum' not in [k.lower() for k in found_keywords]:
            recommendations.append("📚 Mention curriculum development or educational methodology")
            
        if category == 'art' and 'portfolio' not in [k.lower() for k in found_keywords]:
            recommendations.append("🎨 Include portfolio or exhibition experience")
            
        return recommendations

    def generate_smart_recommendations(self, resume_text: str, job_description: Optional[str] = None) -> Dict:
        """
        Generate context-aware recommendations, optionally using a job description.
        This is the main method to call for intelligent analysis.
        """
        if job_description:
            return self._analyze_against_job_posting(resume_text, job_description)
        else:
            return self.analyze_resume(resume_text)

    def _analyze_against_job_posting(self, resume_text: str, job_description: str) -> Dict:
        """Compare resume against specific job requirements."""
        # Extract keywords from job description
        job_keywords = self._extract_important_keywords(job_description)
        resume_keywords = self._extract_important_keywords(resume_text)
        
        # Find matches and gaps
        matching_keywords = list(set(job_keywords) & set(resume_keywords))
        missing_keywords = list(set(job_keywords) - set(resume_keywords))
        
        # Calculate match percentage
        match_percentage = (len(matching_keywords) / len(job_keywords) * 100) if job_keywords else 0
        
        recommendations = []
        if missing_keywords:
            priority_missing = missing_keywords[:8]  # Top 8 missing keywords
            recommendations.append(f"🎯 Add these keywords from job posting: {', '.join(priority_missing)}")
            
        if match_percentage >= 80:
            recommendations.append(f"🎉 Excellent match ({match_percentage:.1f}%) with job requirements!")
        elif match_percentage >= 60:
            recommendations.append(f"👍 Good match ({match_percentage:.1f}%) with job requirements.")
        else:
            recommendations.append(f"⚠️ Low match ({match_percentage:.1f}%) - consider adding more relevant keywords.")
        
        return {
            'analysis_type': 'job_posting_match',
            'job_keywords': job_keywords,
            'resume_keywords': resume_keywords,
            'matching_keywords': matching_keywords,
            'missing_keywords': missing_keywords,
            'match_percentage': round(match_percentage, 1),
            'recommendations': recommendations
        }

    def _extract_important_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text, filtering out common words."""
        import re
        
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Common stopwords to filter out
        stopwords = {
            'the', 'and', 'for', 'with', 'a', 'an', 'of', 'to', 'in', 'on', 'by', 'is', 'at', 
            'as', 'from', 'or', 'that', 'this', 'it', 'are', 'was', 'will', 'be', 'have', 
            'has', 'had', 'do', 'does', 'did', 'can', 'could', 'should', 'would', 'may', 
            'might', 'must', 'shall', 'you', 'your', 'we', 'our', 'they', 'their'
        }
        
        # Filter keywords: length > 2, not in stopwords, appears multiple times or is long
        word_counts = {}
        for word in words:
            if len(word) > 2 and word not in stopwords:
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Select important keywords
        important_keywords = []
        for word, count in word_counts.items():
            if count > 1 or len(word) > 6:  # Appears multiple times or is a long word
                important_keywords.append(word)
        
        return list(set(important_keywords))[:20]  # Return top 20 unique keywords


def test_intelligent_agent():
    """Test function to demonstrate the intelligent agent capabilities."""
    print("🤖 Testing Intelligent ATS Agent...")
    
    # Sample resume text (from your JSON file)
    teacher_resume = """
    Martha Blevins High School Teacher
    I am a committed high school teacher with years of experience in the art industry. 
    I am passionate about promoting student improvement through continuous monitoring 
    of their academic progress.
    
    High School Teacher - Cordale High School
    Mar 2022 - Aug 2025 (3 years, 5 months)
    Improved students' overall grades by 10% by facilitating discussions about 
    art appreciation and aesthetic concepts
    Increased art club participation by 5% by spearheading the annual student 
    art exhibition
    Taught creative techniques in drawing, painting, and printmaking. 
    Moderates student art club as teacher-adviser
    
    Education: Master of Fine Arts in Photography and New Media
    Skills: Graphic Design, Digital Art, Creative Thinking, Effective Communication
    """
    
    # Initialize agent
    agent = IntelligentATSAgent()
    
    # Test category detection
    print("\n📊 Category Detection:")
    category, scores = agent.auto_detect_job_category(teacher_resume)
    print(f"Detected Category: {category}")
    print(f"Scores: {scores}")
    
    # Test resume analysis
    print("\n📋 Resume Analysis:")
    analysis = agent.analyze_resume(teacher_resume)
    print(f"Category: {analysis['detected_category']}")
    print(f"Keywords Found: {analysis['found_keywords']}")
    print(f"Match Percentage: {analysis['keyword_match_percentage']}%")
    print("Recommendations:")
    for rec in analysis['recommendations']:
        print(f"  • {rec}")
    
    return analysis


if __name__ == "__main__":
    # Run test when script is executed directly
    test_intelligent_agent()
