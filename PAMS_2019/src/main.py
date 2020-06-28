import os
import sys
sys.path.append(".")
sys.path.append("C:\\Users\\HEVEN\\darknet\\build\\darknet\\x64")
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from src.Database import Database
from Control.Control import Control
from Path import Path
from Mission import MissionManager, SampleMission, TrafficLightMission, NarrowMission, UturnMission, TargetCarMission, DefaultMission, ParkingMission, CrosswalkMission, DefaultMission2
from YOLO.thread_yolo import YOLO
import time


def main():
    db = Database(gps=False, imu=False)      
    db.start()

    yolo = YOLO(db=db)
    yolo.start()
    
    path = Path(db=db)
    control = Control(db=db, path=path)

    # 미션 매니저 생성
    mission_manager = MissionManager(db=db)

    # 수행할 미션 순서
    mission_manager.mission_keys =\
        ["TrafficLight", "Default2", "Narrow", "U-Turn",
         "Target_Car", "Default", "Parking",
         "CrossWalk"]

    # 시작 미션 할당(일반적인 경우 0번째 미션부터 시작)
    mission_manager.mission_idx = 0
    mission_manager.current_mission_key = mission_manager.mission_keys[mission_manager.mission_idx]

    # 수행할 미션들을 생성
    trafficlight_mission = TrafficLightMission(db=db, control=control, path=path)
    narrow_mission = NarrowMission(db=db, control=control, path=path)
    uturn_mission = UturnMission(db=db, control=control, path=path)
    target_mission = TargetCarMission(db=db, control=control, path=path)
    default_mission = DefaultMission(db=db, control=control, path=path)
    default_mission2 = DefaultMission2(db=db, control=control, path=path)
    parking_mission = ParkingMission(db=db, control=control, path=path)
    crosswalk_mission = CrosswalkMission(db=db, control=control, path=path)
    
    # 미션 매니저에 수행할 미션들을 추가.
    mission_manager.add_mission(key="TrafficLight", mission=trafficlight_mission)
    mission_manager.add_mission(key="Narrow", mission=narrow_mission)
    mission_manager.add_mission(key="U-Turn", mission=uturn_mission)
    mission_manager.add_mission(key="Target_Car", mission=target_mission)
    mission_manager.add_mission(key="Default", mission=default_mission)
    mission_manager.add_mission(key="Default2", mission=default_mission2)
    mission_manager.add_mission(key="Parking", mission=parking_mission)
    mission_manager.add_mission(key="CrossWalk", mission=crosswalk_mission)

    mission_manager.start()
    
    while True:
        if db.flag.system_stop:
            break
        else:
            try:
                print(mission_manager.current_mission_key)
                print(db.mission)
                time.sleep(1)
            except KeyboardInterrupt:
                print("Keyboard Interrupt detected!")
                db.flag.system_stop = True
                break
            
    yolo.join()
    mission_manager.join()
    db.join()

    return 0

if __name__ == "__main__":
    if main() == 0:
        print("\nAutonomous-Car-System terminated successfully!")
    else:
        print("\nThere is something wrong. I recommend you to kill every processes which is related to this program.")
