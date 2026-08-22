@echo off
echo =========================================================
echo   Starting Application Readiness Agent (MVP)
echo =========================================================
echo.
echo Starting Backend (FastAPI + Webcmd 0.7.4) on http://localhost:8000 ...
start "ARA Backend" cmd /k "cd /d %~dp0 && python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 2 /nobreak >nul

echo Starting Frontend (React + Vite) on http://localhost:5173 ...
start "ARA Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers started!
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000/docs
echo Built-in Demo Portal: http://localhost:8000/demo-portal
echo =========================================================