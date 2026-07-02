"""
Quick Setup Script for TruthLens AI
Run this script to set up the environment and train models
"""

import os
import subprocess
import sys


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*70}")
    print(f"📍 {description}")
    print('='*70)
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e}")
        return False


def main():
    """Run setup process"""
    print("\n" + "="*70)
    print("🚀 TruthLens AI - Quick Setup")
    print("="*70)
    
    # Check Python version
    print(f"\n🐍 Python Version: {sys.version}")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("\n❌ Failed to install dependencies")
        return
    
    # Create necessary directories
    print(f"\n{'='*70}")
    print("📁 Creating directories...")
    print('='*70)
    
    directories = ['models', 'history', 'reports', 'data', '.streamlit']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ {directory}/")
    
    # Download NLTK data
    print(f"\n{'='*70}")
    print("📥 Downloading NLTK data...")
    print('='*70)
    
    import nltk
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        print("✅ NLTK data downloaded successfully")
    except Exception as e:
        print(f"⚠️ NLTK download warning: {e}")
    
    # Train models
    if not run_command("python train_models.py", "Training ML models"):
        print("\n⚠️ Model training failed, but you can try manually later")
    
    print(f"\n{'='*70}")
    print("✅ Setup Complete!")
    print('='*70)
    print("\nTo start the application, run:")
    print("  streamlit run app.py")
    print("\nThe app will open at http://localhost:8501")


if __name__ == "__main__":
    main()
