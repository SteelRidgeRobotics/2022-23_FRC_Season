from cscore import CameraServer
from conepipeline import ConePipeline
import cv2
import time
import json
import numpy

def main():
    with open("/boot/frc.json") as f:
        config = json.load(f)
    camera = config["cameras"][0]

    CameraServer.enableLogging()

    camera = CameraServer.startAutomaticCapture()
    camera.setResolution(320, 240)

    cvSink = CameraServer.getVideo()

    output = CameraServer.putVideo("Camera 1", 320, 240)

    while True:
        startTime = time.time()
        frame_time, input_img = cvSink.grabFrame(input_img)

        if frame_time == 0:
            continue

        output_img = ConePipeline.process(input_img)

        processingTime = time.time() - startTime
        fps = 1/processingTime
        cv2.putText(output_img, str(round(fps, 1)), (5, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255))

        output.putFrame(output_img)

main()


