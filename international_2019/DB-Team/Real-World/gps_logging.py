import time
import cv2
import numpy as np
import copy
import pickle
from pynput import keyboard

from Database import Database

recording = False

def on_press(key):
    global recording
    try:
        if key == keyboard.Key.esc:
            recording =False
        elif key.char == 's':
            recording = True
        else:
            print(key)
    except Exception as e:
        if e == AttributeError:
            pass
        else:
            pass


def logging():
    db = Database()
    db.start()
    db.flag.lidar_stop = True
    db.flag.cam_stop = True
    db.flag.platform_stop = True

    real_world_logging_data = []

    def update(_default_img, _buffer):
        input_data = [db.gps.data[1], db.gps.data[3]]
        real_world_logging_data.append(input_data)
        
        _buffer.append(input_data)
        if len(_buffer) > 10:
            _buffer.pop()

        current = _buffer[-1]
        update_img = copy.deepcopy(_default_img)
        for i, item in enumerate(_buffer):
            update_img = cv2.circle(update_img,
                                    (288 + 10 * int(item[1] - current[1]), 288 - 10 * int(item[0] - current[0])), 2,
                                    (int(255 * ((len(_buffer) - i) / len(_buffer))), int(255 * (i / len(_buffer))), 0),
                                    1)

        return update_img, _buffer

    default_img = np.zeros((576, 576, 3), np.uint8)
    default_img = cv2.circle(default_img, (288, 288), 8, (0, 0, 255), 1)
    default_img = cv2.circle(default_img, (288, 288), 32, (0, 0, 255), 1)
    default_img = cv2.circle(default_img, (288, 288), 72, (0, 0, 255), 1)
    default_img = cv2.circle(default_img, (288, 288), 128, (0, 0, 255), 1)
    default_img = cv2.circle(default_img, (288, 288), 200, (0, 0, 255), 1)
    default_img = cv2.circle(default_img, (288, 288), 288, (0, 0, 255), 1)

    buffer = list()

    global recording
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while True:
        if db.flag.system_stop:
            with open('real_world_logging_data.pickle', 'wb') as f:
                pickle.dump(real_world_logging_data, f)
            break
        else:
            try:
                if recording:
                    img, buffer = update(default_img, buffer)
                    cv2.imshow('GPS LOGGING', img)
                    cv2.waitKey(1)
                else:
                    cv2.destroyAllWindows()

            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                print("Keyboard Interrupt detected!")
                
                with open('real_world_logging_data.pickle', 'wb') as f:
                    pickle.dump(real_world_logging_data, f)
                    
                db.flag.system_stop = True
                break

    listener.stop()
    listener.join()
    db.join()

    return 0


if __name__ == "__main__":
    if logging() == 0:
        print("\nLogging System terminated successfully!")
    else:
        print("\nThere is something wromg. I recommend you to kill every processes which is related to this program.")