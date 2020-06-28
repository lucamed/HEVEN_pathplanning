import os
import sys
import warnings
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from abc import abstractclassmethod, ABCMeta
from src.Database import Database
from Path import Path
from Control.Control import Control
import threading
import time
import cv2
import numpy as np

warnings.simplefilter("always")
 
class Mission(metaclass=ABCMeta):
    def __init__(self, db: Database, control: Control, path: Path):
        self.db = db
        self.control = control
        self.path = path
        self.key = None
    
    @abstractclassmethod
    def main(self): # 미션 수행 함수 구현해야함.
        '''
        while not self.mission_end():
            (params) = self.line.some_func_for_specific_mission()
            self.control.some_func_for_specific_mission(*params)
            time.sleep(0.1)
        '''
        pass
    
    @abstractclassmethod
    def mission_end(self): # 탈출조건 검사 함수 구현해야함.
        '''
        if self.db.system_stop:
            return True
        else:
            return False
        
        탈출 조건 검사
        if 탈출 조건 만족:
            return True
        else:
            return False
        '''
        pass

    def __str__(self):
        if self.key is None:
            return "None"
        else:
            return self.key + " Mission"


class MissionManager:
    def __init__(self, db: Database):
        self.missions = dict()
        self.db = db
        self.mission_keys = list()
        self.mission_idx = None
        self.current_mission_key = None
        self.manager_thread = threading.Thread(target=self.main)

    def add_mission(self, key, mission: Mission):
        if key not in self.mission_keys:
            warnings.warn("The new key %s is not registered.\
                 Therefore, NO mission will be added." % key)
        else:
            mission.key = key
            self.missions[key] =  mission
    
    def main(self):
        while not self.db.flag.system_stop:
            current_mission = self.missions[self.current_mission_key] # 미션 번호를 수신함
            current_mission.main() # 미션 탈출조건이 만족될 때까지 해당 미션 수행
            if not self.db.flag.system_stop: 
                # 정상적으로 미션이 끝났을 때만 다음 미션으로 넘어감.
                self.next_mission()
    
    def next_mission(self):
        if self.mission_idx >= len(self.mission_keys):
            print("All missions are complete. System will stop.")
            self.db.flag.system_stop = True
        else:
            self.mission_idx += 1
            self.current_mission_key = self.mission_keys[self.mission_idx]
    
    def start(self):
        self.manager_thread.start()

    def join(self):
        self.manager_thread.join()


# Example for specific mission class
class SampleMission(Mission):
    def main(self):
        while not self.mission_end():
            self.control.main()
            time.sleep(0.1)
            print(self.mission_end())

    def mission_end(self):
        if self.db.flag.system_stop:
            end = True
        else:
            end = False

        if end:
            return True
        else:
            return False


class TrafficLightMission(Mission):

    def main(self):
        self.control.traffic_light_start_time = time.time()
        while not self.mission_end():
            self.control.traffic_light()
            time.sleep(0.1)

    def mission_end(self):
        if self.db.flag.system_stop:
            end = True
        else:
            end = False
 
        check = self.db.mission == "green"
        elapsed_time = time.time() - self.control.traffic_light_start_time
        time_check = elapsed_time > 60  # 어떤 오류로 인해 20초 동안 출발하지 못할 경우, 탈출

        if end or check or time_check:
            return True
        else:
            return False


class NarrowMission(Mission):
    NARROW_WIDTH = 6500 # 2m
    ENTERING_TO_NARROW_TIME = 15
    def main(self):
        cv2.destroyAllWindows()
        self.start_time = time.time()

        while not self.mission_end():
            max_distance, target_angle, image = self.path.narrow()
            self.control.narrow(max_distance, target_angle)

            cv2.imshow("Obstacle", image)
            cv2.waitKey(1)
            
            time.sleep(0.1)

    
    def mission_end(self):
        if self.db.flag.system_stop:
            end = True
        else:
            end = False

        if (time.time() - self.start_time) > self.ENTERING_TO_NARROW_TIME:
            lidar_ending = self.in_narrow()
        else:
            lidar_ending = False

        if end or lidar_ending:
            cv2.destroyAllWindows()
            return True
        else:
            return False

    def in_narrow(self):
        lidar_data = self.db.lidar.data
        # left_data = lidar_data[0:60]
        right_data = lidar_data[0:60]
        # total_data = np.concatenate((left_data, right_data), axis=None)

        min_distance = np.min(right_data)
        print(min_distance)
        if min_distance > (self.NARROW_WIDTH / 2): # 100cm
            return True
        else:
            return False


