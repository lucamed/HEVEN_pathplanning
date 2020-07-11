import sys
import os
sys.path.append(os.path.dirname(__file__))
import numpy as np

class Screens:
    def __init__(self):
        self.db = np.zeros((306, 576, 3), np.uint8)
        self.gps = np.zeros((576, 576, 3), np.uint8)
        self.yolo = np.zeros((324, 576, 3), np.uint8)
        self.lane = np.zeros((324, 576, 3), np.uint8)
        self.cluster = np.zeros((324, 576, 3), np.uint8)
        self.platform = np.zeros((648, 576, 3), np.uint8)
        self.target_points = np.zeros((324, 576, 3), np.uint8)
