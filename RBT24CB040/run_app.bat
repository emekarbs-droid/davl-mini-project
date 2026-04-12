@echo off
echo ============================================================
echo  DAVL - Data Analysis ^& Visualization Lab
echo  Starting Application...
echo ============================================================
echo.

where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo Opening browser at http://localhost:8501
echo Press Ctrl+C to stop the server.
echo.

python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

pause
