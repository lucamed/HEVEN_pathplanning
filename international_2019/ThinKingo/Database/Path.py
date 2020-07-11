import utm

class Path:
    def __init__(self):
        logging_file = list()

        f = open("ThinKingo\\Database\\gps.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')
            logging_file.append([3000 * float(temp[1]), 3000 * float(temp[3])])
        f.close()

        self.gps_pre_path = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\gps2.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')
            logging_file.append([3000 * float(temp[1]), 3000 * float(temp[3])])
        f.close()

        self.gps_main_path = logging_file
        self.generate_path = None
        
        # *************************************************************************************
        # For controling test
        
        logging_file = list()

        f = open("ThinKingo\\Database\\tracktest2.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[1] = float(temp[1])
            temp[3] = float(temp[3])

            m_lad = temp[1] % 100
            d_lad = (temp[1] - m_lad)/100
            temp[1] = (d_lad + m_lad/60) * 110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60) * 88800

            logging_file.append([temp[1], temp[3]])
            
        f.close()

        self.gps_path_test_for_Control = logging_file

        # **************************************************************************************
        logging_file = list()

        f = open("ThinKingo\\Database\\K-City 예선전 경로 파일(LLH).txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.split('\t')
            logging_file.append([float(temp[0])*110000, float(temp[1])*88800])
            #utm_data = utm.from_latlon(float(temp[0]), float(temp[1]), 52, "S")
            #logging_file.append(utm_data)
        f.close()

        self.gps_1_track = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\K-City 본선전 경로 파일(LLH).txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.split('\t')
            logging_file.append([float(temp[0])*110000, float(temp[1])*88800])
        f.close()
        
        self.gps_2_track = logging_file
        # **************************************************************************************

        # 정적 장애물
        logging_file = list()

        f = open("ThinKingo\\Database\\예선정적1.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[1] = float(temp[1])
            temp[3] = float(temp[3])

            m_lad = temp[1] % 100
            d_lad = (temp[1] - m_lad)/100
            temp[1] = (d_lad + m_lad/60) * 110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60) * 88800

            logging_file.append([temp[1], temp[3]])

        f.close()

        self.static_obs_1_1 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\예선정적2.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[1] = float(temp[1])
            temp[3] = float(temp[3])

            m_lad = temp[1] % 100
            d_lad = (temp[1] - m_lad)/100
            temp[1] = (d_lad + m_lad/60) * 110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60) * 88800

            logging_file.append([temp[1], temp[3]])

        f.close()

        self.static_obs_1_2 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\static_obstacle1.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[2] = float(temp[2])
            temp[3] = float(temp[3])

            m_lad = temp[2] % 100
            d_lad = (temp[2] - m_lad)/100
            temp[2] = (d_lad + m_lad/60) * 110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60) * 88800

            logging_file.append([temp[2], temp[3]])
            
        f.close()

        self.static_obs_2_1 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\static_obstacle2.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[2] = float(temp[2])
            temp[3] = float(temp[3])

            m_lad = temp[2] % 100
            d_lad = (temp[2] - m_lad)/100
            temp[2] = (d_lad + m_lad/60) * 110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60) * 88800

            logging_file.append([temp[2], temp[3]])

        f.close()

        self.static_obs_2_2 = logging_file

        # 주차
        logging_file = list()

        f = open("ThinKingo\\Database\\parking1.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.split(',')

            temp[0] = float(temp[0]) * 110000
            temp[1] = float(temp[1]) * 88800

            logging_file.append([temp[0], temp[1]])

        f.close()

        self.park_1 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\parking2.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.split(',')

            temp[0] = float(temp[0]) * 110000
            temp[1] = float(temp[1]) * 88800

            logging_file.append([temp[0], temp[1]])

        f.close()

        self.park_2 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\parking3.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.split(',')

            temp[0] = float(temp[0]) * 110000
            temp[1] = float(temp[1]) * 88800

            logging_file.append([temp[0], temp[1]])

        f.close()

        self.park_3 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\parking4.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.split(',')

            temp[0] = float(temp[0]) * 110000
            temp[1] = float(temp[1]) * 88800

            logging_file.append([temp[0], temp[1]])

        f.close()

        self.park_4 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\parking5.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.split(',')

            temp[0] = float(temp[0]) * 110000
            temp[1] = float(temp[1]) * 88800

            logging_file.append([temp[0], temp[1]])

        f.close()

        self.park_5 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\parking6.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.split(',')

            temp[0] = float(temp[0]) * 110000
            temp[1] = float(temp[1]) * 88800

            logging_file.append([temp[0], temp[1]])

        f.close()

        self.park_6 = logging_file