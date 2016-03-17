import cv2
import time
from PIL import Image, ImageFile
import threading
import os
import zbar
import Queue

ImageFile.LOAD_TRUNCATED_IMAGES = True
symbols_found = {}
barcode_validated = {}
capture_completed = threading.Event()
object_in_system = threading.Event()
q = Queue.Queue()
dict_lock = threading.Lock()

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


def initialize_camera(i):
        # initializes camera using openCV
        # need to pass in an int for the camera we are choosing to initialize and it returns the camera object
        print i
        cam = cv2.VideoCapture(i)
        if cam.isOpened():
                cam.set(5, 8)
                cam.set(3, 1280)
                cam.set(4, 720)
                return cam

def set_resolution(cam, x, y):
        # sets resolution for camera to take pictures with
        cam.set(3,int(x))
        cam.set(4,int(y))

def test_capture(cam, timestamp):
        # runs a loop to take pictures, continuously going until KeyboardInterrupt (Ctrl+C)
        if cam.isOpened():
                retval, im = cam.read()
        return im

def capture(cam, timestamp, prefix):
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
                                threading.Thread(target=export_photos, args=(im,timestamp,prefix, k)).start()
                                capture_completed.set()
                                k += 1

def wait_for_object_to_be_present(): 
        while True: 
                timestamp = time.time()
                im = test_capture(cameras[3], timestamp)
                is_object_present = check_if_object_present(im)
                if is_object_present:

                        object_in_system.clear() #clearing removes the old object from the system so the other camera threads start waiting again
                        q.put(timestamp) #now we are putting the timestamp of the new object into the queue
                        print "qsize is %d" % q.qsize() #should be 1
                        object_in_system.set() #by calling .set(), we are letting the other camreras know that are 
                        #waiting for an object that an object is here (CHECK LINE 69)
                        time.sleep(60)

def start_camera_threads():
        #starting other camera threads
                while True: 
                        # this line allows the cameras to wait for an object when it is not present. 
                        # the function wait_for_an_object_to_be_present() controls this
                        object_in_system.wait()
                        
                        # function will get here only when object_in_system.set() is called
                        if not q.empty():
                                #get the current object timestamp
                                curr_timestamp = q.get()

                                print "qsize is now %d" % q.qsize() #should be 0, calling get removes it from the queue

                                #HERE IS WHERE YOU ADD THE THREADS FOR ADDITIONAL CAMERAS, depending on which one you are using for 
                                # actual detection, and which one is only for checking object presence
                                threading.Thread(target=capture, args=(cameras[1],curr_timestamp, "cam1")).start()
                                print "starting 1"
                                threading.Thread(target=capture, args=(cameras[2],curr_timestamp, "cam2")).start()
                                print "starting 2"
                                threading.Thread(target=capture, args=(cameras[0],curr_timestamp, "cam3")).start()
                                print "starting 3"

def export_photos(im, timestamp, prefix, k):
        # takes an array of image files and a timestamp and creates folder using the timestamp, exports to there
        # making the folder and cd into it
        
        path = str(timestamp)
        if not os.path.isdir(path):
                os.mkdir(path)
        
        filename = prefix + "-" + str(k) + ".png"
        cv2.imwrite(path + '/' + filename, im)
        # use the path to scan the images in the folder we just made
        scan_images(path,filename, timestamp)

def scan_images(path, filename, timestamp):
        global barcode_validated
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        pil = None
        try:
                pil = Image.open(path+ '/' + filename).convert('L')
        except IOError, e:
                print "Error opening file", filename

        if pil:
                width, height = pil.size
                # print width
                # print height
                # raw = pil.tobytes() #for MAC/other version of python
                raw = pil.tostring() #based on python version 2.7.8
                image = zbar.Image(width, height, 'Y800', raw)

                dict_lock.acquire()
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
                                                product_lookup(symbol.data)
                                                break
                                else: 
                                        
                                        symbols_found[timestamp] = symbol.data
                                        
                        else:
                                print "did not decode"
                dict_lock.release()
def check_if_object_present(im):
        #returns whether photo-gate is blocked

        im2 = im[135:145,295:345] # crop image to around the pixels we want to look at
        path = "pixel"
        cv2.imwrite(path + '/' + "crop.png", im2)
        
        threshold = 25  #this is the range that we want the colour to be between (its too high right now, lower this)
        pixels = {}
        object_present = False #usually, an object isn't there
        
        references = [[23,82,118],[15,0,86],[58,27,0]] #this is the colours we EXPECT them to be

        #im[x,y] where x is the row (so going down) and y are columns are going across
        # im[x,y] is the coordinates of where we are checking EACH of the three colours in the flag - NEEDS UPDATING ONCE IN SYSTEM
        # im[x,y] returns the BGR colour at that coordinate
        pixels = [im2[6,6], im2[6,25], im2[6,40]]

        for i in range(0,3):
                for j in range(0,3):
                        #find the colour difference between the pixels we found and the reference
                        # if its less than 25 (threshold), that means the object isnt there and we can still see the flag
                        
                        colour_difference = pixels[i][j] - references[i][j]
                        if abs(colour_difference) >= threshold:
                                object_present = True

        time.sleep(3) #set delays to help with testing
        return True #help with testing - comment out when actually using the photo flag
        # return object_present #- UNCOMMENT WHEN NOT TESTING ANYMORE

def product_lookup(barcode):
        print barcode
        if barcode:
                if database.has_key(barcode):
                        print database[barcode]
                        product_img = cv2.imread(database[barcode]);
                        cv2.imshow('product', product_img)
                        cv2.waitKey(0) #may need to remove this because it may puase the code
                else:
                        print "Image for this barcode does not exist yet"

cameras =  {}
for i in range(0,4):
        cameras[i] = initialize_camera(i)
        print cameras

reference_check_thread = threading.Thread(target=wait_for_object_to_be_present, args=())
reference_check_thread.setDaemon(True)

camera_thread = threading.Thread(target=start_camera_threads, args=())
camera_thread.setDaemon(True)

reference_check_thread.start()
camera_thread.start()

try:
        while True:
                pass    
except (KeyboardInterrupt, SystemExit):
  print '\n! Received keyboard interrupt, quitting threads.\n'
