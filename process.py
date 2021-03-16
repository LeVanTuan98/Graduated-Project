import numpy as np
import cv2
# import imutils
import matplotlib.pyplot as plt

class Process:

    def __init__(self, original_image, blue_HSV=(0, 0, 0), laser_HSV=(0, 0, 0)):
        self.original_image = original_image
        self.index = 0
        # HSV: Hue - Saturate - Value
        self.blueLower = (blue_HSV[0] - 30, blue_HSV[1] - 70, blue_HSV[2] - 70)
        self.blueUpper = (blue_HSV[0] + 30, blue_HSV[1] + 70, blue_HSV[2] + 70)

        self.laserLower = (laser_HSV[0] - 10, laser_HSV[1] - 10, laser_HSV[2] - 10)
        self.laserupper = (255, 255, 255)

    def convert_RGB_to_HSV(self):
        return cv2.cvtColor(self.original_image.copy(), cv2.COLOR_BGR2HSV)

    def extract_frame(self, file_name):
        cap = cv2.VideoCapture(file_name)
        while True:
            # Read a new frame
            ok, frame = cap.read()
            if not ok:
                # Neu khong doc duoc tiep thi out
                break
            else:
                self.index += 1
                self.original_image = frame










