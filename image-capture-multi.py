import cv2
import time
from PIL import Image

# approx velocity 150 cm/s
# survey zone 11cm

def initialize_camera():
	cam = cv2.VideoCapture(1)
	if cam.isOpened():
		print 'camera found'

		width = cam.get(3)
		height = cam.get(4)
		exposure = cam.get(15)

		print 'width is %d' % width
		print 'height is %d' % height
		print 'exposure time is %d' % exposure
		return cam, width, height
	else:
		return False

def test_fps(cam): 
	start = time.time()
	i = 0
	retval, im = cam.read()

	while (time.time() - start) < 1:
		print (time.time() - start)
		retval, im = cam.read()
		# cv2.imshow('file', im)
		# cv2.imwrite(str(i) + ".png", im)
		i += 1

	del(cam)

def single_cap(cam): 
	filename = 'cap1.png'
	if cam.isOpened():
		retval, im = cam.read()
		cv2.imshow('file', im)
		cv2.imwrite(filename, im)
		image = Image.open(filename)
		im_width, im_height = image.size
		print 'captured image width is %d, height is %s' % (im_width, im_height)


	else:
		print 'not initialized camera'

def multi_cap(cam, number): 
	array = []
	if cam.isOpened():
		for k in range(0, int(number)):
				retval, im = cam.read()
				print k
				array.append(im)
	return array

def export_photos(array):
	for k in range (0, len(array)):
			filename = str(k) + ".jpg"
			cv2.imwrite(filename, array[k])
			image = Image.open(filename)
			im_width, im_height = image.size
			print 'captured image width is %d, height is %s' % (im_width, im_height)



def set_resolution(cam, x, y):
	cam.set(3,int(x))
	cam.set(4,int(y))

def set_exposure(cam, exp):
	exp = ca.get(15)
	print "exp is %d" % exp
	# cam.set(15, exp)


max_x = '1280'
max_y = '960'
cam, x, y = initialize_camera()
set_resolution(cam, 2304, 1536)
an_array = multi_cap(cam, 10)
export_photos(an_array)

