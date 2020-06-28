from Database import Database
import time
import threading

if __name__ == "__main__":
    db = Database(cam=False, platform=True, gps=False, lidar=False, imu=False)
    db.start()
    '''path = Path(db=db)
    control = Control(db=db, line=path)
    sample = SampleMission(db=db, control=control, path=path)
    mission_manager = MissionManager(db=db)
    mission_manager.add_mission("Sample", sample)'''

    while not db.flag.system_stop:
        db.platform.send_data.steer = -2000
        db.platform.send_data.speed = 80
        db.platform.send_data.gear = 0x00
        db.platform.send_data.brake = 0

        time.sleep(0.1)
        print("Sending")