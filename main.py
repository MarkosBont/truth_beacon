from deepfake_detector.detector import extract_video_frames, video_deepfake_detector
from transformers import AutoImageProcessor, SiglipForImageClassification, AutoModelForImageClassification


# Using a model trained on deepfakes from hugging face
# https://huggingface.co/prithivMLmods/deepfake-detector-model-v1#:~:text=deepfake%2Ddetector%2Dmodel%2Dv1%20is%20a%20vision%2Dlanguage,model%20uses%20the%20SiglipForImageClassification%20architecture.
#model_name = "prithivMLmods/deepfake-detector-model-v1"
#model = SiglipForImageClassification.from_pretrained(model_name)
#processor = AutoImageProcessor.from_pretrained(model_name,use_fast=True)
#model.eval()

# Using another model trained on deepfakes from hugging face
# https://huggingface.co/dima806/deepfake_vs_real_image_detection
model_name = "dima806/deepfake_vs_real_image_detection"
model = AutoModelForImageClassification.from_pretrained(model_name)
processor = AutoImageProcessor.from_pretrained(model_name)

print("**********Elon Musk Video Result**********")
elon_path = "/Users/markos/Desktop/elon_deepfake.mp4"
elon_result = video_deepfake_detector(elon_path, model, processor)
print(elon_result)
print('\n')

print("**********Erdogan Video Result**********")
erdogan_path = "/Users/markos/Desktop/erdogan_deepfake.mp4"
erdogan_result = video_deepfake_detector(erdogan_path, model, processor)
print(erdogan_result)
print('\n')

print("**********Real Video Result**********")
real_path = "/Users/markos/Desktop/r_video.mp4"
real_result = video_deepfake_detector(real_path, model, processor)
print(real_result)
print('\n')

print("**********High Quality Real Video Result**********")
real_path_hq = "/Users/markos/Desktop/r_video_high_quality.mp4"
real_result_hq = video_deepfake_detector(real_path_hq, model, processor)
print(real_result_hq)
print('\n')

print("**********My Video Result**********")
my_path = "/Users/markos/Desktop/my_video.mp4"
my_result = video_deepfake_detector(my_path, model, processor)
print(my_result)
