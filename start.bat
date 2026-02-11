@echo off
echo Starting Re:Boot Services...

:: 1. Backend Server
start "Re:Boot Backend (Django)" cmd /k "cd backend && ..\venv\Scripts\activate && python manage.py runserver"

:: 2. Frontend Server
start "Re:Boot Frontend (Vite)" cmd /k "cd frontend && npm run dev"

echo All servers are starting. Please check the individual terminal windows.
pause
