import os
import sys
from dotenv import load_dotenv
import assemblyai as aai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
import re
from moviepy import VideoFileClip
from datetime import datetime

# ✅ Create necessary directories
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output_summaries"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ✅ Load API Key from .env
load_dotenv()
api_key = os.getenv("ASSEMBLYAI_API_KEY")

if not api_key:
    print("❌ Missing AssemblyAI API Key in .env file.")
    sys.exit(1)

aai.settings.api_key = api_key
print("✅ AssemblyAI API Key loaded.")


# ✅ Save Transcript and Summary
def save_transcript_and_summary(transcript_obj, original_filename):
    # Generate unique folder name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(original_filename))[0]
    folder_name = f"{base_name}_{timestamp}"
    output_folder = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(output_folder, exist_ok=True)
    
    # Save transcript as TXT
    transcript_path = os.path.join(output_folder, "transcript.txt")
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript_obj.text)
    print(f"📝 Transcript saved: {transcript_path}")
    
    # Save summary as PDF
    pdf_path = os.path.join(output_folder, "summary.pdf")
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Meeting Summary", styles['Title']),
        Spacer(1, 0.2 * inch)
    ]

    normal_style = styles['BodyText']
    normal_style.alignment = TA_JUSTIFY

    important_terms = [
        "AI agents", "trustworthy", "semantic search", "LLM"
    ]

    summary_text = transcript_obj.summary if transcript_obj.summary else "No summary available."
    for para in summary_text.split('\n'):
        styled_text = para
        for term in important_terms:
            styled_text = re.sub(
                rf"\b({re.escape(term)})\b",
                r"<b>\1</b>",
                styled_text,
                flags=re.IGNORECASE,
            )
        story.append(Paragraph(styled_text, normal_style))
        story.append(Spacer(1, 0.1 * inch))

    doc.build(story)
    print(f"📄 Summary PDF created: {pdf_path}")
    print(f"📁 All files saved in: {output_folder}")


# ✅ Ask user for file path (no CLI args)
file_path = input("📁 Enter audio/video file path: ").strip().strip('"\'')

if not os.path.exists(file_path):
    print("❌ File not found!")
    sys.exit(1)

extension = os.path.splitext(file_path)[1].lower()
audio_path = None

try:
    if extension in [".mp4", ".mov", ".avi"]:
        print("🎬 Extracting audio...")
        audio_path = os.path.join(UPLOAD_DIR, "temp_audio.mp3")
        video = VideoFileClip(file_path)
        video.audio.write_audiofile(audio_path, logger=None)
        video.close()
        file_to_process = audio_path
    else:
        file_to_process = file_path

    print("⏳ Transcribing and summarizing...")
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(
        summarization=True,
        summary_model=aai.SummarizationModel.informative,
        summary_type=aai.SummarizationType.bullets
    )

    transcript = transcriber.transcribe(file_to_process, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(transcript.error)

    print("\n✅ Transcription Complete!")
    print(f"\n📝 Transcript Preview (first 500 chars):\n{transcript.text[:500]}...\n")
    print("\n✅ Summary Ready:")
    print(transcript.summary)

    save_transcript_and_summary(transcript, file_path)

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if audio_path and os.path.exists(audio_path):
        os.remove(audio_path)
        print("🧹 Temp audio removed.")

    print("✅ Process Completed.")
