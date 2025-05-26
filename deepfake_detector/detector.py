import cv2
import os
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
import torch.nn.functional as F
import numpy as np

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

def predict_deepfake(frames):
    # Prototype of a model (not the actual one that will be used)
    model = resnet18(weights = ResNet18_Weights.DEFAULT)
    model.fc = torch.nn.Linear(in_features=model.fc.in_features, out_features=2)
    model.eval()

    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    # preprocessing the frames into tensors to used by the model
    inputs = []
    for f in frames:
        t = transform(f)
        inputs.append(t)

    inputs = torch.stack(inputs)

    # generating and returning a prediction
    with torch.no_grad():
        outputs = model(inputs)
        fake_probabilities = F.softmax(outputs, dim=1)[:, 1]
        avg_fake_probability = fake_probabilities.mean().item()

    outcome = "Fake" if avg_fake_probability > 0.5 else "Not Fake"
    return {
        "probabilities": fake_probabilities,
        "outcome": outcome,
        "confidence": str(round(avg_fake_probability * 100, 3)) + " %"
    }


