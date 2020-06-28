import time
import numpy as np

import sys
import os

import math

sys.path.append(os.path.dirname(__file__))

DISTANCE = 500  # 얼마나 더 앞으로 갔을때 차가 중앙으로 오도록 할 것인가? (cm)
                # 크게 할 수록 조향각 변화가 늦어짐. 안정적 주행, 그러나 너무 늦게 조향각 반영될 수 있음.
                # 작게 할 수록 신속한 조향각 변화. 그러나 진동이 심해질 수 있음.

def lane_tracking(target_angle, curr_position):
    # Lane tracking algorithm here

    k1 = 1  # P gain
    k2 = DISTANCE   # Distance parameter

    if -0.2 < curr_position < 0.2 :  # 좀 더 천천히 조향해도 괜찮은 상황
        k2 = 500
    
    elif curr_position > 0.6 or curr_position < -0.6 :  # 신속하게 가운데로 들어와야 함
        k2 = 300

    else:   # 그 중간의 경우 계수는 linear 변화
        k2 = -500*curr_position + 600

    steer_angle = target_angle * k1 + math.atan(-180 * curr_position / k2)* 180 / math.pi

    return steer_angle