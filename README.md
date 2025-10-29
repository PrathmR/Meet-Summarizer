# Meet Summarizer

AI-powered meeting transcription and summarization tool using AssemblyAI. Automatically extracts audio from videos, generates full transcripts, and creates bullet-point summaries.

## Features

- 🎬 **Video Support**: Automatically extracts audio from video files (MP4, AVI, MOV)
- 📝 **Full Transcription**: Complete word-by-word transcript saved as `.txt`
- 📄 **Summary PDF**: Bullet-point summaries with highlighted key terms
- 📁 **Organized Output**: Each file gets its own timestamped folder

## Prerequisites

- Python 3.8+
- AssemblyAI API Key ([Get one free](https://www.assemblyai.com/))

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Meet_Summarizer
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
   - Windows:
     ```cmd
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure API Key**

Create a `.env` file in the root directory:
```
ASSEMBLYAI_API_KEY=your_actual_api_key_here
```

## Usage

Run the application:
```bash
python app.py
```

When prompted, enter the path to your audio or video file:
```
📁 Enter audio/video file path: D:\Meet_Summarizer\media\your_file.mp4
```

## Supported File Formats

- **Video**: `.mp4`, `.mov`, `.avi`
- **Audio**: `.mp3`, `.wav`, `.ogg`, `.m4a`

## Output Structure

```
output_summaries/
└── YourFileName_20251029_183835/
    ├── transcript.txt    # Full transcription
    └── summary.pdf       # Bullet-point summary
```

## Project Structure

```
Meet_Summarizer/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .env                   # API key (don't commit!)
├── .gitignore            # Git ignore rules
├── media/                # Input files (optional)
├── uploads/              # Temporary audio files
└── output_summaries/     # Generated transcripts & summaries
```

## Troubleshooting

### Error: "ASSEMBLYAI_API_KEY not found"
- Ensure `.env` file exists in the root directory
- Check that the API key is correctly set

### Error: "File not found"
- Verify the file path is correct
- Paths with spaces can be entered with or without quotes

### Import Errors
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

## License

MIT License
