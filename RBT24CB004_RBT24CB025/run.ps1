Write-Host "Creating Virtual Environment..."
python -m venv venv
.\venv\Scripts\Activate.ps1

Write-Host "Installing Dependencies..."
python -m pip install -r requirements.txt

Write-Host "Starting Backend Server on port 8000..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"

Write-Host "Waiting for backend to start..."
Start-Sleep -Seconds 5

Write-Host "Starting Frontend Server..."
python -m streamlit run frontend/app.py
