# TruthLens AI - Automated Git Installation
# Simple version without special characters

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Git Installation Script" -ForegroundColor Cyan  
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed
Write-Host "Checking if Git is installed..." -ForegroundColor Cyan
try {
    $gitVersion = & git --version 2>&1
    Write-Host "[OK] Git is already installed: $gitVersion" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now proceed with the deployment!" -ForegroundColor Green
    Read-Host "Press Enter to continue"
    exit 0
} catch {
    Write-Host "[INFO] Git not found, proceeding with installation..." -ForegroundColor Yellow
}

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[WARNING] This script needs to run as Administrator." -ForegroundColor Yellow
    Write-Host "Attempting to run with elevated privileges..." -ForegroundColor Yellow
    $scriptPath = $MyInvocation.MyCommand.Path
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" -Verb RunAs
    exit
}

# Create temp directory
$tempDir = [System.IO.Path]::GetTempPath()
$installerPath = Join-Path $tempDir "Git-Installer.exe"

# Determine architecture
$is64Bit = [Environment]::Is64BitOperatingSystem
$bitString = if ($is64Bit) { "64" } else { "32" }

Write-Host ""
Write-Host "Downloading Git for Windows..." -ForegroundColor Cyan
Write-Host "Architecture: $(if ($is64Bit) { '64-bit' } else { '32-bit' })" -ForegroundColor White

# Download URL
$gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/Git-2.45.0-$bitString-bit.exe"

Write-Host "Download URL: $gitUrl" -ForegroundColor White
Write-Host "Saving to: $installerPath" -ForegroundColor White
Write-Host ""

try {
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $gitUrl -OutFile $installerPath -ErrorAction Stop
    
    if (Test-Path $installerPath) {
        $fileSize = (Get-Item $installerPath).Length / 1MB
        Write-Host "[OK] Downloaded successfully ($('{0:N2}' -f $fileSize) MB)" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Download failed" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "[ERROR] Download failed: $_" -ForegroundColor Red
    Write-Host "Please download Git manually from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Install Git
Write-Host ""
Write-Host "Installing Git..." -ForegroundColor Cyan
Write-Host "This may take a few moments..." -ForegroundColor White
Write-Host ""

try {
    $installArgs = @(
        '/SILENT',
        '/NORESTART'
    )
    
    $process = Start-Process -FilePath $installerPath -ArgumentList $installArgs -PassThru -Wait
    
    if ($process.ExitCode -eq 0) {
        Write-Host "[OK] Git installation completed" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Installation exited with code: $($process.ExitCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] Installation failed: $_" -ForegroundColor Red
    exit 1
}

# Clean up
Write-Host ""
Write-Host "Cleaning up..." -ForegroundColor Cyan
try {
    Remove-Item -Path $installerPath -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Cleanup completed" -ForegroundColor Green
} catch {
    Write-Host "[INFO] Could not remove temporary files (not critical)" -ForegroundColor Yellow
}

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Cyan

Start-Sleep -Seconds 2

try {
    $gitVersion = & git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Git is ready: $gitVersion" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Git command returned error code: $LASTEXITCODE" -ForegroundColor Yellow
        Write-Host "You may need to restart PowerShell or your computer" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[WARNING] Could not verify Git: $_" -ForegroundColor Yellow
    Write-Host "You may need to restart PowerShell or your computer" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Close this window" -ForegroundColor White
Write-Host "2. Run: Deploy.bat" -ForegroundColor Yellow
Write-Host "3. Follow the prompts to deploy to GitHub" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to close"
