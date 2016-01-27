import cv2
import time
from PIL import Image
import threading
import os
import zbar
from urllib2 import Request, urlopen, URLError

im_array = [] # array that will collect all the pictures in real-time
capture_images = False # don't start off taking pictures
capture_completed = 0
exporting = False
capture_completed = threading.Event()

database = {
	"6820020094" : "products/chocolate-milk.jpg",
	"06741806" : "products/fanta.jpg"
}

def initialize_camera():
	# initializes camera using openCV
	#returns the width, height, and camera object 
	cam = cv2.VideoCapture(0)
	if cam.isOpened():
		print 'camera found'
		return cam

def set_resolution(cam, x, y):
	# sets resolution for camera to take pictures with
	cam.set(3,int(x))
	cam.set(4,int(y))

def capture(cam):
	# runs a loop to take pictures, continuously going until KeyboardInterrupt (Ctrl+C)
	global im_array
	global capture_completed
	while True:
		if capture_images:
			# if we are supposed to be taking pictures right now		
			if cam.isOpened():
				print 'taking pictures'
				capture_completed.clear()
				retval, im = cam.read()
				im_array.append(im)
				print "image array length is %s" % len(im_array)
				capture_completed.set()

def export_photos(array, timestamp):
	global exporting
	print timestamp
	exporting = True
	# takes an array of image files and a timestamp and creates folder using the timestamp, exports to there
	# making the folder and cd into it
	path = str(timestamp)
	os.makedirs(path)
	os.chdir(path)
	for k in range (0, len(array)):
		filename = str(k) + ".png"
		cv2.imwrite(filename, array[k])
		image = Image.open(filename)
		im_width, im_height = image.size
	#change back to parent directory
	os.chdir("../")
	exporting = False
	# use the path to scan the images in the folder we just made
	scan_images(path)

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
				capture_completed.wait()
				timestamp = time.time()
				export_array = im_array
				im_array = []				
				threading.Thread(target=export_photos, args=(export_array, timestamp)).start()
			else:
				# if not taking pictures right now, wait till exporting True
				capture_images = True

def scan_images(path):
	# print os.getcwd()
	# print path
	os.chdir(str(path))
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')

	barcodes = []
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
		        barcodes.append(symbol.data)
		        # get_object_image(symbol.data, barcodes)
		else:
		    print 'did not decode'
	os.chdir("../")
	final_list = select_barcodes(barcodes)
	product_lookup(final_list)


def scan_images_mac(path):
	print os.listdir(path)
	for i in os.listdir(path):
		command = "zbarimg -q " + path + '/' + i
		output = os.system(command)
	found_barcodes = ["682002009", "6820020094"]
	# final_list = select_barcodes(found_barcodes)
	# product_lookup(final_list)

def select_barcodes(barcodes): 
	barcodes_to_lookup = []
	for j in range(0,len(barcodes)):
	    for l in range(j+1,len(barcodes)):
	        if barcodes[j] == barcodes[l]:
	           barcodes_to_lookup.append(barcodes[j])
	return barcodes_to_lookup

def product_lookup(barcodes):
	for i in barcodes:
		if database[i]:
			image = Image.open(database[i])
			image.show()	

cam = initialize_camera()
set_resolution(cam, 1900, 1080)

capture_thread = threading.Thread(target=capture, args=(cam,))
capture_thread.setDaemon(True)
user_input_thread = threading.Thread(target=get_user_input, args=())
user_input_thread.setDaemon(True)
capture_thread.start()
user_input_thread.start()

try:
	while True:
		pass	
except (KeyboardInterrupt, SystemExit):
  print '\n! Received keyboard interrupt, quitting threads.\n'