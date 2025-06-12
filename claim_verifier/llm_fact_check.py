import dotenv
import os
from openai import OpenAI
import streamlit as st

dotenv.load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def fact_check_llm(claim):
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1",
        tools=[{"type": "web_search_preview"}],
        input=
        f"""You are an intelligent fact-checking assistant. Given a passage of text, your job is to:
                1. Extract the main factual claims:
                - Identify statements that assert something verifiable about the world (past or present).
                - Ignore subjective opinions, rhetorical questions, or vague generalizations.

                2. Fact-check each claim:
                - Perform live web searches using reputable sources such as major news outlets, academic institutions, government websites, or expert organizations.
                - Assess the truthfulness of each claim as either:
                - "true" – if supported by strong and credible evidence.
                - "false" – if directly contradicted by reliable sources.
                - "unverified" – if the claim cannot be confirmed or refuted based on available credible information.

                3. Return results as a JSON-like string:
                For each verified claim, return a dictionary with:
                - "claim": The exact text of the claim.
                - "verdict": One of "true", "false", or "unverified".
                - "supporting_links": A list of 1–3 reputable source URLs used to verify the claim.
                
                Do NOT include anything else as part of your response.

                Output format:
                [
                {
                     "claim": "Claim text here.",
                    "verdict": "true/false/unverified",
                    "supporting_links": ["https://credible.source1.com", "https://credible.source2.com"]
                },
                ...
                ]

                If no verifiable claims are found in the text, return an empty list: []

Input Text:

{claim}

""")

    return response.output_text


