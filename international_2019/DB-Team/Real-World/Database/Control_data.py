import sys
import os
sys.path.append(os.path.dirname(__file__))

class ControlData:
    def __init__(self):
        self.target = [0, 0]
        self.curr_pos = [0, 0]
        self.angle_error = 0
        self.curr_angle = 0