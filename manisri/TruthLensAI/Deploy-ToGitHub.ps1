# TruthLens AI - Automated Deployment Script
# This script automates the entire GitHub deployment process
# Run this in PowerShell to deploy your app to GitHub

param(
    [string]$GitHubUsername = "",
    [string]$GitHubEmail = "",
    [string]$RepositoryName = "TruthLensAI"
)

# Color codes for output
$Green = "`e[32m"
$Red = "`e[31m"
$Yellow = "`e[33m"
$Blue = "`e[34m"
$Reset = "`e[0m"

# Script variables
$ProjectPath = "c:\Users\manis\OneDrive\Desktop\manisri\TruthLensAI"
$ScriptVersion = "1.0.0"
$StartTime = Get-Date

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     TruthLens AI - Automated Deployment Script         ║" -ForegroundColor Cyan
Write-Host "║                   Version $ScriptVersion                         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Function to print section header
function Show-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
    Write-Host "  $Title" -ForegroundColor Blue
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
}

# Function to print success message
function Show-Success {
    param([string]$Message)
    Write-Host "  $Green✓$Reset $Message" -ForegroundColor Green
}

# Function to print error message
function Show-Error {
    param([string]$Message)
    Write-Host "  $Red✗$Reset $Message" -ForegroundColor Red
}

# Function to print warning message
function Show-Warning {
    param([string]$Message)
    Write-Host "  $Yellow⚠$Reset $Message" -ForegroundColor Yellow
}

# Function to print info message
function Show-Info {
    param([string]$Message)
    Write-Host "  ℹ $Message" -ForegroundColor Cyan
}

# Function to ask user for input
function Get-UserInput {
    param(
        [string]$Prompt,
        [string]$Default = "",
        [switch]$Secure = $false
    )
    
    if ($Default) {
        $DisplayPrompt = "$Prompt [$Default]: "
    } else {
        $DisplayPrompt = "$Prompt: "
    }
    
    if ($Secure) {
        $Input = Read-Host $DisplayPrompt -AsSecureString
        return $Input
    } else {
        $Input = Read-Host $DisplayPrompt
        if (-not $Input -and $Default) {
            return $Default
        }
        return $Input
    }
}

# Step 1: Check Prerequisites
Show-Header "STEP 1: Checking Prerequisites"

$GitInstalled = $false
try {
    $gitVersion = git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $GitInstalled = $true
        Show-Success "Git is installed: $gitVersion"
    }
} catch {
    $GitInstalled = $false
}

