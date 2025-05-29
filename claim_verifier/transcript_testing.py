from transcript_verifier import speech_to_text, claim_should_be_fact_checked, split_text_into_sentences
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

sentences_list = split_text_into_sentences("The Amazon River is the second longest river in the world, stretching over 6,400 kilometers. It flows through Brazil, Peru, and Colombia before emptying into the Atlantic Ocean. The moon has a diameter of about 3,474 kilometers and takes roughly 27.3 days to orbit Earth. Albert Einstein published his theory of general relativity in 1915, revolutionizing our understanding of gravity. The United States dropped atomic bombs on Hiroshima and Nagasaki in August 1945 during World War II. The human body has 206 bones, with the femur being the longest. The Great Wall of China is more than 21,000 kilometers long and was primarily built to defend against invasions from northern tribes. The Eiffel Tower in Paris was completed in 1889 and stands about 330 meters tall. In 2021, the global population surpassed 7.8 billion people. The euro is the official currency of 20 of the 27 European Union countries.")
worthy_claims = []

for s in sentences_list:
    result = claim_should_be_fact_checked(s)
    print(s +" :" + str(result))

