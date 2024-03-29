
from websocket_server import WebsocketServer
import json
import cv2
import time
from PIL import Image, ImageFile
import threading
import os
import zbar
import Queue
import json

ImageFile.LOAD_TRUNCATED_IMAGES = True
symbols_found = {}
barcode_validated = {}
capture_completed = threading.Event()
object_in_system = threading.Event()
q = Queue.Queue()
dict_lock = threading.Lock()
server_started = False
field_was_emptied = True #usually, an object isn't there
object_blocking = False
ready = True

database = {
        "6820020094" : {"name": "Chocolate Milk", "img-url": "products/chocolate-milk.jpg", "price": 2.99},
        "06741806" : {"name": "Fanta", "img-url": "products/triscuit.jpg", "price": 0.99},
        "06782900" : {"name": "Coca-Cola", "img-url": "products/coke.jpg", "price": 0.99},
        "064200150224" : {"name":"Spaghetti", "img-url": "products/spaghetti.jpg", "price":2.99},
        "058496423346" : {"name":"Uncle Ben's Rice", "img-url": "products/uncleben.jpg", "price" : 4.99},
        "066721003140" : {"name": "Triscuit", "img-url": "products/triscuit.jpg", "price":1},
        "060410014431" : {"name" : "Pretzels", "img-url" : "products/pretzel.jpg", "price": 3.99},
        "066721002297" : {"name": "Ritz Crackers", "img-url":"products/ritz.jpg", "price":1},
        "068100058925" : {"name": "Kraft Dinner", "img-url": "products/kd.jpg", "price": 1.99},
        "066721002594" : {"name": "Kraft Dinner", "img-url": "products/triscuit.jpg", "price": 1.99},
        "Not Found" : {"name": "Item Not Found", "img-url":"product/default.png", "price": 0.00}
}

def initialize_camera(i):
        # initializes camera using openCV
        # need to pass in an int for the camera we are choosing to initialize and it returns the camera object
        print i
       
        cam = cv2.VideoCapture(i)
        if cam.isOpened():
                cam.set(5, 8)
                cam.set(3, 5168) #1280
                cam.set(4, 2907) #720
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
        time_elapsed = 0
        while True and (time_elapsed < 5):
                curr_time = time.time()
                time_elapsed = abs(timestamp - curr_time)
                #print "the time elapsed is %s" % time_elapsed
                if not timestamp in barcode_validated.keys():
                        if cam.isOpened():
                                capture_completed.clear()
                                retval, im = cam.read()
                                threading.Thread(target=export_photos, args=(im,timestamp,prefix, k)).start()
                                capture_completed.set()
                                k += 1
                                time.sleep(0.5)
        if time_elapsed > 10:
            left_message = json.dumps({"objectLeft":True})
            server.send_message_to_all(left_message)

def wait_for_object_to_be_present(): 
        while True:
                #time.sleep(3)
                timestamp = time.time()
                im = test_capture(cameras[4], timestamp)
                is_object_present = check_if_object_present(im)
                #print is_object_present
                if is_object_present:
                        entered_message = json.dumps({"objectEntered":True})
                        server.send_message_to_all(entered_message)
                        object_in_system.clear() #clearing removes the old object from the system so the other camera threads start waiting again
                        q.put(timestamp) #now we are putting the timestamp of the new object into the queue
                        #print "qsize is %d" % q.qsize() #should be 1
                        print "NEW OBJECT COMING IN"
                        object_in_system.set() #by calling .set(), we are letting the other camreras know that are 
                        #waiting for an object that an object is here (CHECK LINE 69)
                        

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
                                #print "qsize is now %d" % q.qsize() #should be 0, calling get removes it from the queue

                                #HERE IS WHERE YOU ADD THE THREADS FOR ADDITIONAL CAMERAS, depending on which one you are using for 
                                # actual detection, and which one is only for checking object presence
                                #print "starting 1"
                                t1 = threading.Thread(target=capture, args=(cameras[2],curr_timestamp, "cam1"))
                                t1.start()
                                t1.join(1)

                                #print "the 1st thread is alive %s" % t1.isAlive()
                                #print "starting 2"
                                t2 = threading.Thread(target=capture, args=(cameras[3],curr_timestamp, "cam2"))
                                t2.start()
                                t2.join(1)

                                #print "the 2nd thread is alive %s" % t2.isAlive()
                                #print "starting 3"
                                t3 = threading.Thread(target=capture, args=(cameras[0],curr_timestamp, "cam3"))
                                t3.start()
                                t3.join(1)

                                #print "the 3rd thread is alive %s" % t3.isAlive()

                                #print "num threads alive is %s" % threading.enumerate()


