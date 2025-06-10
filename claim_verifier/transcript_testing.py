from claim_verifier.text_fact_checking import compare_claim_to_web_search
from text_fact_checking import speech_to_text, chunk_article, split_text_into_sentences, get_similar_from_web_search,bing_search, speech_fact_check_webDriver, speech_fact_check_serpAPI
import textwrap
import warnings
import nltk

# Downloads the tokenizer data
nltk.download("punkt")
nltk.download("punkt_tab")

# Ignoring a warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

videos = {
    "Elon Musk Deepfake": "/Users/markos/Desktop/elon_deepfake.mp4",
    "Erdogan Deepfake": "/Users/markos/Desktop/erdogan_deepfake.mp4",
    "test": "/Users/markos/Desktop/test.mov",
    "donald": "/Users/markos/Desktop/donald.mov",
}

video_path = videos["donald"]
results = bing_search("Portugal won the Nations League.")
print(results)

"""
for result in results:
    chunked = result[]
"""

