import cv2
import time
import numpy as np

# Start default camera
video = cv2.VideoCapture(0);

video.set(3,2048)
video.set(4,1152)
       
fps = video.get(cv2.CAP_PROP_FPS)
         
# Number of frames to capture
num_frames = 30;
         
print "Capturing {0} frames".format(num_frames)
     
# Start time
start = time.time()

picarray = []

# Grab a few frames
for i in xrange(0, num_frames) :
    ret, frame = video.read()
    picarray.append(frame)
     
         
# End time
end = time.time()
     
# Time elapsed
seconds = end - start
print "Time taken : {0} seconds".format(seconds)
     
# Calculate frames per second
fps  = num_frames / seconds;
print "Estimated frames per second : {0}".format(fps);

counter = 0

for i in picarray:
    cv2.imwrite(str(counter) + ".png", i)
    counter = counter+1

# Release video
video.release()