def export_photos(im, timestamp, prefix, k):
        # takes an array of image files and a timestamp and creates folder using the timestamp, exports to there
        # making the folder and cd into it
        
        path = str(timestamp)
        if not os.path.isdir(path):
                os.mkdir(path)
        
        filename = prefix + "-" + str(k) + ".png"
        cv2.imwrite(path + '/' + filename, im)
        # use the path to scan the images in the folder we just made
        scan_images(path,filename, timestamp, prefix)

def scan_images(path, filename, timestamp, prefix):
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
                                                handle_product_lookup(symbol.data)
                                                break
                                else: 
                                        symbols_found[timestamp] = symbol.data
                        else:
                                time_elapsed = time.time() - timestamp
                                print "did not decode from %s after %d" % (prefix, time_elapsed)
                dict_lock.release()

def check_if_object_present(im):
        global ready
        #returns whether photo-gate is blocked
        #print ready
        im2 = im[405:425,595:690] # crop image to around the pixels we want to look at
        path = "pixel"
        cv2.imwrite(path + '/' + "im.png", im)
        cv2.imwrite(path + '/' + "crop.png", im2)
        object_blocking = False
        
        threshold = 50  #this is the range that we want the colour to be between (its too high right now, lower this)
        pixels = {}
        references = [[200,140,90],[120,100,185],[120,190,200]] #this is the colours we EXPECT them to be

        #im[x,y] where x is the row (so going down) and y are columns are going across
        # im[x,y] is the coordinates of where we are checking EACH of the three colours in the flag - NEEDS UPDATING ONCE IN SYSTEM
        # im[x,y] returns the BGR colour at that coordinate
        pixels = [im2[10,15], im2[10,50], im2[10,85]]

        for i in range(0,3):
                for j in range(0,3):
                        #find the colour difference between the pixels we found and the reference
                        # if its less than 25 (threshold), that means the object isnt there and we can still see the flag
                        
                        colour_difference = pixels[i][j] - references[i][j]
                        if abs(colour_difference) >= threshold:
                                object_blocking = True

        if object_blocking:
                #print "object is blocking"
                if ready:
                        #print "this object is new"
                        ready = False
                        returnn =  True
                else:
                        returnn = False
                        
        else:
                #print "i should not be called"
                ready = True
                returnn = False

        return returnn
        #time.sleep(10)
        #return True

def construct_product_data(barcode):
    return database[barcode]


def handle_product_lookup(barcode):
    data = construct_barcode_data(barcode)
    data_in_json = json.dumps(data)
    print data_in_json
    server.send_message_to_all(data_in_json)

def construct_barcode_data(barcode):
    if not database.has_key(barcode):
        add_barcode_to_database(barcode)

    return database[barcode]

def add_barcode_to_database(barcode):
    database[barcode] = {"name": "None", "img-url": "products/default.png", "price": "3.99"}

cameras =  {}
for i in range(0,5):
        cameras[i] = initialize_camera(i)
        print cameras

reference_check_thread = threading.Thread(target=wait_for_object_to_be_present, args=())
reference_check_thread.setDaemon(True)

camera_thread = threading.Thread(target=start_camera_threads, args=())
camera_thread.setDaemon(True)

reference_check_thread.start()
camera_thread.start()

def new_client(client, server):
    print "helllooooo"

server = WebsocketServer(5000)
server.set_fn_new_client(new_client)
server.run_forever()

try:
        while True:
                pass    
except (KeyboardInterrupt, SystemExit):
  print '\n! Received keyboard interrupt, quitting threads.\n'
