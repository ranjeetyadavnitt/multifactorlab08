@echo off
setlocal enabledelayedexpansion
title SecureShop - GitHub Push Utility
color 0A

echo ================================================================
echo        SECURESHOP - PUSH TO GITHUB REPOSITORY
echo ================================================================
echo.

:: Ensure Git is in PATH
set "GIT_EXE=C:\Users\205124067\AppData\Local\Programs\Git\cmd\git.exe"
where git >nul 2>nul
if %errorlevel% neq 0 (
    if exist "%GIT_EXE%" (
        set "PATH=C:\Users\205124067\AppData\Local\Programs\Git\cmd;%PATH%"
    ) else (
        echo [ERROR] Git is not found in PATH or at default install location.
        echo Please make sure Git is installed.
        echo.
        pause
        exit /b 1
    )
)

:: Navigate to script directory
cd /d "%~dp0"

echo [1/4] Checking repository status...
git status --short
echo.

echo [2/4] Staging and committing any pending changes...
git add -A
git commit -m "Update SecureShop: 2FA MFA login, light theme, realistic hardware assets" >nul 2>nul
if %errorlevel% equ 0 (
    echo       New changes committed.
) else (
    echo       Working directory is clean.
)
echo.

echo [3/4] Verifying remote origin...
git remote -v
git remote set-url origin https://github.com/ranjeetyadavnitt/multifactorlab08.git 2>nul || git remote add origin https://github.com/ranjeetyadavnitt/multifactorlab08.git
echo.

echo [4/4] Pushing to https://github.com/ranjeetyadavnitt/multifactorlab08.git ...
echo.
echo NOTE: If prompted, Git Credential Manager will open a browser window
echo       for you to authenticate with GitHub.
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ================================================================
    echo [SUCCESS] Code successfully pushed to GitHub!
    echo Repository: https://github.com/ranjeetyadavnitt/multifactorlab08
    echo ================================================================
) else (
    echo.
    echo ================================================================
    echo [NOTICE] Push encountered an issue or requires authentication.
    echo.
    echo If you want to push using a Personal Access Token (PAT):
    echo   1. Generate token at https://github.com/settings/tokens (repo scope)
    echo   2. Paste the token below to push immediately:
    echo ================================================================
    echo.
    set /p GITHUB_TOKEN="Enter GitHub Personal Access Token (or press Enter to exit): "
    if defined GITHUB_TOKEN (
        echo Pushing with provided token...
        git push https://!GITHUB_TOKEN!@github.com/ranjeetyadavnitt/multifactorlab08.git main
        if !errorlevel! equ 0 (
            echo.
            echo [SUCCESS] Successfully pushed using Personal Access Token!
        ) else (
            echo.
            echo [ERROR] Failed to push with token. Please verify token permissions.
        )
    )
)

echo.
pause
