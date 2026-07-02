@echo off
REM TruthLens AI - Automated Deployment (Windows Batch Launcher)
REM This script launches the PowerShell deployment script

title TruthLens AI - Automated Deployment
color 0B

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     TruthLens AI - Automated GitHub Deployment         ║
echo ║              Windows Launcher v1.0.0                   ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if PowerShell is available
where powershell >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PowerShell not found. Please ensure PowerShell is installed.
    pause
    exit /b 1
)

echo [INFO] PowerShell found. Launching deployment script...
echo.

REM Get the script directory
set SCRIPT_DIR=%~dp0Deploy-ToGitHub.ps1

REM Check if script exists
if not exist "%SCRIPT_DIR%" (
    echo [ERROR] Deploy-ToGitHub.ps1 not found at %SCRIPT_DIR%
    pause
    exit /b 1
)

REM Run PowerShell script with bypass execution policy
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%"

REM Check if deployment was successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Deployment completed successfully!
) else (
    echo.
    echo [ERROR] Deployment failed with error code %ERRORLEVEL%
)

echo.
pause
