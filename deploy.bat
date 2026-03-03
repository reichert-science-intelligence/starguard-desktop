@echo off
setlocal
cd /d "%~dp0"
echo.
echo  StarGuard AI Mobile - Deploy / Run
echo  ================================
echo.
echo  1 = Local only       (http://127.0.0.1:8000)
echo  2 = Network (mobile) (http://YOUR-IP:8000 - use on phone)
echo  3 = Port 8502        (http://127.0.0.1:8502)
echo  4 = Show help        (shinyapps.io, firewall)
echo.
set /p choice="Choice (1-4): "
if "%choice%"=="1" goto local
if "%choice%"=="2" goto network
if "%choice%"=="3" goto port
if "%choice%"=="4" goto help
echo Invalid. Using option 1 (local).
goto local

:local
echo.
echo  Starting local only. Open http://127.0.0.1:8000
echo  Ctrl+C to stop.
echo.
shiny run app.py
goto end

:network
echo.
echo  Starting with network access. On your phone (same WiFi) open:
echo  http://YOUR-PC-IP:8000
echo  Find your IP: run 'ipconfig' and look for IPv4.
echo  Ctrl+C to stop.
echo.
shiny run app.py --host 0.0.0.0
goto end

:port
echo.
echo  Starting on port 8502. Open http://127.0.0.1:8502
echo  Ctrl+C to stop.
echo.
shiny run app.py --port 8502
goto end

:help
echo.
echo  shinyapps.io: pip install rsconnect-python
echo  rsconnect add --account YOUR_ACCOUNT --name shinyapps
echo  rsconnect deploy shiny . --name starguard-mobile
echo.
echo  If phone cannot connect: allow Python through Windows Firewall
echo  or allow inbound TCP port 8000.
echo.
pause
goto end

:end
endlocal
