from flask import Flask, render_template, request, redirect, url_for
import keras
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform

import cv2
import h5py
import pandas as pd
import numpy as np
from datetime import datetime
import os


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/mnist', methods=['GET', 'POST'])
def mnist():
    ans = None

    if request.method == 'POST':
        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            model = load_model('./templates/mnist/mnist_model.h5')

        ## 画像処理
        try:
            stream = request.files['img'].stream

            img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, 1)

            ## ===== データ仮保存
            cv2.imwrite("./static/mnist/test.png", img)

            img = cv2.resize(img, (28, 28))

            ## グレースケール変換
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ## 白：0, 黒：1に変換
            img = cv2.bitwise_not(img)

            img = np.array(img)/255

            predicts = model.predict(img.reshape(-1, 28, 28, 1))
            ans = np.argmax(predicts, axis=1)[0]

            ## ===== データ名変更
            dt_now = datetime.now().strftime("%H%M%S")
            os.rename('./static/mnist/test.png', './static/mnist/'+str(ans)+str(dt_now)+'.png')
        except:
            ans = 'Error'

    images = os.listdir('./static/mnist/')
    
    return render_template("/mnist/mnist.html", ans=ans, images=images)



if __name__ == "__main__":
    app.run(debug=True)