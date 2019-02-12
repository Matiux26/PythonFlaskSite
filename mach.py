#Tensorflow
import tensorflow as tf
from tensorflow import keras

#Helber liblaries
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

class Machine_learning:
	
	train_images = 0
	train_labels = 0
	test_images = 0
	test_labels = 0
	class_names = 0
	
	def __init__(this):
		digits_mnist = keras.datasets.mnist
		(train_images, this.train_labels), (test_images, this.test_labels) = digits_mnist.load_data()
		this.train_images = train_images / 255.0
		this.test_images = test_images / 255.0
		this.class_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six',
						'seven', 'eight', 'nine']
	def main(this):
		return this.make_prediction(this.load_image_to_predict())
		#this.train_model(this.create_model())
		
	def create_model(this):
		model = keras.Sequential([
			keras.layers.Flatten(input_shape=(28, 28)),
			keras.layers.Dense(128, activation=tf.nn.relu),
			keras.layers.Dense(10, activation=tf.nn.softmax)
		])

		model.compile(optimizer=tf.train.AdamOptimizer(),
						loss='sparse_categorical_crossentropy',
						metrics=['accuracy'])
		return model

	def train_model(this,model):
		checkpoint_path = "training_1/cp.ckpt"
		checkpoint_dir = os.path.dirname(checkpoint_path)
		
		cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
															save_weights_only=True,
															verbose=1)
		model.fit(this.train_images, this.train_labels, epochs=4,
					validation_data = (this.test_images, this.test_labels),
					callbacks = [cp_callback])
		test_loss,test_acc = model.evaluate(this.test_images, this.test_labels)
		print('Test accuracy: ', test_acc)

	def load_image_to_predict(this):
		img = cv2.imread("static/a7a7cf93-d3e8-43cd-875f-1613957dac5b.png",0)
		img = img / 255.0
		img = 1-img
		img = (np.expand_dims(img,0))
		return img

	def make_prediction(this,img):
		checkpoint_path = "training_1/cp.ckpt"
		model = this.create_model()
		model.load_weights(checkpoint_path)
		predictions = model.predict(img)
		return np.argmax(predictions[0])
if __name__ == '__main__':
	Machine_learning().main()