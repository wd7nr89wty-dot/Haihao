@echo off
setlocal
cd /d %~dp0

if not exist worker.json (
  echo Missing worker.json
  echo Copy worker.example.json to worker.json and set the local GAEA executable path.
  exit /b 1
)

if "%HAIHAO_GAEA_COMMAND%"=="" (
  echo HAIHAO_GAEA_COMMAND is not configured.
  echo Verify the command line syntax supported by your installed GAEA version first.
  exit /b 1
)

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 worker.py
) else (
  python worker.py
)
