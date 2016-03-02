import cv2
from PIL import Image


def initialize_camera():
	# initializes camera using openCV
	#returns the width, height, and camera object 
	cam = cv2.VideoCapture(1)
	if cam.isOpened():
		cam.set(5, 8)
		set_resolution(cam, 1900, 1080)
		return cam

def capture():
	if cam.isOpened():
		retval, im = cam.read()
		filename = "im.png"
		cv2.imwrite(filename, im)

	reference_there = check_image(im)
	print "the reference is there? %s" % reference_there

def set_resolution(cam, x, y):
	# sets resolution for camera to take pictures with
	cam.set(3,int(x))
	cam.set(4,int(y))

cam = initialize_camera()
capture()
