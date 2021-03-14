from flask import Flask
import tensorflow as tf
from PIL import Image


app = Flask(__name__)

tf.keras.backend.clear_session()
model = tf.keras.models.load_model('my_model.h5')
print(model.summary())

@app.route('/',methods=["POST"])
def getInference():
	img = Image.open(request.files['file'])
	return 'Success!'
	


if __name__ == '__main__':
	app.run(debug = True,use_reloader=False)
	
	