if (-not $GitInstalled) {
    Show-Error "Git is not installed or not in PATH"
    Write-Host ""
    Write-Host "  To install Git:" -ForegroundColor Yellow
    Write-Host "  1. Go to: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "  2. Download and run the installer" -ForegroundColor Yellow
    Write-Host "  3. Keep default settings and complete installation" -ForegroundColor Yellow
    Write-Host "  4. Restart PowerShell" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check project path
if (Test-Path $ProjectPath) {
    Show-Success "Project folder found: $ProjectPath"
} else {
    Show-Error "Project folder not found: $ProjectPath"
    exit 1
}

# Step 2: Get GitHub Information
Show-Header "STEP 2: GitHub Account Information"

Write-Host ""
Write-Host "  📝 Enter your GitHub credentials:" -ForegroundColor Cyan
Write-Host ""

if (-not $GitHubUsername) {
    $GitHubUsername = Get-UserInput "GitHub Username"
}

if (-not $GitHubEmail) {
    $GitHubEmail = Get-UserInput "GitHub Email"
}

Show-Info "GitHub Username: $GitHubUsername"
Show-Info "GitHub Email: $GitHubEmail"

# Verify inputs
if ([string]::IsNullOrWhiteSpace($GitHubUsername) -or [string]::IsNullOrWhiteSpace($GitHubEmail)) {
    Show-Error "GitHub credentials cannot be empty"
    exit 1
}

Show-Success "GitHub information provided"

# Step 3: Check if GitHub repository exists
Show-Header "STEP 3: Checking GitHub Repository"

Write-Host ""
Write-Host "  Check your GitHub account and verify:" -ForegroundColor Yellow
Write-Host "  1. Repository name: $RepositoryName" -ForegroundColor Yellow
Write-Host "  2. Repository visibility: Public" -ForegroundColor Yellow
Write-Host "  3. License: MIT" -ForegroundColor Yellow
Write-Host ""
Write-Host "  If repository doesn't exist, create it at: https://github.com/new" -ForegroundColor Cyan
Write-Host ""

$repoExists = Get-UserInput "Have you created the GitHub repository? (yes/no)" "yes"

if ($repoExists -inotlike "yes*" -and $repoExists -inotlike "y") {
    Show-Error "Please create the repository first and run this script again"
    Write-Host ""
    Write-Host "  Create repository at: https://github.com/new" -ForegroundColor Cyan
    exit 1
}

Show-Success "Repository verified"

# Step 4: Configure Git
Show-Header "STEP 4: Configuring Git"

Write-Host ""
Write-Host "  Configuring Git with your credentials..." -ForegroundColor Cyan

try {
    git config --global user.name $GitHubUsername
    git config --global user.email $GitHubEmail
    Show-Success "Git configured with username: $GitHubUsername"
    Show-Success "Git configured with email: $GitHubEmail"
} catch {
    Show-Error "Failed to configure Git: $_"
    exit 1
}

# Step 5: Navigate to project
Show-Header "STEP 5: Navigating to Project"

try {
    Set-Location $ProjectPath
    Show-Success "Current directory: $(Get-Location)"
} catch {
    Show-Error "Failed to navigate to project: $_"
    exit 1
}

# Step 6: Initialize Git Repository
Show-Header "STEP 6: Initializing Git Repository"

$gitFolder = Join-Path $ProjectPath ".git"

if (Test-Path $gitFolder) {
    Show-Warning "Git repository already initialized"
} else {
    try {
        git init
        Show-Success "Git repository initialized"
    } catch {
        Show-Error "Failed to initialize Git: $_"
        exit 1
    }
}

# Step 7: Add files to staging
Show-Header "STEP 7: Staging Files"

Write-Host ""
Write-Host "  Adding all files to Git staging area..." -ForegroundColor Cyan

try {
    git add .
    $fileCount = (git ls-files).Count
    Show-Success "Added $fileCount files to staging area"
} catch {
    Show-Error "Failed to stage files: $_"
    exit 1
}

# Step 8: Create initial commit
Show-Header "STEP 8: Creating Initial Commit"

Write-Host ""
Write-Host "  Creating initial commit..." -ForegroundColor Cyan

try {
    git commit -m "Initial commit: TruthLens AI v1.0.0 - Intelligent Misinformation Detection System"
    Show-Success "Initial commit created"
} catch {
    Show-Error "Failed to create commit: $_"
    Write-Host ""
    Show-Info "This might mean files are already committed. Continuing..."
}

# Step 9: Rename branch to main
Show-Header "STEP 9: Setting Up Main Branch"

Write-Host ""
Write-Host "  Ensuring main branch is configured..." -ForegroundColor Cyan

try {
    git branch -M main
    Show-Success "Branch set to main"
} catch {
    Show-Error "Failed to set branch: $_"
}

# Step 10: Add remote repository
Show-Header "STEP 10: Connecting to GitHub"

$RemoteUrl = "https://github.com/$GitHubUsername/$RepositoryName.git"

Write-Host ""
Write-Host "  Repository URL: $RemoteUrl" -ForegroundColor Cyan

try {
    # Check if remote already exists
    $remoteExists = git remote get-url origin 2>$null
    
    if ($remoteExists) {
        Show-Warning "Remote already configured: $remoteExists"
        $updateRemote = Get-UserInput "Update remote URL? (yes/no)" "yes"
        
        if ($updateRemote -ilike "yes*" -or $updateRemote -ilike "y") {
            git remote remove origin
            git remote add origin $RemoteUrl
            Show-Success "Remote updated: $RemoteUrl"
        }
    } else {
        git remote add origin $RemoteUrl
        Show-Success "Remote added: $RemoteUrl"
    }
} catch {
    Show-Error "Failed to add remote: $_"
}

# Step 11: Push to GitHub
Show-Header "STEP 11: Pushing to GitHub"

Write-Host ""
Write-Host "  Preparing to push code to GitHub..." -ForegroundColor Cyan
Write-Host ""
Write-Host "  $Yellow⚠  Authentication Required$Reset" -ForegroundColor Yellow
Write-Host ""
Write-Host "  You will be prompted for authentication." -ForegroundColor Cyan
Write-Host "  Use one of these methods:" -ForegroundColor Cyan
Write-Host "    • Personal Access Token (Recommended)" -ForegroundColor Cyan
Write-Host "    • GitHub password" -ForegroundColor Cyan
Write-Host ""
Write-Host "  To generate a token: https://github.com/settings/tokens" -ForegroundColor Cyan
Write-Host ""

$confirmPush = Get-UserInput "Ready to push to GitHub? (yes/no)" "yes"

if ($confirmPush -ilike "yes*" -or $confirmPush -ilike "y") {
    try {
        git push -u origin main
        Show-Success "Code successfully pushed to GitHub!"
    } catch {
        Show-Error "Failed to push to GitHub: $_"
        Write-Host ""
        Write-Host "  Troubleshooting:" -ForegroundColor Yellow
        Write-Host "  1. Verify your Personal Access Token is correct" -ForegroundColor Yellow
        Write-Host "  2. Check that the repository exists at: https://github.com/$GitHubUsername/$RepositoryName" -ForegroundColor Yellow
        Write-Host "  3. Ensure you have push permissions to the repository" -ForegroundColor Yellow
        exit 1
    }
} else {
    Show-Warning "Push cancelled by user"
}

# Step 12: Verify deployment
Show-Header "STEP 12: Verifying Deployment"

Write-Host ""
Write-Host "  Verifying repository status..." -ForegroundColor Cyan

try {
    $remoteUrl = git remote get-url origin
    $currentBranch = git rev-parse --abbrev-ref HEAD
    $commitCount = (git rev-list --count HEAD)
    
    Show-Success "Repository URL: $remoteUrl"
    Show-Success "Current branch: $currentBranch"
    Show-Success "Total commits: $commitCount"
} catch {
    Show-Error "Failed to verify: $_"
}

# Step 13: Optional Streamlit Cloud Deployment
Show-Header "STEP 13: Optional - Deploy to Streamlit Cloud"

Write-Host ""
Write-Host "  Your app can be deployed to Streamlit Cloud for free!" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Steps:" -ForegroundColor Cyan
Write-Host "  1. Go to: https://streamlit.io/cloud" -ForegroundColor Cyan
Write-Host "  2. Click 'New app'" -ForegroundColor Cyan
Write-Host "  3. Connect your GitHub account" -ForegroundColor Cyan
Write-Host "  4. Select: $GitHubUsername / $RepositoryName / demo_app.py" -ForegroundColor Cyan
Write-Host "  5. Click 'Deploy'" -ForegroundColor Cyan
Write-Host ""

$deployStreamlit = Get-UserInput "Open Streamlit Cloud now? (yes/no)" "no"

if ($deployStreamlit -ilike "yes*" -or $deployStreamlit -ilike "y") {
    Start-Process "https://streamlit.io/cloud"
    Show-Success "Opening Streamlit Cloud in browser..."
}

# Final Summary
Show-Header "🎉 DEPLOYMENT COMPLETE! 🎉"

$EndTime = Get-Date
$Duration = $EndTime - $StartTime

Write-Host ""
Write-Host "  ✅ All steps completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "  📊 Summary:" -ForegroundColor Cyan
Write-Host "     • GitHub Username: $GitHubUsername" -ForegroundColor Cyan
Write-Host "     • Repository: $RepositoryName" -ForegroundColor Cyan
Write-Host "     • Repository URL: https://github.com/$GitHubUsername/$RepositoryName" -ForegroundColor Cyan
Write-Host "     • Total Time: $($Duration.TotalSeconds) seconds" -ForegroundColor Cyan
Write-Host ""
Write-Host "  🔗 Next Steps:" -ForegroundColor Yellow
Write-Host "     1. Visit your repository: https://github.com/$GitHubUsername/$RepositoryName" -ForegroundColor Yellow
Write-Host "     2. Share with others or add to portfolio" -ForegroundColor Yellow
Write-Host "     3. Optionally deploy to Streamlit Cloud" -ForegroundColor Yellow
Write-Host "     4. Monitor and maintain the repository" -ForegroundColor Yellow
Write-Host ""
Write-Host "  📚 Documentation:" -ForegroundColor Cyan
Write-Host "     • GitHub Docs: https://docs.github.com" -ForegroundColor Cyan
Write-Host "     • Git Tutorial: https://git-scm.com/docs" -ForegroundColor Cyan
Write-Host "     • Project README: https://github.com/$GitHubUsername/$RepositoryName/blob/main/README.md" -ForegroundColor Cyan
Write-Host ""

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║         🚀 Deployment Successful! 🚀                   ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Optional: Open repository in browser
$openRepo = Get-UserInput "Open repository in browser now? (yes/no)" "yes"

if ($openRepo -ilike "yes*" -or $openRepo -ilike "y") {
    Start-Process "https://github.com/$GitHubUsername/$RepositoryName"
    Show-Success "Opening repository in browser..."
}

Write-Host ""
Write-Host "  Press Enter to exit..." -ForegroundColor Gray
Read-Host
