#import cv
#from opencv.highgui import *

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
                # exposure = cam.get(CV_CAP_PROP_EXPOSURE)

                #print 'width is %d' % width
                #print 'height is %d' % height
                # print 'exposure time is %d' % exposure
                return cam, width, height
        else:
                return False

def loop_capture(): 
        start = time.time()
        i = 0
        retval, im = camera.read()

        while (time.time() - start) < 1:
                print (time.time() - start)
                retval, im = camera.read()
                cv2.imshow('file', im)
                cv2.imwrite(str(i) + ".png", im)
                i += 1

        del(camera)

def get_image(cam):
        retval, im = cam.read()
        return im

def single_cap(cam, filename): 
        if cam.isOpened():
                camera_capture = get_image(cam)
                #cv2.imshow('image', camera_capture)
                cv2.imwrite(filename, camera_capture)
                image = Image.open(filename)
                im_width, im_height = image.size
                #print 'captured image width is %d, height is %s' % (im_width, im_height)

        else:
                print 'not initialized camera'

def set_resolution(cam, x,y):
        #cvSetCaptureProperty(cam, CV_CAP_PROP_FRAME_WIDTH, int(x))
        #cvSetCaptureProperty(cam, CV_CAP_PROP_FRAME_HEIGHT, int(y))
        cam.set(3,int(x))
        cam.set(4,int(y))

#!/usr/bin/python
from sys import argv
import zbar
from PIL import Image

def process (theimage): 
    # create a reader
    scanner = zbar.ImageScanner()

    # configure the reader
    scanner.parse_config('enable')

    # obtain image data
    pil = Image.open(theimage).convert('L')
    width, height = pil.size
    raw = pil.tostring()

    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image for barcodes

    if scanner.scan(image):
    # extract results
        for symbol in image:
        # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
    else:
        print 'did not decode'

    # clean up
    del(image)


cam, x, y = initialize_camera()
set_resolution(cam, 2304,1536)


# (2304,1536)
path = ''
for k in range(0,15):
    path = str(k)+ ".png"
    single_cap(cam, path)
    print path
    process(path)
    


