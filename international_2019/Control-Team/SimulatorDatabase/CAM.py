import socket
import cv2
import time
import copy
import sys
import os
sys.path.append(os.path.dirname(__file__))
import numpy as np

from Flag import Flag
class CAM:
    '''
    cam parameter example
    params = {"SOCKET_TYPE": 'JPG',
            "WIDTH": 480, # image width
            "HEIGHT": 300, # image height
            "FOV": 90, # Field of view
            "localIP": "127.0.0.1",
            "localPort": 1232,
            "Block_SIZE": int(65000),
            "X": 0.5, # meter
            "Y": 0,
            "Z": 1,
            "YAW": 0, # deg
            "PITCH": -10,
            "ROLL": 0}
    '''
    def __init__(self, num, name, flag: Flag, params_cam):
        self.__data = None
        self.__name = name
        self.flag = flag
        self.__cam_initializing_success = False
        self.params_cam = params_cam
        
        self.UDP_cam = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        try:
            self.UDP_cam.bind((params_cam["localIP"], params_cam["localPort"]))
            time.sleep(0.5)
            self.__data = self.get_img()
            self.__cam_initializing_success = True
            print("[%s CAM Intializing \tOk  ]" % self.__name)
        except Exception as ex:
            print(ex)
            self.UDP_cam.close()
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
            try:
                if self.flag.cam_stop:
                    time.sleep(0.1)
                else:
                    self.__data = self.get_img()
            except Exception as ex:
                print(ex)
                
        time.sleep(1)
        print("Terminating %s CAM" % self.__name)
        self.UDP_cam.close()

    def get_img(self):
        '''
        receive a camera image
        \n UDPSocket_cam : UDP server socket
        \n params_cam : parameters from cameras 
        '''

        if self.params_cam["SOCKET_TYPE"] == 'JPG':

            # JPG/UDP type

            UnitBlockSize_cam = self.params_cam["Block_SIZE"]
            max_len = np.floor(self.params_cam["WIDTH"]*self.params_cam["HEIGHT"]/UnitBlockSize_cam/2)-1
            
            TotalBuffer = []
            num_block = 0

            while True:

                bytesAddressPair = self.UDP_cam.recvfrom(UnitBlockSize_cam)
                UnitBlock = bytesAddressPair[0]
                
                UnitIdx = np.frombuffer(UnitBlock[3:7], dtype = "int")[0]
                UnitSize = np.frombuffer(UnitBlock[7:11], dtype = "int")[0]
                UnitTail = UnitBlock[-2:]
                UnitBody = np.frombuffer(UnitBlock[11:(11 + UnitSize)], dtype = "uint8")
                
                if num_block == UnitIdx:
                    TotalBuffer.append(UnitBody)
                    num_block += 1
                else:
                    TotalBuffer = []
                    num_block = 0

                if UnitTail==b'EI' and len(TotalBuffer)>max_len:

                    TotalIMG = cv2.imdecode(np.hstack(TotalBuffer), 1)

                    break

        else:

            # RGB/UDP type

            TotalIMG = np.zeros((self.params_cam["HEIGHT"], self.params_cam["WIDTH"], 3), dtype = "uint8")
            img_head = np.zeros(int(self.params_cam["HEIGHT"]/30),)
            UnitBlockSize_cam = int(self.params_cam["WIDTH"]*30*3+8)

            while True:

                bytesAddressPair = self.UDP_cam.recvfrom(UnitBlockSize_cam)
                UnitBlock = bytesAddressPair[0]

                UnitBlock_array = np.frombuffer(UnitBlock, dtype = "uint8")
                
                UnitHead = int(UnitBlock_array[0])
                UnitBody = UnitBlock_array[4:UnitBlockSize_cam-4].reshape(-1, self.params_cam_cam["WIDTH"], 3)
                
                TotalIMG[UnitHead*30:(UnitHead+1)*30,:,:] = UnitBody
                img_head[UnitHead] = 1
                
                if np.mean(img_head)>0.999:

                    break

        return TotalIMG
        
    @property
    def data(self):
        return copy.deepcopy(self.__data)
