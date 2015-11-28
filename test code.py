import cv2
import time
from PIL import Image

camera_port = 0
cam = cv2.VideoCapture(camera_port)
width = cam.get(3)
height = cam.get(4)
print 'width is %d' % width
print 'height is %d' % height
retval, im = cam.read()
file = "C:/Users/Yannick/Documents/Test/test_image.png"
cv2.imwrite(file, im)
