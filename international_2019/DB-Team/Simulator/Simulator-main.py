from SimulatorDatabase import Database
from SimulatorMonitor import Monitor
import time
import cv2


def main():
    db = Database(gps = False, cam=False, lidar=False)
    db.start()

    # monitor = Monitor(db)

    while True:
        if db.flag.system_stop:
            break
        else:
            try:
                # monitor_img = monitor.img
                # cv2.imshow("Monitor", monitor_img)
                # cv2.waitKey(1)
                time.sleep(1)
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                print("Keyboard Interrupt detected!")
                db.flag.system_stop = True
                break

    db.join()

    return 0

if __name__ == "__main__":
    if main() == 0:
        print("\nAutonomous-Car-System terminated successfully!")
    else:
        print("\nThere is something wrong. I recommend you to kill every processes which is related to this program.")
    