class UturnMission(Mission):
    def main(self):
        self.control.uturn_mission_start_time = time.time()
        while not self.mission_end():
            if time.time() - self.control.uturn_mission_start_time < 1:
                self.db.platform.send_data.speed = 50
                self.db.platform.send_data.steer = 1500
                self.db.platform.send_data.gear = 0x00
                self.db.platform.send_data.brake = 0
                
            else:
                self.control.uturn_macro()

            time.sleep(0.1)
            
    def mission_end(self):
        # 유턴 미션이 끝났다는 플래그를 여기에
        if self.db.flag.system_stop:
            end = True
        else:
            end = False

        check = (self.control.uturn_1_left_obstacle_detected) and (self.control.uturn_2_left_obstacle_gone) and (self.db.lidar.data[90] / 10) < 330
        yolo_ending = self.db.mission == "Target_Car"

        if end or check or yolo_ending:
            return True
        else:
            return False
        

class TargetCarMission(Mission):
    def main(self):
        self.control.target_mission_start_time = time.time()
        while not self.mission_end():
            
            self.control.target_car()
            time.sleep(0.1)

    def mission_end(self):
        if self.db.flag.system_stop:
            end = True
        else:
            end = False

        # 타겟차 미션 탈출해야 하는지 검사
        check = (self.control.target_mission_end)

        if end or check:
            cv2.destroyAllWindows()
            return True
        else:
            return False


class DefaultMission(Mission):

    def main(self):
        self.control.default_start_time = time.time()

        while not self.mission_end():
            elapsed_time = time.time() - self.control.default_start_time
            print(elapsed_time)
            if elapsed_time > 4:  # Default 주행은 최대 3초를 넘지 않도록, 바로 주차 미션이 이어지므로
                self.control.default_end = True

            else:
                self.control.main(speed=50) # 차량 정렬

            time.sleep(0.1)

    def mission_end(self):
        if self.db.flag.system_stop:
            end = True
        else:
            end = False

        check = self.control.default_end

        if end or check:
            cv2.destroyAllWindows()
            return True
        else:
            return False

class DefaultMission2(Mission):

    def main(self):
        self.control.default_start_time = time.time()

        while not self.mission_end():
            elapsed_time = time.time() - self.control.default_start_time
            print(elapsed_time)
            if elapsed_time > 16:  # Default 주행은 최대 3초를 넘지 않도록, 바로 주차 미션이 이어지므로
                self.control.default_end = True

            else:
                self.control.main(speed=50, brake=0) # 차량 정렬

            time.sleep(0.1)

    def mission_end(self):
        if self.db.flag.system_stop:
            end = True
        else:
            end = False

        check = self.control.default_end

        if end or check:
            cv2.destroyAllWindows()
            return True
        else:
            return False


class ParkingMission(Mission):
    def main(self):
        #self.parking_start_time = time.time()
        while not self.mission_end():

            '''if time.time() - self.parking_start_time < 1.5:
                self.control.main(speed=60)

            else:
                if self.control.right_sign_distance() < 170:
                    self.control.parking_macro_start_time = time.time()
                    print("주차 매크로 시작")
                    cv2.destroyAllWindows()

                    while not self.mission_end():
                        self.control.parking_macro()
                        time.sleep(0.1)

                else:
                    self.control.main(speed=60)
                    print(self.control.right_sign_distance())

            time.sleep(0.1)'''

            if self.path.parking.check_park_line():
                self.control.parking_macro_start_time = time.time()
                print("주차 매크로 시작")
                cv2.destroyAllWindows()
                
                while not self.mission_end():
                    self.control.parking_macro()
                    time.sleep(0.1)
                    
            else:
                self.control.main(speed=50)

            time.sleep(0.1)

    def mission_end(self):
        if self.db.flag.system_stop:
            end = True
        else:
            end = False

        check = self.control.parking_mission_end

        if end or check:
            return True
        else:
            return False


class CrosswalkMission(Mission):
    def main(self):
        self.crosswalk_start_time = time.time()
        while not self.mission_end():
            
            if time.time() - self.crosswalk_start_time < 2:
                self.control.main(speed=60)
                print(time.time() - self.crosswalk_start_time)
            else:
                #if_stop_line = self.path.line.check_stop_line()
                
                self.control.crosswalk()

            time.sleep(0.1)

    def mission_end(self):
        if self.db.flag.system_stop:
            end = True
        else:
            end = False

        check = self.control.crosswalk_mission_end
        
        if end or check:
            return True
        else:
            return False


if __name__ == "__main__":
    db = Database(gps=False, imu=False)
    db.start()
    
    time.sleep(1)

    path = Path(db=db)
    control = Control(db=db, path=path)
    
    default = DefaultMission(db=db, control=control, path=path)
    narrow = NarrowMission(db=db, control=control, path=path)
    uturn = UturnMission(db=db, control=control, path=path)
    targetcar = TargetCarMission(db=db, control=control, path=path)
    crosswalk = CrosswalkMission(db=db, control=control, path=path)
    parking = ParkingMission(db=db, control=control, path=path)
    sample = SampleMission(db=db, control=control, path=path)
    sample.main()
    #narrow.main()
    #uturn.main()
    #targetcar.main()
    #crosswalk.main()
    #parking.main()