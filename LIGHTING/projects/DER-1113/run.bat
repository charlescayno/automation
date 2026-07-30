@echo off
TITLE DER-1113 Master CLI Test Runner
echo Launching DER-1113 Master CLI...

cd /d "%~dp0"
set ROOT_DIR=%~dp0..\..

if exist "%ROOT_DIR%\Scripts\activate.bat" (
    call "%ROOT_DIR%\Scripts\activate.bat"
) else if exist "%ROOT_DIR%\.venv\Scripts\activate.bat" (
    call "%ROOT_DIR%\.venv\Scripts\activate.bat"
)

if exist "%ROOT_DIR%\Scripts\python.exe" (
    "%ROOT_DIR%\Scripts\python.exe" cli.py %*
) else (
    python cli.py %*
)

if "%~1"=="" pause
