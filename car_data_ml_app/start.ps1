# Start Python Backend
Write-Host "Starting FastAPI Backend..." -ForegroundColor Green
Start-Process -FilePath ".\backend\venv\Scripts\python.exe" -ArgumentList "-m uvicorn main:app --reload --port 8000" -WorkingDirectory ".\backend"

# Wait a moment
Start-Sleep -Seconds 3

# Start React Frontend
Write-Host "Starting React Frontend..." -ForegroundColor Cyan
Start-Process -FilePath "npm.cmd" -ArgumentList "run dev" -WorkingDirectory ".\frontend"

# Open Browser automatically!
Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"

Write-Host "Both servers started! Browser should automatically open to http://localhost:5173" -ForegroundColor Yellow
