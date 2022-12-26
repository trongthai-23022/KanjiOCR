from flask import Flask,request
from flask import jsonify
from tensorflow import keras
import numpy as np
import Labels
import modelProcess as pr
from werkzeug.utils import secure_filename
import os
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
UPLOAD_FOLDER = 'upload/'
PATH = 'upload/requestImg.jpg'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = keras.models.load_model('kanji.h5')

# @app.route("/")
# def home():
#     return jsonify({'name':'愛'})

@app.route('/model',methods = ["POST","GET"])
def predict():

    if request.method == "POST":
        # print("request data", np.asarray(request.files))
        try:
            # print(request)
            data = request.form.get("data")
            pr.covertBase64ToImg(data)
            img = pr.readAndProcessImg(PATH)
            img2 = pr.readAndNOTProcessImg(PATH)
            # print(np.asarray(img))
            result = model.predict(img.reshape(1,48,48,1))
            result2 = model.predict(img2.reshape(1,48,48,1))
            arr_predict = pr.sortPredict(result)
            arr_predict2 = pr.sortPredict(result2)
            arr_predict = arr_predict2 + arr_predict
            js = pr.gettop10(arr_predict)
            return jsonify({'1':(js[0]),
                            '2':(js[1]),
                            '3':(js[2]),
                            '4':(js[3]),
                            '5':(js[4]),
                            '6':(js[5]),
                            '7':(js[6]),
                            '8':(js[7]),
                            '9':(js[8])
            })
        except Exception as e:
            return jsonify(e)
    if request.method == "GET":
        try:
            return jsonify(Labels.labels)
        except Exception as e:
            return jsonify(e)
if __name__ == "__main__":
    app.run(debug=True)