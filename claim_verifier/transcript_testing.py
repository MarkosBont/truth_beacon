from claim_verifier.text_fact_checking import compare_claim_to_web_search
from text_fact_checking import speech_to_text, claim_should_be_fact_checked, split_text_into_sentences, get_similar_from_web_search, speech_fact_check
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
    "test3": "/Users/markos/Desktop/test3.mov",
}

video_path = videos["test3"]
speech_fact_check(video_path)