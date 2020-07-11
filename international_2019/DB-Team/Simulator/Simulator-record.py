import time
import cv2
import numpy as np
import copy

from pynput import keyboard
from SimulatorDatabase import Database

recording = False

def on_press(key):
    global recording
    try:
        if key == keyboard.Key.esc:
            recording = False
        elif key.char == 's':
            recording = True
        else:
            print(key)
    except Exception as e:
        if e == AttributeError:
            pass
        else:
            pass

def record():
    db = Database()
    db.start()
    time.sleep(1)
    db.flag.lidar_stop = True
    db.flag.gps_stop = True
    db.flag.platform_stop = True

    global recording
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('outpu.avi',fourcc, 20.0, (640,480))

    while True:
        if db.flag.system_stop:
            break
        else:
            try:
                if recording:
                    sub_img = db.sub_cam.data
                    cv2.imshow('Record', sub_img)
                    out.write(sub_img)
                    cv2.waitKey(1)
                else:
                    cv2.destroyAllWindows()
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                print("Keyboard Interrupt detected!")
                db.flag.system_stop = True
                break

    out.release()
    cv2.destroyAllWindows()

    listener.stop()
    listener.join()
    db.join()

    return 0

if __name__ == "__main__":
    if record() == 0:
        print("\nRecord System terminated successfully!")
    else:
        print("\nThere is something wrong. I recommend you to kill every processes which is related to this program.")
    
