import cv2
import numpy as np

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def render(self, data):
        return cv2.resize(data, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
