import threading
import time

from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet
from traffic_hsv import lightsParser

# Parameters
SIZE = 20  # Buffer size (if a class reaches SIZE frames -> do mission)
IDLE_SIZE = 30  # Idle mode size (if no reading for IDLE frames -> reset buffer)
THRESH = 0.6  # YOLO threshold
MAX_SIZE = 50000  # Max area size that can be accepted as a detection   -> fix miss-detection with large bounding box
MIN_SIZE = 400  # Min area size that can be accepted as a detection   -> fix miss-detection with small bounding box and prevents detecting anything on the background
BRT_THRESH = 180


# Correction
brightness = -30
contrast = -20

HEIGHT = 608
WEIGHT = 608
netMain = None
metaMain = None
altNames = None

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (30, 30)
fontScale = 0.6
fontColor = (0, 0, 255)
lineType = 2

class Example():
    def __init__(self, db): # db is optional
        self.db = db
        self.flag = db.flag
        self.example_thread = threading.Thread(target=self.__main)
        self.definer = ['red_light',
                        'arrow_light',
                        'green_light',
                        'traffic_light']  # Define all 14 traffic signs used

        self.separate = ['red_light', 'green_light']

        self.sign = {key: [0, 0] for key in self.definer}  # Initialize a dict for each type to store a counter and precision checker


        # ---*Class*--------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # |   intersection   |   left   |   right   |   workers   |    bike   |   crosswalk   |   school   |   speed_bump   |   parking   |   bus    |   red_light   |   green_light   |
        # ---*Counter*------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # |        0         |     0    |     0     |      0      |     0     |       0       |      0     |        0       |      0      |    0     |       0       |        0        |
        # ---*Precision*----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # |        0         |     0    |     0     |      0      |     0     |       0       |      0     |        0       |      0      |    0     |       0       |        0        |
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # YOLO config
        global metaMain, netMain, altNames
        configPath = "custom_traffic/yolov3-t4.cfg"
        weightPath = "backup/yolov3-t4_best(tl).weights"
        metaPath = "custom_traffic/obj.data"
        if not os.path.exists(configPath):
            raise ValueError("Invalid config path `" + os.path.abspath(configPath) + "`")
        if not os.path.exists(weightPath):
            raise ValueError("Invalid weight path `" + os.path.abspath(weightPath) + "`")
        if not os.path.exists(metaPath):
            raise ValueError("Invalid data file path `" + os.path.abspath(metaPath) + "`")
        if netMain is None:
            netMain = darknet.load_net_custom(configPath.encode("ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
        if metaMain is None:
            metaMain = darknet.load_meta(metaPath.encode("ascii"))
        if altNames is None:
            try:
                with open(metaPath) as metaFH:
                    metaContents = metaFH.read()
                    import re
                    match = re.search("names *= *(.*)$", metaContents, re.IGNORECASE | re.MULTILINE)
                    if match:
                        result = match.group(1)
                    else:
                        result = None
                    try:
                        if os.path.exists(result):
                            with open(result) as namesFH:
                                namesList = namesFH.read().strip().split("\n")
                                altNames = [x.strip() for x in namesList]
                    except TypeError:
                        pass
            except Exception:
                pass

    def convertBack(self, x, y, w, h):
            xmin = int(round(x - (w / 2)))
            xmax = int(round(x + (w / 2)))
            ymin = int(round(y - (h / 2)))
            ymax = int(round(y + (h / 2)))
            return xmin, ymin, xmax, ymax

    def cvDrawBoxes(self, detections, img):
        x1 = x2 = y1 = y2 = 0
        if detections:
            for detection in detections:
                x, y, w, h = detection[2][0], \
                            detection[2][1], \
                            detection[2][2], \
                            detection[2][3]
                xmin, ymin, xmax, ymax = self.convertBack(float(x), float(y), float(w), float(h))
                pt1 = (xmin, ymin)
                pt2 = (xmax, ymax)
                area = (xmax - xmin) * (ymax - ymin)
                print(pt1, pt2)
                if area < MAX_SIZE and area > MIN_SIZE and (xmax - xmin) > (ymax-ymin)*1.8:
                    
                    cv2.rectangle(img, pt1, pt2, (0, 0, 0), 1)
                    cv2.putText(img, detection[0].decode() + " [" + str(round(detection[1] * 100, 2)) + "]",
                                (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 0, 0], 2)
                    x1 = xmin
                    x2 = xmax
                    y1 = ymin
                    y2 = ymax
        return img

    def checkSize(self, detections):
        c = 1
        flag = []
        if detections:
            for detection in detections:
                c = c +  1
                x, y, w, h = detection[2][0], detection[2][1], detection[2][2], detection[2][3]
                xmin, ymin, xmax, ymax = self.convertBack(float(x), float(y), float(w), float(h))
                area = (xmax - xmin) * (ymax - ymin)
                if area >= MAX_SIZE or area <= MIN_SIZE or (xmax - xmin) < (ymax-ymin)*1.8:
                    flag.append(detection)

        detections = [x for x in detections if x not in flag]
        return(detections)
    
    def __main(self):
        # cap = cv2.VideoCapture(1)
        # cap = cv2.VideoCapture('/dev/video2')
        cap = cv2.VideoCapture('0818.mp4')

        cap.set(3, WEIGHT)  # Feed resolution from webcam to YOLO however output is from yolo cfg file resolution
        cap.set(4, HEIGHT)
        out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30.0, (darknet.network_width(netMain), darknet.network_height(netMain)))

        print("Starting the YOLO loop...")

        # Create an image we reuse for each detect
        darknet_image = darknet.make_image(darknet.network_width(netMain), darknet.network_height(netMain), 3)

        # Variables
        frame_count = 0
        mx = frame_show = ''
        self.last_mission = ''
        self.TF_flag = [0, 0, 0]
        while not self.flag.system_stop: # By stoping system, Reading GPS should be stopped, too.
            if self.flag.exmpale_stop:
                time.sleep(0.1)
            else:
                prev_time = time.time()
                ret, frame_read = cap.read()
                hsv = cv2.cvtColor(frame_read, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv)
                mean_brt = np.mean(v)

                #  Brightness Correction
                if mean_brt > BRT_THRESH:
                    frame_read = np.int16(frame_read)
                    frame_read= frame_read * (contrast/127+1) - contrast + brightness
                    frame_read = np.clip(frame_read, 0, 255)
                    frame_read = np.uint8(frame_read)

                frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (darknet.network_width(netMain),darknet.network_height(netMain)), interpolation=cv2.INTER_LINEAR) # CHECK RESIZING KEEPING RATIO

                darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())

                detections = darknet.detect_image(netMain, metaMain, darknet_image, THRESH) # Uses YOLO to detect
                detect = self.checkSize(detections) # Gets rid of improper detections

                fps = (1 / (time.time() - prev_time))


                image = self.cvDrawBoxes(detect, frame_resized)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                if detect:
                    sg1 = detect[0][0].decode()
                    if sg1 == 'traffic_light':
                        x, y, w, h = detect[0][2]

                        x11, y11, x22, y22 =self.convertBack(float(x), float(y), float(w), float(h))
    
                        self.TF_flag = lightsParser(image, x11, x22, y11, y22)
                        if self.TF_flag is None:
                            self.TF_flag = [0, 0, 0]

                        if self.TF_flag[0] == 1:
                            self.sign['red_light'][0] += 1

                        if self.TF_flag[1] == 1:
                            self.sign['arrow_light'][0] += 1

                        if self.TF_flag[2] == 1:
                            self.sign['green_light'][0] += 1

                    mx = max(self.sign, key=lambda key: self.sign[key][0])

                    if self.sign[mx][0]:
                        frame_show = str(self.sign[mx][0])
                    
                    frame_count = 0

                else:
                    frame_count += 1  # In order to know IDLE, count frames without any reading and store in frame_count

                self.check_lights()

                if frame_count > IDLE_SIZE:  # If No detection for the last IDLE_SIZE frames -> refresh all  (used to avoid random uncertain and uncontinuos detections)
                    self.reset_dict(0)
                    mx = 'SEARCHING'
                    frame_show = ''
                    frame_count = 0
                    self.last_mission = 'GREEN'
                    self.TF_flag = [0, 0, 0]

                m_number = self.get_mission_number()


                # DEBUGING: write frame count, last mission, the sign with max count and its count, fps
                cv2.putText(image, str(frame_count), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                cv2.putText(image, self.last_mission, (450, 600), font, fontScale, fontColor, lineType)
                # cv2.putText(image, mx, (400, 570), font, fontScale, fontColor, lineType)
                # cv2.putText(image, frame_show, (550, 570), font, fontScale, fontColor, lineType)
                cv2.putText(image, str(m_number), (10, 370), font, fontScale, fontColor, lineType)
                # cv2.putText(image, self.mission, (10, 400), font, fontScale, fontColor, lineType)
                cv2.putText(image, str(self.TF_flag), (10, 600), font, fontScale, fontColor, lineType)
                cv2.putText(image, 'fps: ' + str(int(fps)), (545, 25), font, 0.5, fontColor, lineType)
                cv2.putText(image, 'brt: ' + str(int(mean_brt)), (540, 45), font, 0.5, fontColor, lineType)
                # cv2.putText(image, 'School: '+ str(self.is_school_zone()), (530, 65), font, 0.5, fontColor, lineType)
                cv2.rectangle(image, (0, 0), (100, 100), (60, 60, 60), 1)
                cv2.rectangle(image, (0, 0), (223, 223), (60, 60, 60), 1)

                out.write(image)
                cv2.imshow('Output', image)
                cv2.waitKey(3)

    def reset_dict(self, flag):
            # turn = ''
            if flag == 0:
                self.sign = {key: [0, 0] for key in self.definer}
            else:
                for i in self.separate:
                    self.sign[i] = [0, 0]
            frame_count = 0


    def check_lights(self):
        if self.sign['red_light'][0] > SIZE:  # *Car to-do*: Reset the buffer (not left and right), find the line and stop. **add better implementation
            if self.sign['arrow_light'][0] > SIZE :
                self.last_mission = 'arrow'
                self.reset_dict(0)
            else:
                self.last_mission = 'red'
                self.reset_dict(1)

        elif self.sign['green_light'][0] > SIZE:  # *Car to-do*: Green lights - MOVE
            self.last_mission = 'green'
            self.reset_dict(0)
        return (self.last_mission)


    def start(self):
        self.example_thread.start()

    def join(self):
        self.example_thread.join()
