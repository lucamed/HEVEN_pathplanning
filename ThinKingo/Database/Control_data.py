import sys
import os
sys.path.append(os.path.dirname(__file__))

class ControlData:
    def __init__(self):
        self.p_curr = [0, 0]
        self.p_targ = [0, 0]
        self.car_angle = 0
        self.distance = 0
        self.final_speed = 0
        self.final_steer_angle = 0
        self.final_gear = 0x00
        self.final_brake = 0