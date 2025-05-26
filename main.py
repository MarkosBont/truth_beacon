from deepfake_detector.detector import extract_video_frames, predict_deepfake

print("\n")
print("**********Elon Musk Video Result**********")
video_elon_path = "/Users/markos/Desktop/elon_deepfake.mp4"
frames = extract_video_frames(video_elon_path)
elon_result = predict_deepfake(frames)
print(elon_result)
print('\n')
print("**********Erdogan Video Result**********")
video_erdogan_path = "/Users/markos/Desktop/erdogan_deepfake.mp4"
frames = extract_video_frames(video_erdogan_path)
erdogan_result = predict_deepfake(frames)
print(erdogan_result)

