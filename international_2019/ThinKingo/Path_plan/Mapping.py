'''
#################### PATH PLAN TEAM ####################

## ABOUT
- 미션 번호에 따라 lane과 lidar를 적절히 혼합하여 target, map을 반환해주는 코드

## INPUT & OUTPUT
- Input: Mission number, DB
- Output: Path_Planning에 넘겨줄 target, map
#y 20 pixel  =1m  x 60pixel = 1m
'''
import sys
import os
sys.path.append(os.path.dirname(__file__))

from Lane_Detection import Lane_Detection
import cv2
import numpy as np
import math
from Parking import parking
#from Basic import BasicPath


import matplotlib.pyplot as plt
#1m/pixel
x_scale = 37
y_scale = 35
# Input : DB, Mission number 
# Output : target, map
class Mapping:  # 나중에 이 함수에 display 메소드도 추가해야 할듯..?
    def __init__(self, mission_number,database):  # 초기화
        self.__mission_number = mission_number
        self.database = database
        self.Lane_detect = Lane_Detection(poly_order=2)
        self.radius = 5 # 5m to see
        self.map = [(0,0)]
        self.target = (0,0)
        self.obstacle = []

    def update_map(self, left_on = True , right_on = True, lidar_on = True, img = None):
        #img = cv2.imread(self.database.main_cam.data)
        self.Lane_detect.run(img)#self.database.main_cam.data
        ob = [(1000,1000)]

        if left_on:
            left_x = (self.Lane_detect.left.allx)#/37 * 20
            left_y = (600 - self.Lane_detect.left.ally)#/35 * 20
            left = np.polyfit(left_y,left_x,2)
            left_ob = [(np.polyval(left,i), i) for i in range(600)]

        if right_on:
            right_x = (self.Lane_detect.right.allx)#/37 * 20
            right_y = (600 - self.Lane_detect.right.ally)#/35 * 20
            right = np.polyfit(right_y,right_x,2)
            right_ob = [(np.polyval(right,i),i) for i in range(600)]
            
        
        #ob = left_ob + right_ob

        if lidar_on:
            '''lidar = [5645, 5642, 5635, 5643, 5622, 5630, 5643, 5642, 5640, 5658, 5634, 5634, 5657, 5671, 5660, 5667, 5675, 5687, 5703, 5697, 5688, 5702, 5713, 5724, 5730, 5743, 5764, 5775, 5789, 5778, 5797, 5804, 5826, 5835, 5851, 5875, 5871, 5876, 5892, 5907, 5942, 5959, 5976, 6002, 6019, 6025, 6043, 6073, 6098, 6121, 6139, 6184, 6186, 6220, 6237, 6274, 6296, 6324, 6341, 6378, 6409, 6445, 6466, 6507, 6533, 6565, 6594, 6646, 6676, 6709, 6763, 6794, 6831, 6887, 6927, 6959, 7011, 7046, 7107, 7166, 7202, 7261, 7310, 7349, 7422, 7478, 7454, 7378, 7398, 7446, 7515, 7575, 7778, 8001, 8083, 8145, 8232, 8292, 8392, 8472, 8534, 8624, 8725, 8807, 8894, 9004, 9095, 9218, 9312, 9412, 9519, 9634, 9745, 9883, 10005, 10156, 10275, 10429, 10558, 10699, 10860, 11029, 11153, 11332, 11502, 11653, 11833, 12049, 12234, 9900, 9862, 9827, 9772, 9746, 9704, 9683, 9648, 9622, 1000000, 1000000, 12750, 10612, 12203, 11673, 12208, 12306, 12352, 15484, 15436, 15555, 15676, 15754, 15994, 16313, 16923, 22700, 
            22645, 22133, 22106, 7735, 7756, 7736, 7694, 7708, 7719, 7686, 7681, 7697, 1000000, 1000000, 39561, 39528, 39522, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 16534, 15390, 15021, 15051, 15099, 15128, 15044, 14681, 14640, 14609, 16723, 1000000, 1000000, 1000000, 1000000, 18237, 3247, 3235, 3237, 3247, 3312, 3287, 3245, 3223, 3212, 3204, 3236, 3253, 3289, 3334, 3321, 3332, 3326, 3377, 7194, 1000000, 13527, 13484, 13683, 13713, 13737, 13577, 13375, 13195, 13000, 12830, 12649, 12481, 12311, 12156, 12008, 8971, 8847, 5590, 5561, 5520, 5497, 5385, 5714, 5432, 5255, 5296, 5396, 5252, 5012, 5142, 5236, 5393, 4768, 4810, 5495, 5859, 4873, 4681, 5072, 4821, 5117, 4752, 4750, 4330, 4457, 4478, 4672, 4675, 4522, 4492, 4671, 4544, 4440, 4293, 4322, 4510, 4305, 4577, 4537, 4530, 
            4396, 4532, 4546, 4461, 4329, 4373, 4396, 4127, 3638, 4063, 4042, 3931, 3986, 4276, 4507, 4518, 4485, 4566, 4406, 4576, 4188, 4348, 4148, 4254, 4479, 4492, 3999, 3794, 3734, 3531, 3504, 4345, 4437, 4154, 3702, 3672, 3665, 3670, 3828, 3474, 3496, 4086, 3265, 3263, 3510, 3570, 3441, 3276, 3642, 3990, 4095, 4082, 4083, 4044, 3508, 3281, 3291, 3783, 3334, 3380, 3589, 3472, 3442, 3234]
            '''         
            lidar = self.database.lidar.data
            lidar = np.array(lidar)
            lidar[lidar > 15000] = 0

            angle = (np.linspace(0,180,361)/180 * np.pi)
            x = x_scale * np.cos(angle) * lidar/1000 + 400
            y = y_scale * np.sin(angle) * lidar/1000 + 0

            #plt.plot(x,y)
            #plt.show()

            for z in zip(x,y):
                ob.append(z)
        
        self.obstacle += ob

        return self.obstacle



if __name__ == "__main__":
    db = Database()
    db.start()
    Combine(0,db)
    db.join()
