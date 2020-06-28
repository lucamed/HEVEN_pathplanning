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

        logging_file = list()

        f = open("ThinKingo\\Database\\직선경로.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[1] = float(temp[1])
            temp[3] = float(temp[3])
            m_lad = temp[1] % 100
            d_lad = (temp[1] - m_lad)/100
            temp[1] = (d_lad + m_lad/60)*110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60)*88800

            logging_file.append([float(temp[1]), float(temp[3])])
            
        f.close()

        self.gps_path_test_for_Control = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\K-City 예선전 경로 파일(LLH).txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.split('\t')
            logging_file.append([float(temp[0])*110000, float(temp[1])*88800])
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
            temp[1] = (d_lad + m_lad/60)*110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60)*88800

            logging_file.append([float(temp[1]), float(temp[3])])
            
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
            temp[1] = (d_lad + m_lad/60)*110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60)*88800

            logging_file.append([float(temp[1]), float(temp[3])])
            
        f.close()

        self.static_obs_1_2 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\본선정적1.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[1] = float(temp[1])
            temp[3] = float(temp[3])
            m_lad = temp[1] % 100
            d_lad = (temp[1] - m_lad)/100
            temp[1] = (d_lad + m_lad/60)*110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60)*88800

            logging_file.append([float(temp[1]), float(temp[3])])
            
        f.close()

        self.static_obs_2_1 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\본선정적2.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[1] = float(temp[1])
            temp[3] = float(temp[3])
            m_lad = temp[1] % 100
            d_lad = (temp[1] - m_lad)/100
            temp[1] = (d_lad + m_lad/60)*110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60)*88800

            logging_file.append([float(temp[1]), float(temp[3])])
            
        f.close()

        self.static_obs_2_2 = logging_file

        logging_file = list()

        # 주차
        f = open("ThinKingo\\Database\\주차1.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[1] = float(temp[1])
            temp[3] = float(temp[3])
            m_lad = temp[1] % 100
            d_lad = (temp[1] - m_lad)/100
            temp[1] = (d_lad + m_lad/60)*110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60)*88800

            logging_file.append([float(temp[1]), float(temp[3])])
            
        f.close()

        self.parking1 = logging_file

        logging_file = list()

        f = open("ThinKingo\\Database\\주차2.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[1] = float(temp[1])
            temp[3] = float(temp[3])
            m_lad = temp[1] % 100
            d_lad = (temp[1] - m_lad)/100
            temp[1] = (d_lad + m_lad/60)*110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60)*88800

            logging_file.append([float(temp[1]), float(temp[3])])
            
        f.close()

        self.parking2 = logging_file

        logging_file = list()
        
        f = open("ThinKingo\\Database\\주차3.txt", 'r')
        while True:
            line = f.readline()
            if not line: break
            temp = line.replace('[', '').replace(']', '').split(',')

            temp[1] = float(temp[1])
            temp[3] = float(temp[3])
            m_lad = temp[1] % 100
            d_lad = (temp[1] - m_lad)/100
            temp[1] = (d_lad + m_lad/60)*110000

            m_lon = temp[3] % 100
            d_lon = (temp[3] - m_lon)/100
            temp[3] = (d_lon + m_lon/60)*88800

            logging_file.append([float(temp[1]), float(temp[3])])
            
        f.close()

        self.parking3 = logging_file