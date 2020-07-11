import sys
'''sys.path.append("C:\\Users\\HEVEN\\Desktop\\heven 2019\\HEVEN-AutonomousCar-2019\\ThinKingo\\Database")
import Database'''
from SimulatorDatabase import Database
from SimulatorControl import Control
import time
import cv2

def main():
    db = Database(gps=True, lidar=True, cam=False)
    c = Control(db=db)

    db.start()
    c.start()
    file = open('output.txt', 'w')
    while True:
        if db.flag.system_stop:
            break
        else:
            try:
                time.sleep(1)
                pass
            except KeyboardInterrupt:
                #cv2.destroyAllWindows()
                print("Keyboard Interrupt detected!")
                db.flag.system_stop = True
                break

    db.join()
    c.join()
    file.close()
    return 0


if __name__ == "__main__":
    if main() == 0:
        print("\nAutonomous-Car-System terminated successfully!")
    else:
        print("\nThere is something wrong. I recommend you to kill every processes which is related to this program.")
