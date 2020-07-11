import sys
sys.path.append(".")
sys.path.append("C:\\Users\\HEVEN\\darknet\\build\\darknet\\x64")
from ThinKingo.Database import Database
from ThinKingo.Control import Control1
from ThinKingo.Control import Control2
from ThinKingo.Monitor import Monitor
from ThinKingo.Path_plan import Path_plan
import time
import cv2

def main():
    db = Database(gps=True,lidar=True,cam=True,imu=True)      
    db.start()

    # c = Control1(db=db)
    c = Control2(db=db)
    c.start()

    m = Monitor(db=db)
    m.start()
    
    while True:
        if db.flag.system_stop:
            break
        else:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                print("Keyboard Interrupt detected!")
                db.flag.system_stop = True
                break

    m.join()
    c.join()
    db.join()

    return 0

if __name__ == "__main__":
    if main() == 0:
        print("\nAutonomous-Car-System terminated successfully!")
    else:
        print("\nThere is something wrong. I recommend you to kill every processes which is related to this program.")
