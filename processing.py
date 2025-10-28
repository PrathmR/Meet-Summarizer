import os
from moviepy.editor import VideoFileClip
import assemblyai as aai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def process_video(video_path):
    """
    Extracts audio, transcribes, and summarizes it.
    Returns the transcript and summary.
    """
    try:
        # 1. Extract audio from the video file
        print("Extracting audio...")
        video_clip = VideoFileClip(video_path)
        audio_path = "temp_audio.mp3"
        video_clip.audio.write_audiofile(audio_path)
        video_clip.close()
        
        # 2. Configure AssemblyAI for transcription and summarization
        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(
            summarization=True,
            summary_model=aai.SummarizationModel.informative, # You can choose other models like 'conversational'
            summary_type=aai.SummarizationType.bullets      # Or 'paragraph', 'headline', etc.
        )

        # 3. Transcribe and summarize the audio
        print("Transcribing and summarizing...")
        transcript = transcriber.transcribe(audio_path, config=config)

        # Clean up the temporary audio file
        os.remove(audio_path)

        if transcript.status == aai.TranscriptStatus.error:
            return None, transcript.error
            
        return transcript.text, transcript.summary

    except Exception as e:
        # Clean up audio file in case of an error
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")
        return None, f"An error occurred: {str(e)}"