import os
import sys
import argparse  # Added for command-line arguments
from dotenv import load_dotenv  # Added for .env support
import assemblyai as aai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
import re

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
try:
    api_key = os.getenv('ASSEMBLYAI_API_KEY')
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY not found in .env file.")
    aai.settings.api_key = api_key
except Exception as e:
    print(f"Error: {e}")
    print("Please create a .env file in the same directory and add the line:")
    print("ASSEMBLYAI_API_KEY='your_key_here'")
    sys.exit(1) # Stop execution if the key is missing

print("✅ AssemblyAI API Key loaded.")

# Define the PDF generation function (No changes needed)
def generate_summary_pdf(summary_text, filename="meeting_summary.pdf"):
    """Generates a PDF document containing the meeting summary."""
    doc = SimpleDocTemplate(filename,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    story = []
    styles = getSampleStyleSheet()

    # Add heading
    heading_style = styles['h1']
    story.append(Paragraph("Meeting Summary", heading_style))
    story.append(Spacer(1, 0.2 * inch))

    # Process and add summary text with bolding
    normal_style = styles['Normal']
    normal_style.alignment = TA_JUSTIFY

    important_terms = ["AI agents", "legal teams", "trustworthy", "hybrid RAG", "ediscovery", "semantic search", "structured search", "precision", "traceable output", "LLM", "law", "medicine"]
    
    paragraphs = summary_text.split('\n')

    for para in paragraphs:
        if para.strip(): # Avoid adding empty paragraphs
            styled_text = para
            for term in important_terms:
                styled_text = re.sub(r'\b(' + re.escape(term) + r')\b', r'<b>\1</b>', styled_text, flags=re.IGNORECASE)

            story.append(Paragraph(styled_text, normal_style))
            story.append(Spacer(1, 0.1 * inch)) # Add space between paragraphs

    # Build the PDF
    doc.build(story)
    print(f"\nPDF summary generated: {filename}")


# ==============================================================================
# 3. GET FILE PATH FROM ARGUMENTS
# ==============================================================================
# Replaced Colab's files.upload() with argparse
parser = argparse.ArgumentParser(description="Transcribe and summarize a meeting file.")
parser.add_argument("file_path", help="Path to the audio or video file to process.")
args = parser.parse_args()

file_path = args.file_path

if not os.path.exists(file_path):
    print(f"Error: File not found at '{file_path}'")
    sys.exit(1)

print(f"Processing file: '{file_path}'")

# ==============================================================================
# 4. PROCESSING LOGIC
# ==============================================================================
audio_path = None
pdf_filename = "meeting_summary.pdf" # Define here for the finally block

try:
    # --- Determine file to process ---
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension in ['.mp4', '.avi', '.mov']:
        print("\nStep 1/3: Extracting audio from video...")
        video_clip = VideoFileClip(file_path)
        audio_path = "temp_audio.mp3"
        video_clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
        video_clip.close()
        print("✅ Audio extracted.")
        file_to_process = audio_path
    elif file_extension in ['.mp3', '.wav', '.ogg', '.m4a']:
        print("\nStep 1/3: Using provided audio file...")
        file_to_process = file_path
        print("✅ Audio file ready.")
    else:
        raise ValueError("Unsupported file type provided.")


    # --- Transcribe and Summarize ---
    print("\nStep 2/3: Transcribing and summarizing... (This may take a few minutes)")
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(
        summarization=True,
        summary_model=aai.SummarizationModel.informative,
        summary_type=aai.SummarizationType.bullets
    )
    transcript = transcriber.transcribe(file_to_process, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")

    print("✅ Transcription and summarization complete.")

    # --- Display Results ---
    # Replaced display(Markdown(...)) with standard print()
    print("\nStep 3/3: Displaying results...")
    
    print("\n" + "="*30)
    print(" 📋 Summary of the Meeting")
    print("="*30)
    print(transcript.summary)

    print("\n" + "="*30)
    print(" 📄 Full Transcript")
    print("="*30)
    # Just print the text. The HTML scroll box is for notebooks.
    print(transcript.text)
    print("-" * 30)

    # --- Generate PDF Summary ---
    generate_summary_pdf(transcript.summary, pdf_filename)

    # --- Provide Download Link ---
    # Replaced FileLink() with a simple print statement
    print(f"\n✅ Successfully created PDF: {os.path.abspath(pdf_filename)}")


except Exception as e:
    print(f"\nAn error occurred: {e}")

finally:
    # --- Cleanup ---
    print("\nCleaning up temporary files...")
    
    # IMPORTANT: We no longer delete the original file_path
    # as it's the user's source file, not an upload.
    
    if audio_path and os.path.exists(audio_path):
        os.remove(audio_path)
        print(f"Removed temporary file: {audio_path}")
    
    # Keep the generated PDF
    print("Done.")