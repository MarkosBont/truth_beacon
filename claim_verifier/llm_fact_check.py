import os
import dotenv
from openai import OpenAI
import re
from claim_verifier.text_fact_checking import speech_to_text

def fact_check_llm(claim):
    # Load environment variables from .env file
    dotenv.load_dotenv()

    # Get API key from environment
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in your environment or .env file.")

    # Initialising the OpenAI client
    client = OpenAI(api_key=openai_key)

    # Prompt entered in the LLM
    prompt = f"""
    You are an intelligent fact-checking assistant. Given a passage of text, your job is to:

    1. Extract the main factual claims:
    - Identify statements that assert something verifiable about the world (past or present).
    - Ignore subjective opinions, rhetorical questions, or vague generalizations.

    2. Fact-check each claim:
    - Perform live web searches using the web search tool.
    - Construct accurate and focused queries using keywords from the claim (e.g., names, dates, locations, or institutions).
    - Prefer results from authoritative domains such as .gov, .edu, .org, and well-established news outlets.
    - If multiple sources are needed to verify the claim, use them collectively.
    - Disregard non-authoritative or user-generated content (e.g., blogs, Reddit, Quora).

    3. Return results as a JSON-like string:
    For each verified claim, return a dictionary with:
    - "claim": The exact text of the claim.
    - "verdict": One of "true", "false", or "unverified".
    - "supporting_links": A list of 2–3 **unique and domain-distinct** reputable URLs used to verify the claim.

      Each URL in "supporting_links" must:
    - Come from a different domain (e.g., no more than one link from wikipedia.org).
    - Be directly relevant to verifying the specific claim.
    - Not repeat domains already used in that claim’s link list.

    Do not include multiple links from the same website (even if the pages are different).
    Prioritize diversity of sources (e.g., use one link from a news site, one from a government site, etc., where available).

    Do NOT include anything else as part of your response.

    Output format:
    [
      {{
        "claim": "Claim text here.",
        "verdict": "true/false/unverified",
        "supporting_links": ["https://credible.source1.com", "https://other.source2.com", ...]
      }},
      ...
    ]

    If no verifiable claims are found in the text, return an empty list: []
    
    If you are unsure of any results you find, set "unverified" as a verdict. You can still return the supporting links and allow the user to manually fact check.
    

    Input Text:

    {claim}
    """

    # Making the API call
    response = client.responses.create(
        model="gpt-4.1",
        tools=[{"type": "web_search_preview"}],
        input=prompt
    )


    return extract_json_text(response.output_text) # Returns only the actual JSON as a string


def extract_json_text(output_text):
    """
    Removes markdown code block formatting from GPT responses, if present.
    Handles ```json, ```python, or plain ``` wrappers.
    """
    # Pattern matches any ```json/python ... ```
    match = re.search(r"```(?:json|python)?\s*(.*?)\s*```", output_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # If no wrapping was found, assume it's already plain JSON
    return output_text.strip()


def full_llm_fact_check(video_path):
    sp_tt_dict = speech_to_text(video_path) # OpenAI Whisper used to extract text from speech
    result_json = fact_check_llm(sp_tt_dict["text"]) # Enters the text into the llm fact-checker

    return result_json
