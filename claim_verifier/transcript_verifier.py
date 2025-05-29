import whisper
import os
import certifi

# Setting SSl certificates in order to load model
os.environ["SSL_CERT_FILE"] = certifi.where()
model = whisper.load_model("base")

def speech_to_text(video_path):
    """
    Transcribe speech from a video file using Whisper.

    Args:
        video_path (str): Path to the video file (e.g. MP4)

    Returns:
        dict: {
            "text": str,         # Transcribed speech
            "language": str      # Detected language (e.g. 'en')
        }
    """

    result = model.transcribe(video_path)
    return {
        "text": result["text"],
        "language": result["language"]
    }