import cv2
from PIL import Image


def initialize_camera():
	# initializes camera using openCV
	#returns the width, height, and camera object 
	cam = cv2.VideoCapture(0)
	if cam.isOpened():
		cam.set(5, 8)
		set_resolution(cam, 1900, 1080)
		return cam

def capture():
	if cam.isOpened():
		retval, im = cam.read()
		filename = "im.png"
		cv2.imwrite(filename, im)

	check_image(im)

def set_resolution(cam, x, y):
	# sets resolution for camera to take pictures with
	cam.set(3,int(x))
	cam.set(4,int(y))

def check_image(im):	
	height, width = im.shape[:2]
	print width
	print height
	print im[1070,10]



cam = initialize_camera()
capture()
