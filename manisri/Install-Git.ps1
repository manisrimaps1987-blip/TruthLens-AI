# TruthLens AI - Automated Git Installation Script
# This script downloads and installs Git for Windows automatically

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     TruthLens AI - Automated Git Installation          ║" -ForegroundColor Cyan
Write-Host "║                    Version 1.0.0                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  This script requires Administrator privileges." -ForegroundColor Yellow
    Write-Host "Attempting to elevate..." -ForegroundColor Yellow
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Function to display progress
function Show-Progress {
    param([string]$Message)
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "  📦 $Message" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
}

function Show-Success {
    param([string]$Message)
    Write-Host "  ✓ $Message" -ForegroundColor Green
}

function Show-Error {
    param([string]$Message)
    Write-Host "  ✗ $Message" -ForegroundColor Red
}

function Show-Info {
    param([string]$Message)
    Write-Host "  ℹ $Message" -ForegroundColor Cyan
}

# Step 1: Check if Git is already installed
Show-Progress "Checking if Git is already installed"
try {
    $gitVersion = & git --version 2>&1
    Show-Success "Git is already installed: $gitVersion"
    Write-Host ""
    Write-Host "✅ Git installation verified!" -ForegroundColor Green
    Write-Host "You can now proceed with the deployment script." -ForegroundColor Green
    Write-Host ""
    Pause
    exit 0
} catch {
    Show-Info "Git not found. Proceeding with installation..."
}

# Step 2: Determine Git download URL
Show-Progress "Preparing Git download"
Show-Info "Detecting system architecture..."

$is64Bit = [Environment]::Is64BitOperatingSystem
$arch = if ($is64Bit) { "64-bit" } else { "32-bit" }
$bitString = if ($is64Bit) { "64" } else { "32" }
Show-Success "System architecture: $arch"

# Git download URL for latest version
$gitDownloadUrl = "https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/Git-2.45.0-$bitString-bit.exe"

# Step 3: Create temporary directory for download
$tempDir = [System.IO.Path]::GetTempPath()
$installerPath = Join-Path $tempDir "Git-Installer.exe"

Show-Progress "Downloading Git for Windows"
Show-Info "Download URL: $gitDownloadUrl"
Show-Info "Saving to: $installerPath"

try {
    # Download Git installer
    $ProgressPreference = 'SilentlyContinue'  # Suppress progress bar for cleaner output
    Invoke-WebRequest -Uri $gitDownloadUrl -OutFile $installerPath -ErrorAction Stop
    
    if (Test-Path $installerPath) {
        Show-Success "Git installer downloaded successfully"
        $fileSize = (Get-Item $installerPath).Length / 1MB
        Show-Info "File size: $([math]::Round($fileSize, 2)) MB"
    } else {
        Show-Error "Failed to download Git installer"
        Write-Host ""
        Pause
        exit 1
    }
} catch {
    Show-Error "Download failed: $_"
    Show-Info "Please download Git manually from: https://git-scm.com/download/win"
    Write-Host ""
    Pause
    exit 1
}

# Step 4: Run Git installer silently
Show-Progress "Installing Git for Windows"
Show-Info "Starting silent installation..."
Show-Info "This may take a few minutes..."

try {
    # Run installer with silent flags
    $installArgs = @(
        '/SILENT',
        '/NORESTART',
        '/NOCANCEL',
        '/SP-',
        '/CLOSEAPPLICATIONS',
        '/RESTARTAPPLICATIONS',
        '/COMPONENTS=icons,ext\reg\shellhere,ext\reg\guihere,assoc,assoc_sh'
    )
    
    $process = Start-Process -FilePath $installerPath -ArgumentList $installArgs -PassThru -Wait
    
    if ($process.ExitCode -eq 0) {
        Show-Success "Git installation completed successfully"
    } else {
        Show-Error "Git installation exited with code: $($process.ExitCode)"
    }
} catch {
    Show-Error "Installation failed: $_"
    Write-Host ""
    Pause
    exit 1
}

# Step 5: Clean up installer
Show-Progress "Cleaning up"
try {
    Remove-Item -Path $installerPath -Force -ErrorAction SilentlyContinue
    Show-Success "Temporary files cleaned up"
} catch {
    Show-Info "Could not remove temporary installer (not critical)"
}

# Step 6: Refresh environment variables
Show-Progress "Refreshing environment variables"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
Show-Success "Environment variables refreshed"

# Step 7: Verify installation
Show-Progress "Verifying Git installation"
Start-Sleep -Seconds 2

try {
    $gitVersion = & git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Show-Success "Git verification successful!"
        Show-Info "Version: $gitVersion"
    } else {
        Show-Error "Git command returned error code: $LASTEXITCODE"
        Show-Info "You may need to restart PowerShell or your computer"
    }
} catch {
    Show-Error "Could not verify Git installation: $_"
    Show-Info "You may need to restart PowerShell or your computer"
}

# Step 8: Summary
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║         ✅ GIT INSTALLATION COMPLETE ✅                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "✓ Git has been successfully installed!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Close this window (press any key)" -ForegroundColor White
Write-Host "  2. Run: Deploy.bat" -ForegroundColor Yellow
Write-Host "  3. Follow the prompts to deploy to GitHub" -ForegroundColor White
Write-Host ""

Pause
