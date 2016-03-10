import cv2
import time
from PIL import Image
import threading
import os
import zbar
import Queue

capture_images = False # don't start off taking pictures
symbols_found = {}
barcode_validated = {}
capture_completed = threading.Event()
object_in_system = threading.Event()
q = Queue.Queue()

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

def initialize_camera(i):
	# initializes camera using openCV
	#returns the width, height, and camera object 
	print i
	cam = cv2.VideoCapture(i)
	if cam.isOpened():
		cam.set(5, 8)
		return cam

def set_resolution(cam, x, y):
	# sets resolution for camera to take pictures with
	cam.set(3,int(x))
	cam.set(4,int(y))

def test_capture(cam, timestamp):
	# runs a loop to take pictures, continuously going until KeyboardInterrupt (Ctrl+C)
	if cam.isOpened():
		retval, im = cam.read()
		is_object_present = check_if_object_present(im)
		if is_object_present:
			object_in_system.clear()
			q.put(timestamp)
			object_in_system.set()


def capture(cam, timestamp):
	k = 0
	# runs a loop to take pictures, continuously going until KeyboardInterrupt (Ctrl+C)
	global capture_completed
	while True:
		if not timestamp in barcode_validated.keys():
			# if we are supposed to be taking pictures right now	
			# print 'before starting image array length is %s' % len(im_array)
			if cam.isOpened():
				capture_completed.clear()
				retval, im = cam.read()
				if not waiting_for_object: 
					threading.Thread(target=export_photos, args=(im,timestamp,k)).start()
				capture_completed.set()
				k += 1

def export_photos(im, timestamp, k):
	# takes an array of image files and a timestamp and creates folder using the timestamp, exports to there
	# making the folder and cd into it
	
	path = str(timestamp)
	if not os.path.isdir(path):
		print "hello"
		os.mkdir(path)
	
	filename = str(k) + ".png"
	cv2.imwrite(path + '/' + filename, im)
	# use the path to scan the images in the folder we just made
	scan_images(path,filename, timestamp)

def wait_for_object_to_be_present(): 
	while True: 
		timestamp = time.time()
		print "taking a test picture"
		test_capture(cameras[0], timestamp)

def start_camera_threads():
	#starting other camera threads
		while True: 
			object_in_system.wait()
			
			print "im not waiting anymore"
			
			if not q.empty():
				curr_timestamp = q.get()
				print curr_timestamp

				threading.Thread(target=capture, args=(cameras[1],curr_timestamp)).start()
				threading.Thread(target=capture, args=(cameras[2],curr_timestamp)).start()


def scan_images(path, filename, timestamp):
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')

	pil = Image.open(path+ '/' + filename).convert('L')
	width, height = pil.size
	raw = pil.tostring()
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

def check_if_object_present(im):
	#returns whether photo-gate is blocked

	threshold = 100	
	pixels = {}
	reference_present = True
	#im[x,y] where x is the row (so going down) and y are columns are going across
	references = [[57,78,127],[32,22,95],[70,50,35]]
	pixels = [im[950,980], im[950,1015], im[950,1045]]

	for i in range(0,3):
		for j in range(0,3):
			colour_difference = pixels[i][j] - references[i][j]
			print i, j
			print pixels[i]
			print references[i]

			print colour_difference

			if abs(colour_difference) >= threshold:
				reference_present = False
	print "reference is present %s" % reference_present
	return True

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

cameras =  {}
for i in range(0,2):
	cameras[i] = initialize_camera(i)
	print cameras

wait_for_object_to_be_present()
start_camera_threads()

try:
	while True:
		pass	
except (KeyboardInterrupt, SystemExit):
  print '\n! Received keyboard interrupt, quitting threads.\n'
