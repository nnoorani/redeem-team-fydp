import cv2
import time

camera = cv2.VideoCapture(0)
fps = 5
period = 1.0 / fps


start = time.time()
i = 0
retval, im = camera.read()

while (time.time() - start) <= 1:
	print (time.time() - start)
	retval, im = camera.read()
	cv2.imshow('file', im)
	cv2.imwrite("webcam_" + str(i) + ".png", im)
	i += 1

del(camera)



# approx velocity 150 cm/s
# survey zone 11cm
# 

