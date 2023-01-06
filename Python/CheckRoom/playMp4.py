##import cv2

##cap = cv2.VideoCapture("VID.mp4")
##ret, frame = cap.read()
##while(1):
##   ret, frame = cap.read()
##   cv2.imshow('frame',frame)
##   if cv2.waitKey(1) & 0xFF == ord('q') or ret==False :
##       cap.release()
##       cv2.destroyAllWindows()
##       break
##   cv2.imshow('frame',frame)
from os import startfile
import time
startfile("VID.mp4")

time.sleep(10)
startfile("VID.mp4")
