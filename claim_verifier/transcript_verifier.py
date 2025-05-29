import whisper
import os
import certifi
import requests
from nltk.tokenize import sent_tokenize

# Setting SSl certificates in order to load model
os.environ["SSL_CERT_FILE"] = certifi.where()
model = whisper.load_model("base")


def split_text_into_sentences(text):
    return sent_tokenize(text)


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


def claim_should_be_fact_checked(claim):

    api_key = "a9e84fbf35644881b3e378a1af81b21c"

    # Define the endpoint (url) with the claim formatted as part of it, api-key (api-key is sent as an extra header)
    api_endpoint = f"https://idir.uta.edu/claimbuster/api/v2/score/text/{claim}"
    request_headers = {"x-api-key": api_key}

    # Sending the GET request to the API and storing the api response
    api_response = requests.get(url=api_endpoint, headers=request_headers)

    response_json = api_response.json()
    results = response_json['results']
    score = results[0]['score']
    if score > 0.5:
        return True

    # Returns the JSON payload the API sent back
    return False
