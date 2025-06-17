# Truth Beacon

# Truth Beacon

**Truth Beacon** is an AI-powered fact-checking system that analyzes factual claims and determines their truthfulness. It uses natural language models to evaluate claims and generate clear, justified verdicts with context.

## Project Overview

Truth Beacon started as a system combining traditional web scraping and natural language inference (NLI). The original model scraped search results from the web and compared them against a claim using an NLI model from Hugging Face. While this approach showed potential, it faced major hurdles in real-world deployment—most notably:

- Frequent and inconsistent captchas
- Rate-limiting from search engines
- Parsing inconsistencies in webpage structures

After extensive testing, it became clear that this method was unreliable for production use.

As a result, the project pivoted to a more robust and scalable solution: integrating an LLM (Large Language Model) through OpenAI's API. This allowed Truth Beacon to perform the following within a single, well-engineered prompt:

- Extract claims from a body of text
- Search for and synthesize relevant background information (via LLM's knowledge)
- Assess truthfulness based on up-to-date context
- Generate a natural-language explanation and verdict

---

## Features

- **Claim Extraction**: Detects and isolates factual claims from user input or documents.
- **Fact Checking**: Uses OpenAI’s API to perform reasoning over the claim.
- **Verdict Generation**: Outputs clear justifications and verdict labels: `True`, `False`, or `Unverified`.
- **Supporting Claims**: Outputs for each claim include supporting links for the verdict. Even if the claim is unverifiable, links are given to allow the user to manually fact-check.

---

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/MarkosBont/truth_beacon.git
cd truth_beacon
pip install -r requirements.txt
