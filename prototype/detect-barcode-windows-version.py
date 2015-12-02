import cv2
import time
from PIL import Image
import thread
import os
import zbar

global capture_images, im_array, exported, export_array
im_array = [] #array that will collect all the pictures in real-time
export_array = [] #after we stop taking pictures, put all images to be exported in here so im_array can take mroe images
capture_images = False #don't start off taking pictures
exported = False

def initialize_camera():
	# initializes camera using openCV
	#returns the width, height, and camera object 
	cam = cv2.VideoCapture(1)
	if cam.isOpened():
		print 'camera found'

		width = cam.get(3)
		height = cam.get(4)
		return cam, width, height
	else:
		return False

def set_resolution(cam, x, y):
	#sets resolution for camera to take pictures with
	cam.set(3,int(x))
	cam.set(4,int(y))

def capture(cam):
	# runs a loop to take pictures, continuously going until KeyboardInterrupt (Ctrl+C)
	while True:
		if capture_images:
			# if we are supposed to be taking pictures right now
			print 'taking pictures'			
			if cam.isOpened():
				retval, im = cam.read()
				im_array.append(im)

def export_photos(array, timestamp):
	# takes an array of image files and a timestamp and creates folder using the timestamp, exports to there
	print timestamp, array
	global exported
	#making the folder and cd into it
	path = str(timestamp)
	os.makedirs(path)
	os.chdir(path)
	for k in range (0, len(array)):
			filename = str(k) + ".jpg"
			cv2.imwrite(filename, array[k])
			image = Image.open(filename)
			im_width, im_height = image.size
	#change back to parent directory
	os.chdir("../")
	exported = True
	# use the path to scan the images in the folder we just made
	scan_images(path)

def get_user_input():
	# controls whether or not we are taking pictures right now
	global capture_images, export_array, im_array, exported
	while True:
		#always asking for user input to control
		x = raw_input('Press Enter to toggle picture taking')
		if not x:
			#happens when you press Enter
			if capture_images:
				# if already taking pictures, turn it off
				capture_images = False
				print 'stop capturing'
				#if we haven't already exported, export the pictures by the timestamp
				if exported == False:
					print 'exporting'
					timestamp = time.time()
					export_array = im_array
					export_photos(export_array, timestamp)
					#empty image array again so we can take more pictures while exporting happens
					im_array = []
			else:
				# if not taking pictures right now, start
				print 'not exporting'
				capture_images = True
				exported = False

def scan_images(path):
	# print os.getcwd()
	# print path
	os.chdir(str(path))
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')

	barcodes = {}
	for i in os.listdir(os.getcwd()):
		pil = Image.open(i).convert('L')
		width, height = pil.size
		raw = pil.tostring()
		image = zbar.Image(width, height, 'Y800', raw)
		
		if scanner.scan(image):
		# extract results
		    for symbol in image:
		    	image = Image.open(i)
		    # do something useful with results
		        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
		        barcodes[path] = symbol.data
		        # get_object_image(symbol.data, barcodes)
		else:
		    print 'did not decode'
	os.chdir("../")
	
    

cam, x, y = initialize_camera()
set_resolution(cam, 2304, 1536)
thread.start_new_thread(capture, (cam,))
thread.start_new_thread(get_user_input, ())

while True:
	pass	