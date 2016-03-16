import cv2
import time
from PIL import Image
import thread
import os
import zbar

im_array = [] # array that will collect all the pictures in real-time
capture_images = False # don't start off taking pictures
exporting = False

database = {
	"6820020094" : "products/chocolate-milk.jpg",
	"06741806" : "products/fanta.jpg",
	"06782900" : "products/coke.jpg",
	"064200150224" : "products/spaghetti.jpg",
	"058496423346" : "products/uncleben.jpg",
	"060383674304": "products/tomatoes.jpg",
	"066721020376" : "products/triscuit.jpg",
	"060410014431" : "products/pretzel.jpg",
	"066721002297" : "products/ritz.jpg",
	"068100058925" : "products/kd.jpg"

}

def initialize_camera():
	# initializes camera using openCV
	#returns the width, height, and camera object 
	cam = cv2.VideoCapture(0)
	cam.set(5, 8)
	if cam.isOpened():
		return cam

def set_resolution(cam, x, y):
	# sets resolution for camera to take pictures with
	cam.set(3,int(x))
	cam.set(4,int(y))

def capture(cam):
	# runs a loop to take pictures, continuously going until KeyboardInterrupt (Ctrl+C)
	global im_array
	while True:
		if capture_images:
			# if we are supposed to be taking pictures right now
			print 'taking pictures'			
			if cam.isOpened():
				retval, im = cam.read()
				im_array.append(im)

def export_photos(array, timestamp):
	global exporting
	# print len(array)
	# print timestamp
	exporting = True
	# takes an array of image files and a timestamp and creates folder using the timestamp, exports to there
	# making the folder and cd into it
	path = str(timestamp)
	os.makedirs(path)
	os.chdir(path)
	for k in range (0, len(array)):
		filename = str(k) + ".png"
		cv2.imwrite(filename, array[k])
	#change back to parent directory
	os.chdir("../")
	exporting = False
	# use the path to scan the images in the folder we just made
	scan_images(path)

def get_user_input():
	global im_array, capture_images, exporting
	# controls whether or not we are taking pictures right now
	while True:
		#always asking for user input to control
		x = raw_input('Press Enter to toggle picture taking')
		if not x:
			#happens when you press Enter
			if capture_images:
				# if already taking pictures, turn it off
				capture_images = False
				timestamp = time.time()
				# print 'previous image array length is %d' % len(im_array)
				export_array = im_array
				im_array = []
				# print 'now it is %d and the image array length is %s' % (len(export_array), len(im_array))
				thread.start_new_thread(export_photos, (export_array, timestamp))
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
		    # print ""
	os.chdir("../")
	final_list = select_barcodes(barcodes)
	product_lookup(final_list)


def scan_images_mac(path):
	print 'hello output'
	print os.listdir(path)
	for i in os.listdir(path):
		command = "zbarimg -q " + path + '/' + i
		output = os.system(command)
	found_barcodes = ["6820020094", "6820020094"]
	final_list = select_barcodes(found_barcodes)
	product_lookup(final_list)

def select_barcodes(barcodes): 
	for j in range(2,len(barcodes)):
	    for l in range(j+1,len(barcodes)):
	        if barcodes[j] == barcodes[l]:
	           return barcodes[j]

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
# set_resolution(cam, 2304, 1536)
set_resolution(cam, 1900, 1080)
thread.start_new_thread(capture, (cam,))
thread.start_new_thread(get_user_input, ())

while True:
	pass	