@echo off
echo ============================================
echo   Meeting Transcriber ^& Summarizer
echo ============================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please create a .env file with your AssemblyAI API key:
    echo   ASSEMBLYAI_API_KEY=your_key_here
    echo.
    pause
    exit /b 1
)

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please create a virtual environment first:
    echo   python -m venv venv
    echo.
    pause
    exit /b 1
)

echo Checking dependencies...
venv\Scripts\python.exe check_setup.py

echo.
echo ===========================
echo HOW TO RUN:
echo ===========================
echo.
echo   venv\Scripts\python.exe new.py "path\to\your\file.mp3"
echo.
echo Example:
echo   venv\Scripts\python.exe new.py "sample_audio.mp3"
echo.
echo For help:
echo   venv\Scripts\python.exe new.py --help
echo.
echo Supported formats: .mp3, .wav, .mp4, .avi, .mov, .ogg, .m4a
echo.
pause
