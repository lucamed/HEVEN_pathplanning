import time
import cv2
import numpy as np
import copy
import pickle

def pre_processing(_logging_file):
    temp = (-1, -1)
    processed_logging_file = list()
    for log in _logging_file:
        if temp == log:
            pass
        else:
            temp = log
            processed_logging_file.append(log)

    return processed_logging_file


def player():
    
    logging_file = list()

    f = open("/Users/deinm/Desktop/codeworks/HEVEN-AutonomousCar-2019/DB-Team/Real-World/Database/gps.txt", 'r')
    while True:
        line = f.readline()
        if not line: break
        temp = line.replace('[', '').replace(']', '').split(',')
        logging_file.append([3000 * float(temp[1]), 3000 * float(temp[3])])
    f.close()

    def update(_default_img, _logging_file, _buffer):
        _buffer = _buffer + _logging_file[:1]

        _logging_file = _logging_file[1:]
        try:
            current = _buffer[-1]
        except IndexError:
            print("End of logging file")
            raise KeyboardInterrupt
        update_img = copy.deepcopy(_default_img)
        for i, item in enumerate(_buffer):
            update_img = cv2.circle(update_img, (288 + 10 * int(item[1] - current[1]), 288 - 10 * int(item[0] - current[0])), 2, (int(255 * ((len(_buffer) - i) / len(_buffer))), int(255 * (i / len(_buffer))), 0), 1)
        
        return update_img, _logging_file, _buffer

    default_img = np.zeros((576, 576, 3), np.uint8)
    default_img = cv2.circle(default_img, (288,288), 8, (0,0,255), 1)
    default_img = cv2.circle(default_img, (288,288), 32, (0,0,255), 1)
    default_img = cv2.circle(default_img, (288,288), 72, (0,0,255), 1)
    default_img = cv2.circle(default_img, (288,288), 128, (0,0,255), 1)
    default_img = cv2.circle(default_img, (288,288), 200, (0,0,255), 1)
    default_img = cv2.circle(default_img, (288,288), 288, (0,0,255), 1)

    stop = False
    buffer = list()
    while True:
        if stop:
            break
        else:
            try:
                img, logging_file, buffer = update(default_img, logging_file, buffer)
                cv2.imshow('GPS PLAYING', img)
                cv2.waitKey(50)
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                print("Keyboard Interrupt detected!")
                stop = True
                break

    return 0

if __name__ == "__main__":
    if player() == 0:
        print("\nPlayer System terminated successfully!")
    else:
        print("\nThere is something wromg. I recommend you to kill every processes which is related to this program.")
    
