from flask import Flask, request, jsonify
import tensorflow as tf
from datetime import datetime
from PIL import Image
import numpy as np
import base64
import json
import cv2
import os


app = Flask(__name__)


tf.keras.backend.clear_session()
model = tf.keras.models.load_model('my_model.h5')

categories = ['beagle', 'chihuahua', 'doberman',
              'french_bulldog', 'golden_retriever', 
              'malamute', 'pug', 'saint_bernard',
              'scottish_deerhound','tibetan_mastiff']
 
 
def predict(image):
	image = cv2.resize(image,(224,224))
	imageArray = np.expand_dims(image,axis=0)
	preds = model.predict(imageArray)
	return categories[np.argmax(preds)],np.max(preds)


@app.route("/im_size", methods=["POST"])
def process_image():
	image = request.get_json()
	image = json.loads(image)['image']
	image = image.encode('utf-8')
	nparr = np.fromstring(base64.b64decode(image), np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	label , confidence = predict(img)
	print(label , confidence)
	return jsonify({'msg': 'success','breed':label,'score':str(confidence)})


if __name__ == "__main__":
    app.run(debug=False)
    
    


