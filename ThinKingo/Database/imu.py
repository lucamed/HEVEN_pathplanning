import serial
import time
import sys
import os
sys.path.append(os.path.dirname(__file__))

from Flag import Flag

class Imu:
    def __init__(self, port, baud, flag: Flag):
        self.__data = [0,0,0,0,0,0]
        self.flag = flag
        self.__imu_initializing_success = False

        try:
            self.__serial = serial.Serial(port, baud)
            self.__imu_initializing_success = True
            print("[IMU Intializing \tOk  ]")
        except serial.serialutil.SerialException as e:
            print("[IMU Intializing \tFail] \tCheck your COMPORT: ", e)

    def main(self):
        if self.__imu_initializing_success:
            print("Start IMU \t- Success\n")
            time.sleep(1)
            self.__read_imu()
        else:
            print("Start IMU \t- Fail: \tIMU doesn't initialize succeessfully. Therefore, IMU will not run.")
        print("\t\t\t\t-->\tTerminate IMU")
              
    def __read_imu(self):
        line = list()
        while not self.flag.system_stop: # By stoping system, Reading IMU should be stopped, too.
            if self.flag.imu_stop:
                time.sleep(0.1) # Connection to IMU is Valid. But do not read data from IMU.
            else:
                for c in self.__serial.read():
                    line.append(chr(c))
                    if c == 10:
                        self.__parse_imu(line)
                        line.clear()
        time.sleep(0.1)
        print("Terminating IMU")
        self.__serial.close()


    def __parse_imu(self, data):
        tmp = ''.join(data)
        if data == ['\n']:
            return 0
        if tmp[0] == '*':    
            try:
                tmp = tmp.split('*')[1].split('\r')[0]
                datas = tmp.split(',')
                roll = float(datas[0])
                pitch = float(datas[1])
                yaw = float(datas[2])
                ax = float(datas[3])
                ay = float(datas[4])
                az = float(datas[5])
                self.__data = [roll, pitch, yaw, ax, ay, az]
            except Exception as e:
                print("[IMU Running \tError] \t\tInvalid data is generated by IMU. Check IMU status:", e)
                time.sleep(1)


    def __parse_imu2(self, data):
        tmp = ''.join(data)
        if data == ['\n']:
            return 0
        else:    
            try:
                tmp.replace('\r', '').replace('\n', '')
                datas = tmp.split(',')
                roll = float(datas[1])
                pitch = float(datas[2])
                yaw = float(datas[3])
                self.__data = [roll, pitch, yaw]
            except Exception as e:
                print("[IMU Running \tError] \t\tInvalid data is generated by IMU. Check IMU status:", e)
                time.sleep(1)
            
    
    @property
    def data(self):
        return self.__data

if __name__ == "__main__":
    imu = Imu('COM5', 115200, Flag())
    imu.main()
