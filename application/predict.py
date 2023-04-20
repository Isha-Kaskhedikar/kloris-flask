import tensorflow as tf
from tensorflow.keras import models
import h5py
import cv2,numpy as np
# @app.route("/predict")
def predict(img):
    # ['Isariopsis_leaf_spot' 'apple_rust' 'apple_scab' 'bacterial_spot'
    #  'black_measles' 'black_rot' 'common_rust' 'early_blight' 'gray_leaf_spot'
    #  'healthy' 'late_blight' 'leaf_mold' 'leaf_scorch' 'mosiac_virus'
    #  'northern_leaf_blight' 'powdery_mildew' 'septoria_leaf_spot'
    #  'spider_mite' 'target_spot' 'yellowLeaf__curl_virus']
    model = models.load_model('D:/RNH/kloris/kloris-flask/application/model/mobNet_smallDS.h5')
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (256, 256))
    img = np.reshape(image,[1,256,256,3])
    predict_x=model.predict(img) 
    print(predict_x)
    classs=np.argmax(predict_x,axis=1)
    print(classs)
    return str(classs[0])