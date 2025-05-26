import cv2
import os

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

