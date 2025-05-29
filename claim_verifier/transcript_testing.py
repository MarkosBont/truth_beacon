from transcript_verifier import speech_to_text
import textwrap
import warnings

# Ignoring a warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")


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