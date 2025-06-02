from claim_verifier.text_fact_checking import compare_claim_to_web_search
from text_fact_checking import speech_to_text, claim_should_be_fact_checked, split_text_into_sentences, get_similar_from_web_search
import textwrap
import warnings
import nltk

# Downloads the tokenizer data
nltk.download("punkt")
nltk.download("punkt_tab")

# Ignoring a warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

"""
videos = {
    "Elon Musk Deepfake": "/Users/markos/Desktop/elon_deepfake.mp4",
    "Erdogan Deepfake": "/Users/markos/Desktop/erdogan_deepfake.mp4",
    "Real Video": "/Users/markos/Desktop/r_video.mp4",
    "My Greek Video": "/Users/markos/Desktop/greek.mov"
}

for label, path in videos.items():
    print(f"********** {label} Result **********")
    result = speech_to_text(path)
    print("Language Detected:", result["language"])
    print("Transcript:\n")
    print(textwrap.fill(result["text"], width=80))
    print('\n')
    """

text = "Water boils at 100 degrees Celsius at sea level. The Great Wall of China is visible from the moon with a naked eye."
sentences = split_text_into_sentences(text)
for sentence in sentences:
    data = get_similar_from_web_search(sentence)
    #result = compare_claim_to_web_search(sentence, data)
    #print(result)
    print(data)


