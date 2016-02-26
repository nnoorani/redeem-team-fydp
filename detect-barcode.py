import cv2
import time
from PIL import Image
import threading
import os
import zbar

capture_images = False # don't start off taking pictures
symbols_found = {}
barcode_validated = {}
capture_completed = threading.Event()

database = {
	"6820020094" : "products/chocolate-milk.jpg",
	"06741806" : "products/fanta.jpg",
	"06782900" : "products/coke.jpg",
	"064200150224" : "products/spaghetti.jpg",
	"058496423346" : "products/uncleben.jpg",
	"060383674304": "products/tomatoes.jpg",
	"066721020376" : "products/triscuit.jpg",
	"060410014431" : "products/pretzel.jpg"
}

def initialize_camera():
	# initializes camera using openCV
	#returns the width, height, and camera object 
	cam = cv2.VideoCapture(0)
	if cam.isOpened():
		cam.set(5, 8)
		return cam

def set_resolution(cam, x, y):
	# sets resolution for camera to take pictures with
	cam.set(3,int(x))
	cam.set(4,int(y))

def capture(cam, timestamp):
	k = 0
	# runs a loop to take pictures, continuously going until KeyboardInterrupt (Ctrl+C)
	global im_array
	global capture_completed
	while True:
		if capture_images and not timestamp in barcode_validated:
			# if we are supposed to be taking pictures right now	
			# print 'before starting image array length is %s' % len(im_array)
			if cam.isOpened():
				capture_completed.clear()
				retval, im = cam.read()
				threading.Thread(target=export_photos, args=(im,timestamp,k)).start()
				capture_completed.set()
				k += 1

def export_photos(im, timestamp, k):
	# takes an array of image files and a timestamp and creates folder using the timestamp, exports to there
	# making the folder and cd into it
	
	path = str(timestamp)
	if not os.path.isdir(path):
		os.mkdir(path)
	
	filename = str(k) + ".png"
	cv2.imwrite(path + '/' + filename, im)
	# use the path to scan the images in the folder we just made
	scan_images(path,filename, timestamp)

def get_user_input():
	global im_array, capture_images, exporting, capture_completed
	# controls whether or not we are taking pictures right now
	while True:
		#always asking for user input to control
		x = raw_input('Press Enter to toggle picture taking')
		print x
		if not x:
			#happens when you press Enter
			if capture_images:
				# if already taking pictures, turn it off
				capture_images = False
			else:
				# if not taking pictures right now, start taking pictures
				capture_images = True
				timestamp = time.time()
				threading.Thread(target=capture, args=(cam,timestamp)).start()

def scan_images(path, filename, timestamp):
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')

	pil = Image.open(path+ '/' + filename).convert('L')
	width, height = pil.size
	raw = pil.tobytes()
	image = zbar.Image(width, height, 'Y800', raw)
	
	if scanner.scan(image):
	# extract results
	    for symbol in image:
	    	print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
	    	if (timestamp in symbols_found.keys()):
	    		if symbols_found[timestamp] == symbol.data:
	    			print "success, validated barcode"
	    			barcode_validated[timestamp] = True
	    			break
	    	else: 
	    		symbols_found[timestamp] = symbol.data
	else:
	    print 'did not decode'
	
	print 'exit symbol loop'	
	# product_lookup(final_list)

def product_lookup(barcode):
	print barcode
	if barcode:
		if database.has_key(barcode):
			print database[barcode]
			product_img = cv2.imread(database[barcode]);
			cv2.imshow('product', product_img)
			cv2.waitKey(0)
		else:
			print "Image for this barcode does not exist yet"

cam = initialize_camera()
set_resolution(cam, 1900, 1080)
user_input_thread = threading.Thread(target=get_user_input, args=())
user_input_thread.setDaemon(True)

user_input_thread.start()

try:
	while True:
		pass	
except (KeyboardInterrupt, SystemExit):
  print '\n! Received keyboard interrupt, quitting threads.\n'
