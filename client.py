import requests
from flask import jsonify
import base64
import json

url = 'http://localhost:5000/im_size'
image_file = 'images/0a0b97441050bba8e733506de4655ea1.jpg'
image = open(image_file, 'rb')
image_read = image.read()
image_64_encode = base64.b64encode(image_read)
dic = {'image': image_64_encode.decode('utf-8')}
my_img = json.dumps(dic)

r = requests.post(url, json=my_img)


print(r.json())

