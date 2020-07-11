import socket
import time
import copy
import sys
import os
import struct
import select
sys.path.append(os.path.dirname(__file__))

from Flag import Flag

class LiDAR:
    def __init__(self, host, port, flag: Flag):
        self.__data = None
        self.flag = flag
        self.__lidar_initializing_success = False
        self.info = dict()

        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.__socket.bind((host, port))
            self.__lidar_initializing_success = True
            print("[LiDAR Intializing \tOk  ]")
        except Exception as e:
            print("[LiDAR Intializing \tFail] \tError occurred while opening the socket:", e)

    def main(self):
        if self.__lidar_initializing_success:
            print("Start LiDAR\t- Success\n")
            time.sleep(1)
            self.__read_lidar()
        else:
            print("Start LiDAR\t- Fail:\t\tLiDAR doesn't initialize succeessfully. Therefore, LiDAR will not run.")
        print("\t\t\t\t-->\tTerminate LiDAR")

    def __read_lidar(self):
        while not self.flag.system_stop:
            if self.flag.lidar_stop:
                time.sleep(0.1)
            else:
                try:

                    ready_socks, _, _ = select.select([self.__socket], [], [], 0.0)
                    for sock in ready_socks:
                        bytes_data, addr = sock.recvfrom(65536)
                        self.decode_from_bytes(bytes_data)
                
                except Exception as e:
                    print("[LiDAR Running \tError] \t Error occured while parsing data from LiDAR:", e)

        time.sleep(0.1)
        print("Terminating LiDAR")
        self.__socket.close()
    
    def decode_from_bytes(self, data):
        len_header_and_tail = 5
        len_info = 4 * 7  # INFO는 4종류
        len_data = 3 * 361
        len_total = len_header_and_tail + len_info + len_data

        assert len(data) == len_total, \
            '[ERROR] cannot parse this data. Data length must be equal to {}. Data length = {}, Data passed = {}'.format(\
        len_total, len(data), data)

        format_string_data_part = ''
        for i in range(0, 361):
            format_string_data_part += 'HB'
            # unsigned short Distance
            # unsigned char Intensity

        format_string = '<ccc' + 'fffffII' + format_string_data_part + 'cc' # AI
        data_unpacked = struct.unpack(format_string, data)

        assert data_unpacked[0] == b'M', \
            '[ERROR] Error in the header, it must be M, but the value is = {}'.format(data_unpacked[0])
        assert data_unpacked[1] == b'O', \
            '[ERROR] Error in the header, it must be O, but the value is = {}'.format(data_unpacked[1])
        assert data_unpacked[2] == b'R', \
            '[ERROR] Error in the header, it must be R, but the value is = {}'.format(data_unpacked[2])
        assert data_unpacked[-2] == b'A', \
            '[ERROR] Error in the header, it must be A, but the value is = {}'.format(data_unpacked[-2])
        assert data_unpacked[-1] == b'I', \
            '[ERROR] Error in the header, it must be I, but the value is = {}'.format(data_unpacked[-1])

        # INFO
        self.info = dict()
        self.info['angular_resolution'] = data_unpacked[3]
        self.info['detection_range_min'] = data_unpacked[4]
        self.info['detection_range_max'] = data_unpacked[5]
        self.info['start_angle'] = data_unpacked[6]
        self.info['end_angle'] = data_unpacked[7]
        self.info['num_ray'] = data_unpacked[8]
        self.info['timestamp_ms'] = data_unpacked[9]

        assert 361 == self.info['num_ray'], \
            '[ERROR] cannot parse this data. num_data is set as {}, but the packet received says it has {} number of data'.format(361, self.info['num_ray'])

        i = 10
        self.__data = list()
        for k in range(0, 361):
            self.__data.append(data_unpacked[i])
            i += 2


    @property
    def data(self):
        return copy.deepcopy(self.__data)