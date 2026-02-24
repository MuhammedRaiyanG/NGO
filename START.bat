@echo off
title Hope Foundation - NGO Website
echo.
echo ========================================
echo   HOPE FOUNDATION - Auto Start
echo ========================================
echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d d:\NGO\backend && C:\Users\ELCOT\AppData\Local\Programs\Python\Python311\python.exe app.py"

echo Waiting for backend to start...
timeout /t 4 /nobreak

echo.
echo Opening Website in Browser...
start http://localhost:5000/

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo   Backend running on port 5000
echo   Website opening in browser
echo.
echo   ADMIN LOGIN CREDENTIALS:
echo   Username: admin
echo   Password: admin123
echo.
echo   Close this window when done
echo ========================================
echo.
pause
