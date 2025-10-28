# PowerShell script to run new.py

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Meeting Transcriber & Summarizer" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-Not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Please create a .env file with your AssemblyAI API key:" -ForegroundColor Yellow
    Write-Host "  ASSEMBLYAI_API_KEY=your_key_here" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Check if venv exists
if (-Not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create a virtual environment first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host "Checking dependencies..." -ForegroundColor Yellow
& venv\Scripts\python.exe check_setup.py

Write-Host ""
Write-Host "To run the script, use:" -ForegroundColor Green
Write-Host '  .\venv\Scripts\python.exe new.py "path\to\your\file.mp3"' -ForegroundColor White
Write-Host ""
Write-Host "Example:" -ForegroundColor Green
Write-Host '  .\venv\Scripts\python.exe new.py "sample_audio.mp3"' -ForegroundColor White
Write-Host ""
Write-Host "For help:" -ForegroundColor Green
Write-Host "  .\venv\Scripts\python.exe new.py --help" -ForegroundColor White
Write-Host ""

# If arguments provided, run the script
if ($args.Count -gt 0) {
    Write-Host "Running new.py with file: $($args[0])" -ForegroundColor Cyan
    & venv\Scripts\python.exe new.py $args[0]
} else {
    Write-Host "No file specified. Please provide an audio/video file path." -ForegroundColor Yellow
}

Write-Host ""
pause
