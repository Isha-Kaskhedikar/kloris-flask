import tensorflow as tf
from tensorflow.keras import models
from keras.utils import load_img, img_to_array
import h5py
import cv2,numpy as np
import requests

# @app.route("/predict")
def predict(img):
    labels=['Isariopsis_leaf_spot', 'apple_rust', 'apple_scab', 'bacterial_spot',
     'black_measles', 'black_rot', 'common_rust', 'early_blight', 'gray_leaf_spot',
     'healthy', 'late_blight', 'leaf_mold', 'leaf_scorch', 'mosiac_virus',
     'northern_leaf_blight', 'powdery_mildew', 'septoria_leaf_spot',
     'spider_mite', 'target_spot', 'yellowLeaf__curl_virus']
    
    labels1=["Apple_scab",
    "Apple_black_rot",
    "Apple_cedar_apple_rust",
    "Apple_healthy",
    "Background_without_leaves",
    "Blueberry_healthy",
    "Cherry_powdery_mildew"
    "Cherry_healthy",
    "Corn_gray_leaf_spot",
    "Corn_common_rust",
    "Corn_northern_leaf_blight",
    "Corn_healthy",
    "Grape_black_rot",
    "Grape_black_measles",
    "Grape_leaf_blight",
    "Grape_healthy",
    "Orange_haunglongbing",
    "Peach_bacterial_spot",
    "Peach_healthy",
    "Pepper_bacterial_spot",
    "Pepper_healthy",
    "Potato_early_blight",
    "Potato_healthy",
    "Potato_late_blight",
    "Raspberry_healthy",
    "Soybean_healthy",
    "Squash_powdery_mildew",
    "Strawberry_healthy",
    "Strawberry_leaf_scorch",
    "Tomato_bacterial_spot",
    "Tomato_early_blight",
    "Tomato_healthy",
    "Tomato_late_blight",
    "Tomato_leaf_mold",
    "Tomato_septoria_leaf_spot",
    "Tomato_spider_mites_two-spotted_spider_mite",
    "Tomato_target_spot",
    "Tomato_mosaic_virus",
    "Tomato_yellow_leaf_curl_virus"]
    model = models.load_model('application/model/mobNet_bigDS.h5')
    r = requests.get(img)
    with open('google_logo.png', 'wb') as f:
        f.write(r.content)
    
    IMG_SIZE=256
    #load the image
    my_image = load_img('google_logo.png', target_size=(IMG_SIZE, IMG_SIZE))
    #preprocess the image
    my_image = img_to_array(my_image)/255
    # print(my_image)
    my_image = my_image.reshape((1, my_image.shape[0], my_image.shape[1], my_image.shape[2]))
    # my_image = preprocess_input(my_image)

    #make the prediction
    prediction = model.predict(my_image)
    # print(prediction)
    classs=np.argmax(prediction,axis=1)
    # print(classs)
    # image = cv2.imread('google_logo.png')
    # # image = cv2.imread(img)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.resize(image, (256, 256))
    # img = np.reshape(image,[1,256,256,3])
    # predict_x=model.predict(img) 
    # print(predict_x)
    # classs=np.argmax(predict_x,axis=1)
    print(classs)
    return str(labels1[classs[0]])