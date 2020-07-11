#-*- coding:utf-8 -*-
from Database import Database
from Monitor import Monitor
import time

def main():
    db = Database(lidar=False,cam=False,lidar=False,imu=False)
    db.start()

    monitor = Monitor(db=db)
    monitor.start()

    while True:
        if db.flag.system_stop:
            break
        else:
            try:
                print(db.gps.data)
                time.sleep(1)
            except KeyboardInterrupt:
                print("\nKeyboard Interrupt detected!")
                db.flag.system_stop = True
                break

    db.join()
    monitor.join()

    return 0

if __name__ == "__main__":
    if main() == 0:
        print("\nAutonomous-Car-System terminated successfully!")
    else:
        print("\nThere is something wromg. I recommend you to kill every processes which is related to this program.")
    
