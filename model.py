from  keras.models import load_model
from keras.applications.vgg16 import  preprocess_input, decode_predictions, VGG16
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from glob import glob
import cv2
import os
import json

VGG16_Model = VGG16(weights='imagenet', include_top=True, input_shape=None, input_tensor=None)
VIDEO_FRAMES = glob("static/video_frames/*.jpg")

distinct_objects = set()

def video_to_frames(video_file):
    vidcap = cv2.VideoCapture(video_file)
    success,image = vidcap.read()
    count = 0
    while(vidcap.isOpened()):
        success, frame = vidcap.read()
        if success:
            cv2.imwrite('static/video_frames/frame'+str(count)+'.jpg', frame)
        else:
             break
        count = count+1
        
    detected_objects = feeding_frames_to_vgg16(VIDEO_FRAMES)
    with open('objects.txt', 'w') as f:
        f.write(json.dumps(detected_objects))
    vidcap.release()
    cv2.destroyAllWindows()

  

def feeding_frames_to_vgg16(frame_list):
    features = []
    for item in frame_list:
        image = load_img(item, target_size=(224, 224))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = preprocess_input(image)
        y_pred = VGG16_Model.predict(image)
        label = decode_predictions(y_pred)
        features.append(label[0][1][1])
        #distinct_objects.add(label[0][1][1])
    return features

def search_frames(obj):
    with open('objects.txt', 'r') as f:
        detected_objects = json.loads(f.read())
    result_list = []
    indexes = []
    if obj in set(detected_objects):
      for i in range(len(detected_objects)):
          if obj.__eq__(detected_objects[i]):
              img_url = VIDEO_FRAMES[i]
              path_arr = img_url.split('\\')
              img_url = os.path.join('video_frames/', path_arr[1])
              result_list.append(img_url)
              indexes.append(i)
    else:
        return 'Object does not exist' 
    return result_list 

        
        