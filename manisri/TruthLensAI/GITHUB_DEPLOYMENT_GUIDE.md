# 🚀 GitHub Deployment Guide for TruthLens AI

## Complete Step-by-Step Instructions

### Prerequisites
- GitHub Account (create one at github.com if you don't have it)
- Git installed on your computer
- Project folder ready

---

## Step 1: Install Git (If Not Already Installed)

### Windows:
1. Download from: https://git-scm.com/download/win
2. Run the installer with default settings
3. Restart your terminal/PowerShell

### Verify Installation:
```bash
git --version
```

---

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in repository name: **TruthLensAI**
3. Description: "Intelligent Misinformation Detection and Content Credibility Assessment System"
4. Select **Public** (for open source)
5. Check "Add a README file" - **NO** (we have one)
6. Choose license: **MIT License**
7. Click **Create repository**

---

## Step 3: Configure Git (First Time Only)

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.email@github.com"
```

---

## Step 4: Initialize Repository Locally

Navigate to your TruthLensAI folder and run:

```bash
cd "c:\Users\manis\OneDrive\Desktop\manisri\TruthLensAI"

git init
git add .
git commit -m "Initial commit: TruthLens AI - Intelligent Misinformation Detection System"
```

---

## Step 5: Connect to GitHub

After creating the repository on GitHub, you'll see a URL like:
```
https://github.com/YOUR_USERNAME/TruthLensAI.git
```

Run these commands:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/TruthLensAI.git
git push -u origin main
```

When prompted, enter your GitHub credentials:
- **Username**: your-github-username
- **Password**: Use a Personal Access Token (see below)

---

## Step 6: Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: "TruthLens AI Deployment"
4. Select scopes:
   - ✅ repo (Full control of private repositories)
   - ✅ workflow
   - ✅ write:packages
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. Use this token as password when pushing

---

## Quick Command Sequence

```bash
# Navigate to project
cd "c:\Users\manis\OneDrive\Desktop\manisri\TruthLensAI"

# Configure Git (first time)
git config --global user.name "Your Name"
git config --global user.email "your.email@github.com"

# Initialize repository
git init
git add .
git commit -m "Initial commit: TruthLens AI v1.0.0"

# Connect to GitHub
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/TruthLensAI.git

# Push to GitHub
git push -u origin main
```

---

## Deploy to Streamlit Cloud (Optional)

1. Push to GitHub first (above steps)
2. Go to: https://streamlit.io/cloud
3. Click "New app"
4. Connect GitHub account
5. Select: YOUR_USERNAME / TruthLensAI / demo_app.py
6. Click "Deploy"

Your app will be live at: `https://[random-name].streamlit.app`

---

## Project Files Included

✅ app.py - Full-featured Streamlit application
✅ demo_app.py - Fast demo version
✅ train_model.py - ML model training module
✅ train_models.py - Model training script
✅ predict.py - Prediction engine
✅ preprocess.py - Text preprocessing
✅ utils.py - Utility functions
✅ requirements.txt - Python dependencies
✅ README.md - Documentation
✅ .gitignore - Git ignore rules
✅ models/ - Trained ML models
✅ history/ - Prediction history storage
✅ data/ - Sample datasets

---

## Troubleshooting

### Git not recognized
```bash
# Add Git to PATH or reinstall
# Windows: https://git-scm.com/download/win
```

### Authentication failed
```bash
# Use Personal Access Token instead of password
# Get token from: https://github.com/settings/tokens
```

### Push rejected
```bash
# Pull latest changes first
git pull origin main

# Then push
git push origin main
```

### Large files warning
```bash
# If models are too large, use Git LFS
git lfs install
git lfs track "*.pkl"
git add .gitattributes
```

---

## Useful Git Commands

```bash
# Check status
git status

# View commit history
git log

# Add specific file
git add filename.py

# Commit with message
git commit -m "Your message"

# Push changes
git push origin main

# Pull latest
git pull origin main

# Create new branch
git checkout -b feature-branch

# Switch branch
git checkout main
```

---

## Next Steps After Deployment

1. **Share your repository**: Copy the GitHub URL
2. **Add to portfolio**: Link from your resume/portfolio
3. **Set up CI/CD**: Add GitHub Actions for automated testing
4. **Deploy to cloud**: Use Streamlit Cloud, Heroku, or AWS
5. **Contribute**: Accept pull requests and collaborate

---

## Support

📚 **Git Documentation**: https://git-scm.com/doc
🎬 **GitHub Guides**: https://guides.github.com
🚀 **Streamlit Cloud**: https://docs.streamlit.io/streamlit-cloud

---

**Created**: 2026-07-02
**TruthLens AI v1.0.0** - Production Ready ✅
