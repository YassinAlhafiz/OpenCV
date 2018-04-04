# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy
import RPi.GPIO as GPIO

#GPIO Settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.OUT)

#Default Off-Sustain 
GPIO.output(2,False) 

faceCascade = cv2.CascadeClassifier('/home/pi/haarcascade_frontalface_default.xml')
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(1920, 1080))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
         
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
        
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
 
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    if not numpy.any(faces):
        print ("Face not detected: Pedal")#Return Values from the Facial Array
        GPIO.output(2,True)
    else:
        print ("Face dectected: Normal")
        GPIO.output(2,False)
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break