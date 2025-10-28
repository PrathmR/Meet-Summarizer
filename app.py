import streamlit as st
import os
from processing import process_video

st.set_page_config(layout="wide")
st.title("Meeting Video Summarizer 📝")

# Create a temporary directory for uploads if it doesn't exist
if not os.path.exists("temp_uploads"):
    os.makedirs("temp_uploads")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your meeting video file (.mp4, .mov, .mkv)",
    type=["mp4", "mov", "mkv"]
)

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_video_path = os.path.join("temp_uploads", uploaded_file.name)
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Display the video player
    st.video(temp_video_path)

    # Process the video
    with st.spinner("Processing video... This might take a few minutes depending on the length of the video."):
        transcript_text, summary_text = process_video(temp_video_path)

    # Clean up the uploaded video file
    os.remove(temp_video_path)

    if transcript_text and summary_text:
        st.success("Processing Complete!")
        
        col1, col2 = st.columns(2)

        with col1:
            st.header("📋 Summary")
            st.markdown(summary_text)

        with col2:
            st.header("📄 Full Transcript")
            # Use an expander for the long transcript text
            with st.expander("Click to view full transcript"):
                st.text_area(label="", value=transcript_text, height=400)
    else:
        st.error(f"Failed to process the video. Error: {summary_text}")