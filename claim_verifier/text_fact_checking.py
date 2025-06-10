import whisper
import os
import certifi
from nltk.tokenize import sent_tokenize
from serpapi import GoogleSearch
from transformers import pipeline
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from newspaper import Article

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


def chunk_article(article_text, chunk_size=3):
    sentences = sent_tokenize(article_text)
    chunks = []

    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def extract_full_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Failed to extract {url}: {e}")
        return ""


def bing_search(claim, num_results=3):
    options = Options()
    options.add_argument("--lang=en-US")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)
    driver.get(f"https://www.bing.com/search?q={claim}&setlang=en")
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    results = []
    count = 0
    for item in soup.find_all("li", class_="b_algo"):
        title_tag = item.find("h2")
        link_tag = item.find("a")
        snippet_tag = item.find("p")

        if title_tag and link_tag and snippet_tag:
            url = link_tag["href"]
            article_text = extract_full_text(url)
            if article_text:
                results.append({
                    "title": title_tag.get_text(),
                    "snippet": snippet_tag.get_text(),
                    "url": url,
                    "article": article_text
                })
                count += 1

        else:
            print(f"Failed to extract {title_tag}, {link_tag}, {snippet_tag}, {article_text}")
            return []

        if count >= num_results:
            break

    return results

def get_similar_from_web_search(claim, num_results=3):
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


def compare_claim_to_web_search(claim, data, model_name = "Dzeniks/roberta-fact-check"):

    if model_name == "facebook/bart-large-mnli":
        nli = pipeline("text-classification", model=model_name)

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

    elif model_name == "Dzeniks/roberta-fact-check":
        nli = pipeline("text-classification", model=model_name)
        support_scores = []
        refute_scores = []

        support_links = []
        refute_links = []

        snippets = []
        for tup in data:
            snippets.append(tup[0])

        for snippet, url in data:
            result = nli(f"{claim} </s>{snippet}")
            result_label = result[0]['label'].upper()
            result_score = result[0]['score']
            if result_label == "LABEL_0":
                support_scores.append(result_score)
                support_links.append(url)
            elif result_label == "LABEL_1":
                refute_scores.append(result_score)
                refute_links.append(url)

        support_count = len(support_scores)
        refute_count = len(refute_scores)

        support_average = sum(support_scores) / support_count if support_count > 0 else 0
        refute_average = sum(refute_scores) / refute_count if refute_count > 0 else 0


        if support_count > refute_count and support_average > 0.70:
            return {"claim" : claim,
                    "verdict": "TRUE",
                    "support_score" : support_average,
                    "refute_score" : refute_average,
                    "support_links": support_links,
                    "refute_links": refute_links}

        elif refute_count > support_count and refute_average > 0.75:
            return {"claim": claim,
                    "verdict": "FALSE",
                    "support_score": support_average,
                    "refute_score": refute_average,
                    "support_links": support_links,
                    "refute_links": refute_links}

        elif support_count == 0 and refute_count == 0:
            return {"claim": claim,
                    "verdict": "NO-DATA",
                    "support_score": support_average,
                    "refute_score": refute_average,
                    "support_links": support_links,
                    "refute_links": refute_links}

        # Neutral Cases where either the claim or the evidence is unclear.
        elif (support_count == refute_count) or (abs(support_average - refute_average) < 0.1):
            return {"claim": claim,
                    "verdict": "UNC-CONFLICT",
                    "support_score": support_average,
                    "refute_score": refute_average,
                    "support_links": support_links,
                    "refute_links": refute_links}

        elif max(support_average, refute_average) < 0.5:
            return {"claim": claim,
                    "verdict": "UNC-NOT-ENOUGH-DATA",
                    "support_score": support_average,
                    "refute_score": refute_average,
                    "support_links": support_links,
                    "refute_links": refute_links}

        else:
            return {"claim": claim,
                    "verdict": "CLAIM-UNC",
                    "support_score": support_average,
                    "refute_score": refute_average,
                    "support_links": support_links,
                    "refute_links": refute_links}



def speech_fact_check_serpAPI(video_path, model_name="Dzeniks/roberta-fact-check"):
    sp_tt_dict = speech_to_text(video_path) # OpenAI Whisper used to extract text from speech
    results = []

    claims = split_text_into_sentences(sp_tt_dict["text"]) # Adding the individual sentences from all the text into a list

    # Going through each claim individually
    for claim in claims:
        web_search_results = get_similar_from_web_search(claim) # Retrieves top 5 (can get more/less by changing the parameter num_results) google results for this claim.
        result = compare_claim_to_web_search(claim, web_search_results, model_name)
        results.append(result)
    return results



def speech_fact_check_webDriver(video_path, model_name="Dzeniks/roberta-fact-check"):
    sp_tt_dict = speech_to_text(video_path) # OpenAI Whisper used to extract text from speech
    results = []

    claims = split_text_into_sentences(sp_tt_dict["text"]) # Adding the individual sentences from all the text into a list

    # Going through each claim individually
    for claim in claims:
        web_search_results = bing_search(claim) # Retrieves top 5 (can get more/less by changing the parameter num_results) bing results for this claim.
        result = compare_claim_to_web_search(claim, web_search_results, model_name)
        results.append(result)

    return results