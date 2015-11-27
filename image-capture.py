import cv2
import time

camera = cv2.VideoCapture(0)
fps = 5
period = 1.0 / fps


start = time.time()
i = 0
retval, im = camera.read()

# for i in range(2):
	# print (time.time() - start)
retval, im = camera.read()
cv2.imshow('file', im)
cv2.imwrite("60cm.png", im)

del(camera)



# approx velocity 150 cm/s
# survey zone 11cm
# 

