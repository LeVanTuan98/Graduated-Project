import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt

class Process:

    def __init__(self, original_image, laserLower, laserUpper, blueLower, blueUpper):
        self.original_image = original_image
        self.laserLower = laserLower
        self.laserupper = laserUpper
        self.blueLower = blueLower
        self.blueUpper = blueUpper

    def convert_RGB_to_HSV(self):
        return cv2.cvtColor(self.original_image.copy(), cv2.COLOR_BGR2HSV)


