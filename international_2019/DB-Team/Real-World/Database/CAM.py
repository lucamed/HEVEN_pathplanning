import time
import copy
import cv2
import sys
import os
sys.path.append(os.path.dirname(__file__))

from Flag import Flag
class CAM:
    def __init__(self, num, name, flag: Flag):
        self.__data = None
        self.__name = name
        self.flag = flag
        self.__cam_initializing_success = False

        self.__capture = cv2.VideoCapture(num, cv2.CAP_DSHOW)
        if self.__capture.read()[0]:    # If cam works well, it return (True, Data)
            self.__cam_initializing_success = True
            print("[%s CAM Intializing \tOk  ]" % self.__name)
        else:
            self.__capture.release()
            print("[%s CAM Intializing \tFail] \tCan not read image from cam successfully. " % self.__name)

    def main(self):
        if self.__cam_initializing_success:
            print("Start %s CAM\t- Success\n" % self.__name)
            time.sleep(1)
            self.__read_cam()
        else:
            print("Start %s CAM\t- Fail:\t\t%s CAM doesn't initialize succeessfully. Therefore, %s CAM will not run." % (self.__name, self.__name, self.__name))
        print("\t\t\t\t-->\tTerminate %s CAM" % self.__name)

    def __read_cam(self):
        while not self.flag.system_stop:
            if self.flag.cam_stop:
                time.sleep(0.1)
            else:
                success, frame = self.__capture.read()
                if success:
                    self.__data = frame
                else:
                    pass
        time.sleep(0.1)
        self.__capture.release()
        print("Terminating %s CAM" % self.__name)


    @property
    def data(self):
        return copy.deepcopy(self.__data)