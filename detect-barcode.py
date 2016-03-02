import cv2
import time
from PIL import Image
import threading
import os
import zbar

im_array = [] # array that will collect all the pictures in real-time
capture_images = False # don't start off taking pictures
capture_completed = 0
exporting = False
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

def initialize_cameras():
	# initializes camera using openCV
	#returns camera object 
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
	frame_rate = 1
	# runs a loop to take pictures, continuously going until KeyboardInterrupt (Ctrl+C)
	global im_array
	global capture_completed
	while True:
		if capture_images:
			# if we are supposed to be taking pictures right now	
			print 'before starting image array length is %s' % len(im_array)
			if cam.isOpened():
				print 'taking pictures'
				capture_completed.clear()
				retval, im = cam.read()
				threading.Thread(target=export_photos, args=(im,timestamp,k)).start()
				time.sleep(frame_rate)
				print "done"
				capture_completed.set()

def export_photos(array, timestamp):
	global exporting
	exporting = True
	# takes an array of image files and a timestamp and creates folder using the timestamp, exports to there
	# making the folder and cd into it
	path = str(timestamp)
	os.makedirs(path)
	for k in range (0, len(array)):
		filename = str(k) + ".png"
		cv2.imwrite(path + '/' + filename, array[k])
	exporting = False
	# use the path to scan the images in the folder we just made
	scan_images(path,filename,timestamp)

def get_user_input():
	# this method will eventually be obsoletes
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
				capture_completed.wait()
				print "capture completed"
				timestamp = time.time()
				export_array = im_array
				im_array = []				
				threading.Thread(target=export_photos, args=(export_array, timestamp)).start()
			else:
				# if not taking pictures right now, wait till exporting True
				capture_images = True

def scan_images(path):
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')

	#used for validating two barcodes
	found_symbol = ""
	barcode_validated = False
	
	# array of all pictures taken
	files = [f for f in os.listdir(path)]

	for i in files:
		pil = Image.open(path+ '/' + i).convert('L')
		width, height = pil.size
		raw = pil.tostring()
		image = zbar.Image(width, height, 'Y800', raw)
		
		if scanner.scan(image):
		# extract results
		    for symbol in image:
		    	print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
		    	if (found_symbol and (symbol.data == found_symbol)):
		    		print "success, validated barcode"
		    		barcode_validated = True
		    		break
		    	else: 
		    		found_symbol = symbol.data
		else:
		    print 'did not decode'
		
		print 'exit symbol loop'
		print barcode_validated
		if barcode_validated:
			break

	pil = Image.open(path+ '/' + filename).convert('L')
	width, height = pil.size
	raw = pil.tobytes()
	image = zbar.Image(width, height, 'Y800', raw)
	
	if not timestamp in barcode_validated.keys():
		results = scanner.scan(image)
	
	if results:
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
	references = [[155,156,198],[106,139,140]]
	pixels = [im[1000,40], im[1000,300]]
	print pixels[0]
	print pixels[1]

	print len(pixels)

	for i in (0,1):
		if (pixels[i][i] < (references[i][i] - threshold)) or (pixels[i][i] > (references[i][i] + threshold)):
			reference_present = False

	return reference_present

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

#creating threads for capturing and getting user input
capture_thread = threading.Thread(target=capture, args=(cam,))
capture_thread.setDaemon(True)
user_input_thread = threading.Thread(target=get_user_input, args=())
user_input_thread.setDaemon(True)

#start the threads
capture_thread.start()
user_input_thread.start()

#keep the application running
try:
	while True:
		pass	
except (KeyboardInterrupt, SystemExit):
  print '\n! Received keyboard interrupt, quitting threads.\n'
