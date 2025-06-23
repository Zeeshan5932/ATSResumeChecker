"""
Setup and Installation Script for ATS Resume Checker
This script helps set up the application with initial configuration
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"Python version {sys.version} - OK")
    return True

def install_requirements():
    """Install required packages"""
    try:
        logger.info("Installing required packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        logger.info("Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'logs',
        'resumes/uploaded_resumes',
        'backups',
        'exports'
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def create_env_file():
    """Create .env file with configuration template"""
    env_content = """# ATS Resume Checker Configuration
# Copy this file to .env and update with your settings

# Email Configuration (Required for email features)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# File Upload Settings
MAX_FILE_SIZE_MB=10
UPLOAD_FOLDER=resumes/uploaded_resumes

# ATS Scoring Thresholds
ATS_PASS_THRESHOLD=75
ATS_EXCELLENT_THRESHOLD=85

# Database (Optional - for future use)
# DATABASE_URL=sqlite:///ats_checker.db

# Cache Settings (Optional)
# CACHE_TYPE=simple
# CACHE_TIMEOUT=300

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        logger.info("Created .env file template")
    else:
        logger.info(".env file already exists")

def setup_email_configuration():
    """Interactive email configuration setup"""
    print("\n" + "="*50)
    print("EMAIL CONFIGURATION SETUP")
    print("="*50)
    print("To enable email features, you need to configure SMTP settings.")
    print("For Gmail:")
    print("1. Enable 2-factor authentication")
    print("2. Generate an app password")
    print("3. Use the app password (not your regular password)")
    print("\nYou can skip this now and configure later in the .env file")
    
    configure = input("\nWould you like to configure email now? (y/n): ").lower().strip()
    
    if configure == 'y':
        email = input("Enter your email address: ").strip()
        password = input("Enter your app password: ").strip()
        
        # Update config.py
        config_path = 'config.py'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                content = f.read()
            
            # Replace email configuration
            content = content.replace("'your_email@gmail.com'", f"'{email}'")
            content = content.replace("'your_app_password'", f"'{password}'")
            
            with open(config_path, 'w') as f:
                f.write(content)
            
            logger.info("Email configuration updated in config.py")
        
        # Update .env file
        env_path = '.env'
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                content = f.read()
            
            content = content.replace('your_email@gmail.com', email)
            content = content.replace('your_app_password', password)
            
            with open(env_path, 'w') as f:
                f.write(content)
            
            logger.info("Email configuration updated in .env file")
    else:
        print("Email configuration skipped. Update the .env file manually when ready.")

def test_imports():
    """Test if all required modules can be imported"""
    logger.info("Testing imports...")
    
    required_modules = [
        'flask',
        'pandas',
        'numpy',
        'sklearn',
        'nltk',
        'textstat',
        'PyPDF2',
        'docx'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"✓ {module}")
        except ImportError:
            logger.error(f"✗ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        logger.warning(f"Failed to import: {', '.join(failed_imports)}")
        logger.warning("Some features may not work properly")
        return False
    
    logger.info("All imports successful")
    return True

def download_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        logger.info("Downloading NLTK data...")
        
        nltk_downloads = [
            'punkt',
            'stopwords',
            'wordnet',
            'averaged_perceptron_tagger',
            'vader_lexicon'
        ]
        
        for data in nltk_downloads:
            try:
                nltk.download(data, quiet=True)
                logger.info(f"Downloaded NLTK data: {data}")
            except:
                logger.warning(f"Failed to download NLTK data: {data}")
        
        return True
    except ImportError:
        logger.warning("NLTK not available, skipping data download")
        return False

def create_startup_script():
    """Create startup script for easy launching"""
    
    # Windows batch file
    batch_content = """@echo off
echo Starting ATS Resume Checker...
echo ==============================
python app.py
pause
"""
    
    with open('start_ats_checker.bat', 'w') as f:
        f.write(batch_content)
    
    # Unix shell script
    shell_content = """#!/bin/bash
echo "Starting ATS Resume Checker..."
echo "=============================="
python3 app.py
"""
    
    with open('start_ats_checker.sh', 'w') as f:
        f.write(shell_content)
    
    # Make shell script executable on Unix systems
    if os.name != 'nt':
        os.chmod('start_ats_checker.sh', 0o755)
    
    logger.info("Created startup scripts")

def run_initial_test():
    """Run a basic test to ensure everything works"""
    try:
        logger.info("Running initial test...")
        
        # Test CSV logger
        from utils.csv_logger import CSVLogger
        csv_logger = CSVLogger()
        logger.info("✓ CSV logging system initialized")
        
        # Test email sender (just import)
        from utils.email_sender import send_congrats_email
        logger.info("✓ Email system available")
        
        logger.info("Initial test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Initial test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("="*60)
    print("ATS RESUME CHECKER - SETUP & INSTALLATION")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    create_directories()
    
    # Install requirements
    if not install_requirements():
        logger.error("Setup failed during package installation")
        return False
    
    # Create configuration files
    create_env_file()
    
    # Test imports
    if not test_imports():
        logger.warning("Some imports failed, but continuing...")
    
    # Download NLTK data
    download_nltk_data()
    
    # Create startup scripts
    create_startup_script()
    
    # Email configuration
    setup_email_configuration()
    
    # Run initial test
    if run_initial_test():
        logger.info("Setup completed successfully!")
    else:
        logger.warning("Setup completed with warnings")
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("Next steps:")
    print("1. Configure email settings in .env file (if not done)")
    print("2. Run 'python app.py' to start the application")
    print("3. Open http://localhost:5000 in your browser")
    print("4. Or use start_ats_checker.bat (Windows) / start_ats_checker.sh (Unix)")
    print("="*60)
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
    except Exception as e:
        logger.error(f"Setup failed with error: {e}")
        sys.exit(1)
