# TruthLens AI - Final Deployment Script
# Simple and reliable GitHub deployment

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TruthLens AI - GitHub Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set project path
$ProjectPath = "c:\Users\manis\OneDrive\Desktop\manisri\TruthLensAI"
cd $ProjectPath

# Refresh PATH to ensure Git is available
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Step 1: Verify Git is installed
Write-Host "Step 1: Checking Git installation..." -ForegroundColor Cyan
try {
    $gitVersion = git --version
    Write-Host "[OK] $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Step 2: Collect GitHub information
Write-Host ""
Write-Host "Step 2: GitHub Account Information" -ForegroundColor Cyan
$GitHubUsername = Read-Host "Enter your GitHub username"
$GitHubEmail = Read-Host "Enter your GitHub email"
$RepositoryName = "TruthLensAI"

Write-Host "[OK] Username: $GitHubUsername" -ForegroundColor Green
Write-Host "[OK] Email: $GitHubEmail" -ForegroundColor Green
Write-Host "[OK] Repository: $RepositoryName" -ForegroundColor Green

# Step 3: Verify repository exists on GitHub
Write-Host ""
Write-Host "Step 3: Repository Verification" -ForegroundColor Cyan
$repoExists = Read-Host "Have you created the GitHub repository '$RepositoryName'? (yes/no)"
if ($repoExists -ne "yes") {
    Write-Host "[INFO] Please create the repository at: https://github.com/new" -ForegroundColor Yellow
    Write-Host "[INFO] Name: TruthLensAI, Public, License: MIT" -ForegroundColor Yellow
    $proceed = Read-Host "Have you created it now? (yes/no)"
    if ($proceed -ne "yes") {
        Write-Host "[ABORT] Cannot proceed without repository." -ForegroundColor Red
        exit 1
    }
}

# Step 4: Configure Git
Write-Host ""
Write-Host "Step 4: Configuring Git..." -ForegroundColor Cyan
git config --global user.name $GitHubUsername
git config --global user.email $GitHubEmail
Write-Host "[OK] Git configured" -ForegroundColor Green

# Step 5: Initialize Git repository
Write-Host ""
Write-Host "Step 5: Initializing repository..." -ForegroundColor Cyan
if (-not (Test-Path ".git")) {
    git init
    Write-Host "[OK] Repository initialized" -ForegroundColor Green
} else {
    Write-Host "[OK] Repository already initialized" -ForegroundColor Green
}

# Step 6: Add files
Write-Host ""
Write-Host "Step 6: Staging files..." -ForegroundColor Cyan
git add .
Write-Host "[OK] Files staged" -ForegroundColor Green

# Step 7: Create initial commit
Write-Host ""
Write-Host "Step 7: Creating commit..." -ForegroundColor Cyan
$commitDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Initial commit: TruthLens AI v1.0.0 - Intelligent Misinformation Detection System"
Write-Host "[OK] Commit created" -ForegroundColor Green

# Step 8: Set main branch
Write-Host ""
Write-Host "Step 8: Setting up main branch..." -ForegroundColor Cyan
git branch -M main
Write-Host "[OK] Main branch ready" -ForegroundColor Green

# Step 9: Add remote
Write-Host ""
Write-Host "Step 9: Connecting to GitHub..." -ForegroundColor Cyan
$RemoteUrl = "https://github.com/$GitHubUsername/$RepositoryName.git"
Write-Host "Repository URL: $RemoteUrl" -ForegroundColor White

# Remove existing remote if it exists
git remote remove origin -ErrorAction SilentlyContinue
git remote add origin $RemoteUrl
Write-Host "[OK] Connected to GitHub" -ForegroundColor Green

# Step 10: Push to GitHub
Write-Host ""
Write-Host "Step 10: Pushing to GitHub..." -ForegroundColor Cyan
Write-Host "[INFO] You may be prompted for authentication." -ForegroundColor Cyan
Write-Host "[INFO] Use your Personal Access Token as the password." -ForegroundColor Cyan
Write-Host "[INFO] Generate one at: https://github.com/settings/tokens" -ForegroundColor Cyan
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Push successful!" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Push failed!" -ForegroundColor Red
    Write-Host "[INFO] Make sure your Personal Access Token has 'repo' scope" -ForegroundColor Yellow
    exit 1
}

# Step 11: Verify deployment
Write-Host ""
Write-Host "Step 11: Verifying deployment..." -ForegroundColor Cyan
$remoteBranch = git rev-parse --abbrev-ref HEAD
$commitCount = git rev-list --count HEAD
Write-Host "[OK] Branch: $remoteBranch" -ForegroundColor Green
Write-Host "[OK] Total commits: $commitCount" -ForegroundColor Green

# Final summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your TruthLens AI is now on GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "Repository URL:" -ForegroundColor Cyan
Write-Host "  https://github.com/$GitHubUsername/$RepositoryName" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Visit your repository to verify the code is there" -ForegroundColor White
Write-Host "  2. Share your GitHub link" -ForegroundColor White
Write-Host "  3. (Optional) Deploy to Streamlit Cloud at https://streamlit.io/cloud" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to close"
