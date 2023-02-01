from cscore import CameraServer
import cv2
import numpy

CameraServer.enableLogging()

camera = CameraServer.startAutomaticCapture()
camera.setResolution(320, 240)

sink = CameraServer.getVideo()

output = CameraServer.putVideo()

while True:
    time, input_img = cvSink.grabFrame(input_img)

    if time == 0:
        continue

