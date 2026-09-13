@echo off
setlocal EnableExtensions
title WoW Arena Strategist
cd /d "%~dp0"

if /I "%~1"=="--open" goto wait_and_open

set "APP_URL=http://127.0.0.1:5173/"
set "APP_PORT=5173"

echo.
echo  WoW Arena Strategist
echo  Booting local resources, then the app.
echo.

echo [1/4] Node.js
call :find_node
if errorlevel 1 (
  echo        Not found. Trying winget install of Node.js LTS...
  call :install_node
  call :find_node
)
if errorlevel 1 (
  echo ERROR: Node.js is required.
  echo Install it from https://nodejs.org then double-click start.bat again.
  pause
  exit /b 1
)
for /f "delims=" %%v in ('node -v') do echo        %%v

echo [2/4] npm packages
if not exist "node_modules\.bin\vite.cmd" (
  if exist "package-lock.json" (
    call npm.cmd ci
  ) else (
    call npm.cmd install
  )
  if errorlevel 1 (
    echo ERROR: npm install failed.
    pause
    exit /b 1
  )
) else (
  echo        already installed
)

echo [3/4] Corpus data
if not exist "public\data\canonical-package.json" (
  echo ERROR: missing public\data\canonical-package.json
  echo Run: npm run export-data
  pause
  exit /b 1
)
if not exist "public\data\matches-slim.json" (
  echo ERROR: missing public\data\matches-slim.json
  pause
  exit /b 1
)
if not exist "public\data\corpus-health.json" (
  echo ERROR: missing public\data\corpus-health.json
  pause
  exit /b 1
)
echo        canonical-package.json, matches-slim.json, corpus-health.json

echo [4/4] App server
call :port_up
if not errorlevel 1 (
  echo        already running at %APP_URL%
  start "" "%APP_URL%"
  echo.
  echo Browser opened. This window can be closed if the server is in another window.
  pause
  exit /b 0
)

echo        starting Vite at %APP_URL%
echo        Close this window or press Ctrl+C to stop the app.
echo.
start "wow-strategist-open" /min "%~f0" --open
call npm.cmd start
echo.
echo Server stopped.
pause
exit /b 0

:wait_and_open
set "APP_URL=http://127.0.0.1:5173/"
for /L %%i in (1,1,60) do (
  call :port_up
  if not errorlevel 1 (
    start "" "%APP_URL%"
    exit /b 0
  )
  timeout /t 1 /nobreak >nul
)
exit /b 1

:port_up
curl.exe -fsS -o NUL --max-time 2 "http://127.0.0.1:5173/" >nul 2>&1
if not errorlevel 1 exit /b 0
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 http://127.0.0.1:5173/; if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 500) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
exit /b %ERRORLEVEL%

:find_node
where node >nul 2>&1
if not errorlevel 1 exit /b 0
if exist "%ProgramFiles%\nodejs\node.exe" (
  set "PATH=%ProgramFiles%\nodejs;%PATH%"
  where node >nul 2>&1
  if not errorlevel 1 exit /b 0
)
if exist "%LOCALAPPDATA%\Programs\node\node.exe" (
  set "PATH=%LOCALAPPDATA%\Programs\node;%PATH%"
  where node >nul 2>&1
  if not errorlevel 1 exit /b 0
)
exit /b 1

:install_node
where winget >nul 2>&1
if errorlevel 1 exit /b 1
winget install -e --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
if errorlevel 1 exit /b 1
if exist "%ProgramFiles%\nodejs\node.exe" set "PATH=%ProgramFiles%\nodejs;%PATH%"
exit /b 0
