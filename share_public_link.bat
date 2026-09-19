@echo off
title Share Mattress AI Dashboard Publicly
echo ======================================================================
echo    Instant Public Share Link Generator (Zero Signup / Free)
echo ======================================================================
echo.
echo [1/2] Making sure your local dashboard is active on port 8000...
echo.

echo [2/2] Generating instant secure HTTPS public link...
echo Anyone in the world on mobile or PC can open the link below!
echo.
echo Press Ctrl+C anytime to close the public link.
echo ======================================================================
echo.

ssh -o StrictHostKeyChecking=no -R 80:localhost:8000 nokey@localhost.run

pause
