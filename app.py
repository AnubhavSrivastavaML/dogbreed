from flask import Flask, request, jsonify
from datetime import datetime
from PIL import Image
import numpy as np
import sqlite3
import base64
import json
import cv2
import os





app = Flask(__name__)



	



labelsPath = "model.names"
LABELS = open(labelsPath).read().strip().split("\n")
weightsPath = "yolov3-tiny_6000.weights"
print(weightsPath)
configPath = "yolov3-tiny.cfg"
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def detect(image):
	image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	vehicle_info = []
	(H, W) = image.shape[:2]
	#print(H,W)
	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (960, 960),
		swapRB=True, crop=False)
	net.setInput(blob)
	
	layerOutputs = net.forward(ln)
	
	boxes = []
	confidences = []
	classIDs = []
	for output in layerOutputs:
		for detection in output:
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			if confidence > 0.25 :
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.2,0.3)
	print(idxs)
	if len(idxs) > 0:
		for i in idxs.flatten():
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
			text = "{}".format(LABELS[classIDs[i]])
			vehicle_info.append([x,y,w,h,text])
			#print(x,y,w,h)
			#image =cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
	return(vehicle_info)
	#return image
	



@app.route("/im_size", methods=["POST"])
def process_image():
	image = request.get_json()
	image = json.loads(image)['image']
	image = image.encode('utf-8')
	nparr = np.fromstring(base64.b64decode(image), np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	data = detect(img)
	print(data)
	return jsonify({'msg': 'success','status':'red','coords':data})










if __name__ == "__main__":
	app.run(host='0.0.0.0',port=8000,threaded=True)
	print("Server Terminated Successfully")

