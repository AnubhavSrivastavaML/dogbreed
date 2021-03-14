import base64
#import json

'''
image = open('/home/anubhav/DeepLearning/Dataset/faceDataset/images (77).jpg', 'rb')
image_read = image.read()
image_64_encode = base64.encodestring(image_read)
image_64_decode = base64.decodestring(image_64_encode) 
image_result = open('deer_decode.jpg', 'wb') # create a writable image and write the decoding result
image_result.write(image_64_decode)

'''
'''
#from __future__ import print_function
import requests
import json
import cv2

addr = 'http://localhost:5000'
test_url = addr + '/im_size'

# prepare headers for http request
content_type = '/im_size'

img = cv2.imread('/home/anubhav/img.jpg')
_, img_encoded = cv2.imencode('.jpg', img)


jpg = base64.b64encode(img_encoded)

# send http request with image and receive response
response = requests.post(test_url,json.dumps({'data':jpg}))
# decode response
print(response)

# expected output: {u'message': u'image received. size=124x124'}
'''
import requests
from flask import jsonify
import base64
import json

url = 'http://localhost:5000/im_size'
image_file = '/home/anubhav/Competitions/dog_breed/test/0a0b97441050bba8e733506de4655ea1.jpg'
image = open(image_file, 'rb')
image_read = image.read()
image_64_encode = base64.b64encode(image_read)
dic = {'image': image_64_encode.decode('utf-8')}
my_img = json.dumps(dic)

r = requests.post(url, json=my_img)


print(r.json())

