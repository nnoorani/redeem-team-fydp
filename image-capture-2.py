#import cv
#from opencv.highgui import *

import cv2
import time
from PIL import Image

# approx velocity 150 cm/s
# survey zone 11cm

def initialize_camera():
        cam = cv2.VideoCapture(0)
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



max_x = '1280'
max_y = '960'
cam, x, y = initialize_camera()


res_1 = [1920,2048,1792,1856,2880,1800,2048,1920,2538,2560,1920,2160,2048,2304,2560,2304,2560,2560,2560,3440,2736,2880,2560,2732,2800,3200,3000,3200,3200,3840,3840,4096,5120,4096,5120,5120,5120,6400,6400,7680,7680,8192,8192]
res_2 = [1080,1152,1344,1392,900,1440,1280,1400,1080,1080,1440,1440,1536,1440,1440,1728,1600,1700,1920,1440,1824,1800,2048,2048,2100,1800,2000,2048,2400,2160,2400,2304,2160,3072,2880,3200,4096,4096,4800,4320,4800,4608,8192]

for a in range(0,len(res_1)):
        set_resolution(cam, res_1[a], res_2[a])
        single_cap(cam, str(res_1[a]) + "x" + str(res_2[a]) +".png")


