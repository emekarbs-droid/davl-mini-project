@echo off
echo ============================================================
echo  DAVL - Data Analysis ^& Visualization Lab
echo  Setup Script
echo ============================================================
echo.

:: Check if python is available via winget or direct path
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found in PATH.
    echo.
    echo Please install Python 3.11 from:
    echo   https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check:
    echo   [x] Add Python to PATH
    echo.
    echo After installing Python, re-run this script.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

echo [1/3] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo [3/3] Verifying Streamlit installation...
python -m streamlit --version

echo.
echo ============================================================
echo  Setup complete! Run the app with:
echo     run_app.bat
echo  OR:
echo     python -m streamlit run app.py
echo ============================================================
pause
