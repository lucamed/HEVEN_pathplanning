from Database import Database
from Recording import Recording
import time

def main():
    db = Database(gps=True,lidar=False,cam=False,imu=True)
    r = Recording(db=db)
         
    db.start()
    r.start()
    while True:
        if db.flag.system_stop:
            break
        else:
            try:
                time.sleep(0.1)
                pass
            except KeyboardInterrupt:
                print("Keyboard Interrupt detected!")
                db.flag.system_stop = True
                break

    r.join()
    db.join()
    
    return 0


if __name__ == "__main__":
    if main() == 0:
        print("\nAutonomous-Car-System terminated successfully!")
    else:
        print("\nThere is something wrong. I recommend you to kill every processes which is related to this program.")