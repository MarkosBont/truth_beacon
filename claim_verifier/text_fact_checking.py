from os import truncate

import whisper
import os
import certifi
import requests
from nltk.tokenize import sent_tokenize
from serpapi import GoogleSearch
from transformers import pipeline

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


def get_similar_from_web_search(claim, num_results=5):
    params = {
        "q": claim,
        "api_key": "d6ce7e36a6da680ab314e44aeb0b4a9c691fba1dfc2c0150f409589b63ca7c4d",
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    data = []
    for res in results.get("organic_results", []):
        snippet = res.get("snippet")
        link = res.get("link")
        if snippet and link:
            data.append((snippet, link))

    return data


def compare_claim_to_web_search(claim, data):
    nli = pipeline("text-classification", model="facebook/bart-large-mnli")

    entailment_scores = []
    contradiction_scores = []
    neutral_scores = []

    entailment_links = []
    contradiction_links = []

    snippets = []
    for tup in data:
        snippets.append(tup[0])

    for snippet, url in data:
        result = nli(f"{claim} </s>{snippet}")
        label = result[0]['label'].lower()
        score = result[0]['score']

        if label == "entailment":
            entailment_scores.append(score)
            entailment_links.append(url)
        elif label == "contradiction":
            contradiction_scores.append(score)
            contradiction_links.append(url)
        elif label == "neutral":
            neutral_scores.append(score)


    count_entailment = len(entailment_scores)
    average_entailment = sum(entailment_scores) / count_entailment if count_entailment > 0 else 0

    count_contradiction = len(contradiction_scores)
    average_contradiction = sum(contradiction_scores) / count_contradiction if count_contradiction > 0 else 0

    count_neutral = len(neutral_scores)

    if count_entailment > count_contradiction and count_entailment > count_neutral and average_entailment > 0.5:
        return f"Claim Supported: {claim}, Confidence Score: {average_entailment}\nSupporting links:\n" + "\n".join(entailment_links)
    elif count_contradiction > count_entailment and count_contradiction > count_neutral and average_contradiction > 0.5:
        return f"Claim Refuted: {claim}, Confidence Score: {average_contradiction}\nContradicting links:\n" + "\n".join(contradiction_links)
    else:
        return f"Claim Unclear: {claim} - Insufficient or Conflicting Evidence"

"""
    return {
        "entailment_scores": entailment_scores,
        "entailment_links": entailment_links,
        "contradiction_scores": contradiction_scores,
        "contradiction_links": contradiction_links,
        "neutral_scores": neutral_scores,
        "average_entailment": average_entailment,
        "average_contradiction": average_contradiction,
        "counts": {
            "entailment": count_entailment,
            "contradiction": count_contradiction,
            "neutral": count_neutral
        }
    }
"""



