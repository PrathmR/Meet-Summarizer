# How to Run new.py

## Prerequisites

1. **Python Virtual Environment**: Already set up in `venv/` directory
2. **Dependencies**: Install required packages
3. **API Key**: Configure AssemblyAI API key in `.env` file

## Step 1: Install Dependencies

Open Command Prompt in this directory and run:

```cmd
venv\Scripts\pip.exe install -r requirements.txt
```

## Step 2: Configure API Key

Make sure your `.env` file contains your AssemblyAI API key:

```
ASSEMBLYAI_API_KEY=your_actual_api_key_here
```

## Step 3: Run the Script

### Basic Usage

```cmd
venv\Scripts\python.exe new.py "path\to\your\audio_or_video_file.mp3"
```

### Example with a test file

```cmd
venv\Scripts\python.exe new.py "venv\Lib\site-packages\pyannote\audio\sample\sample.wav"
```

### Get Help

```cmd
venv\Scripts\python.exe new.py --help
```

## Supported File Formats

- **Video**: `.mp4`, `.avi`, `.mov`
- **Audio**: `.mp3`, `.wav`, `.ogg`, `.m4a`

## Output

The script will:
1. Extract audio from video files (if needed)
2. Transcribe the audio using AssemblyAI
3. Generate a summary in bullet points
4. Create a PDF file: `meeting_summary.pdf`
5. Display the results in the console

## Troubleshooting

### Error: "ASSEMBLYAI_API_KEY not found"
- Check your `.env` file exists and contains the correct API key

### Error: "File not found"
- Verify the file path is correct
- Use quotes around paths with spaces

### Import Errors
- Run: `venv\Scripts\pip.exe install -r requirements.txt`
