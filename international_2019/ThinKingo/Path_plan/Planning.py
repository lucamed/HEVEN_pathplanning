'''
#################### PATH PLAN TEAM ####################

## ABOUT
- target point에 따른 path를 반환해주는 코드.

## INPUT & OUTPUT
- Input: Combine에서 받은 target, map
- Output: 제어에 넘길 Path
'''

from Mapping import Mapping
from hybrid_astar.hybrid_a_star import HybridAStar
from hybrid_astar.car import Car
from hybrid_astar.mapinfo import MapInfo
import numpy as np

import matplotlib.pyplot as plt

#세로 35pixel
#가로 37pixel

class Planning:  # Mission으로부터 mission number를 받아 그에 맞는 제어에 넘겨줄 list를 반환해줌.
    def __init__(self, mission_number,db,image):  # 초기화
        self.db = db
        self.mapping = Mapping(mission_number,self.db)
        self.radius = 100
        self.vehicle = Car(60,20)
        self.__local_target = self.mapping.target
        self.__map = MapInfo(800, 600 , distance = 15)
        self.__path = [(0,0,0)]
        self.img = image
    def make_path(self, goal, left = True, right = True, lidar = True):         
            start = (400,20,np.pi/2)#self.database.imu.data[2]
            #end = (400,450,np.pi/2)#self.__local_target
            self.__map.start = start
            self.__map.end = goal

            self.__map.obstacle = self.mapping.update_map(left_on = left ,right_on = right, lidar_on = lidar, img = self.img)
            
            self.vehicle.set_position([start[0],start[1],start[2]])
            #vehicle.show()
            plan = HybridAStar(self.__map.start, self.__map.end, self.__map, self.vehicle, r= self.radius, r_step = 20, grid_step=20)

            if plan.run(False):
                xs,ys,yaws = plan.reconstruct_path()
                path = []
                
                #plt.scatter(xs,ys)
                #self.vehicle.show()
                #plt.show()


                gx,gy = float(self.db.gps.data[1]), float(self.db.gps.data[3])
                theta = float(self.db.imu.data[2] + 180) / 180 * np.pi
                
                gx = gx // 100 + (gx % 100)/60
                gy = gy // 100 + (gy % 100)/60

                gx *= 110000
                gy *= 88800

                xs = (np.array(xs)-400)/37
                ys = np.array(ys)/35

                x = np.cos(theta) * xs - np.sin(theta) * ys + gx
                y = np.sin(theta) * xs + np.cos(theta) * ys + gy
            
                for cord in zip(x,y):
                    path.append(cord)
            
            print(path)
            self.__path = path

    @property
    def path(self):
        return self.__path
     
if __name__ == "__main__":
    #db = Database()
    #db.start()

    Path = Planning(0,1)
    #Path.make_path()
    p = Path.path
    #db.path.generate_path = p
    

#    db.join()
