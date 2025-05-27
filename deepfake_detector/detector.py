import cv2
import torch
import torch.nn.functional as F
from PIL import Image


def extract_video_frames(path, num_frames=10):
    frames = []
    cap = cv2.VideoCapture(path)
    total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameIndexes = []

    # adding evenly spaced video frames from the video
    for i in range(num_frames):
        index = int(i * total_video_frames / num_frames)
        frameIndexes.append(index)

    for index in frameIndexes:
        cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    cap.release()
    return frames


def predict_deepfake_from_frames(frames, model, processor):

    fake_probabilities = []

    # preprocessing the frames into PIL images to used by the model
    for f in frames:
        if not isinstance(f, Image.Image):
            f = Image.fromarray(f).convert("RGB")
        else:
            f = f.convert("RGB")

        inputs = processor(images=f, return_tensors="pt")
        with torch.no_grad():
            outputs= model(**inputs)
            probabilities = F.softmax(outputs.logits, dim=1)
            fake_probabilities.append(probabilities[0][0].item())

    avg_fake_probability = sum(fake_probabilities) / len(fake_probabilities)

    result = "FAKE" if avg_fake_probability > 0.5 else "NOT FAKE"

    return {
        "probabilities": fake_probabilities,
        "result": result,
        "confidence": str(round(avg_fake_probability*100, 2)) + " %"
    }


def video_deepfake_detector(path, model, processor, num_frames=10):
    video_frames = extract_video_frames(path, num_frames)
    result = predict_deepfake_from_frames(video_frames, model, processor)

    return result


