import sys

import cv2
from keras.models import load_model
import numpy as np

from face.src.utils.datasets import get_labels
from face.src.utils.inference import detect_faces
from face.src.utils.inference import draw_text
from face.src.utils.inference import draw_bounding_box
from face.src.utils.inference import apply_offsets
from face.src.utils.inference import load_detection_model
from face.src.utils.inference import load_image
from face.src.utils.preprocessor import preprocess_input

def main(path):
    # 载入数据和图像的参数
    image_path = path
    detection_model_path = 'E:/Projects/AIelder/Web_shown/face/src/trained_models/detection_models/haarcascade_frontalface_default.xml'
    emotion_model_path = 'E:/Projects/AIelder/Web_shown/face/src/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
    gender_model_path = 'E:/Projects/AIelder/Web_shown/face/src/trained_models/gender_models/simple_CNN.81-0.96.hdf5'
    emotion_labels = get_labels('fer2013')
    gender_labels = get_labels('imdb')
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 界限盒形状的超参数
    gender_offsets = (30, 60)
    gender_offsets = (10, 10)
    emotion_offsets = (20, 40)
    emotion_offsets = (0, 0)

    # 装载模型
    face_detection = load_detection_model(detection_model_path)
    emotion_classifier = load_model(emotion_model_path,compile=False)
    gender_classifier = load_model(gender_model_path,compile=False)

    # 获得用于推理的输入模型形状
    emotion_target_size = emotion_classifier.input_shape[1:3]
    gender_target_size = gender_classifier.input_shape[1:3]

    # loading images
    rgb_image = load_image(image_path, grayscale=False)
    gray_image = load_image(image_path, grayscale=True)
    gray_image = np.squeeze(gray_image)
    gray_image = gray_image.astype('uint8')

    faces = detect_faces(face_detection, gray_image)
    for face_coordinates in faces:
        x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)
        rgb_face = rgb_image[y1:y2, x1:x2]

        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]

        try:
            rgb_face = cv2.resize(rgb_face, (gender_target_size))
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

        rgb_face = preprocess_input(rgb_face, False)
        rgb_face = np.expand_dims(rgb_face, 0)
        gender_prediction = gender_classifier.predict(rgb_face)
        gender_label_arg = np.argmax(gender_prediction)
        gender_text = gender_labels[gender_label_arg]

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
        emotion_text = emotion_labels[emotion_label_arg]

        return gender_text, emotion_text

if __name__ == '__main__':
    main()