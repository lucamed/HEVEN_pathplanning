
from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import sys
sys.path.append("C:\\Users\\HEVEN\\darknet\\build\\darknet\\x64")
import darknet


# Parameters
SIZE = 10  # Buffer size (if a class reaches SIZE frames -> do mission)
IDLE_SIZE = 20  # Idle mode size (if no reading for IDLE frames -> reset buffer)
THRESH = 0.4  # YOLO threshold
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


class YOLO():
    def __init__(self):
        self.definer = ['u-turn',
                        'crosswalk',
                        'narrow',
                        'tracking',
                        'parking',
                        'red',
                        'green']  # Define all traffic signs used



        self.sign = {key: [0, 0] for key in self.definer}  # Initialize a dict for each type to store a counter and precision checker


        # YOLO config
        global metaMain, netMain, altNames
        configPath = "C:\\Users\\HEVEN\\darknet\\build\\darknet\\x64\\needed_files\\pams19\\yolov3.cfg"
        weightPath = "C:\\Users\\HEVEN\\darknet\\build\\darknet\\x64\\needed_files\\pams19\\yolov3_last.weights"
        metaPath = "C:\\Users\\HEVEN\\darknet\\build\\darknet\\x64\\needed_files\\pams19\\obj.data"
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
        for detection in detections:
            x, y, w, h = detection[2][0], \
                         detection[2][1], \
                         detection[2][2], \
                         detection[2][3]
            xmin, ymin, xmax, ymax = self.convertBack(float(x), float(y), float(w), float(h))
            pt1 = (xmin, ymin)
            pt2 = (xmax, ymax)
            area = (xmax - xmin) * (ymax - ymin)

            if area < MAX_SIZE and area > MIN_SIZE:
                cv2.rectangle(img, pt1, pt2, (75, 150, 0), 1)
                cv2.putText(img, detection[0].decode() + " [" + str(round(detection[1] * 100, 2)) + "]",
                            (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [75, 150, 0], 2)
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
                if area >= MAX_SIZE or area <= MIN_SIZE:
                    flag.append(detection)

        detections = [x for x in detections if x not in flag]
        return(detections)

    def main(self):
        cap = cv2.VideoCapture(1)
        # cap = cv2.VideoCapture('t1.avi')
        # cap = cv2.VideoCapture('closer_school.mp4')

        cap.set(3, WEIGHT)  # Feed resolution from webcam to YOLO however output is from yolo cfg file resolution
        cap.set(4, HEIGHT)
        out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10.0, (darknet.network_width(netMain), darknet.network_height(netMain)))

        print("Starting the YOLO loop...")

        # Create an image we reuse for each detect
        darknet_image = darknet.make_image(darknet.network_width(netMain), darknet.network_height(netMain), 3)

        # Variables
        frame_count = 0
        mx = frame_show = ''
        self.mission = ''
        while True:
            
            prev_time = time.time()
            ret, frame_read = cap.read()
            frame_read = cv2.resize(frame_read, (HEIGHT, WEIGHT), cv2.INTER_AREA)
            hsv = cv2.cvtColor(frame_read, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            mean_brt = np.mean(v)

            #  Brightness Correction
            if mean_brt > BRT_THRESH:
                frame_read = np.int16(frame_read)
                frame_read = frame_read * (contrast / 127 + 1) - contrast + brightness
                frame_read = np.clip(frame_read, 0, 255)
                frame_read = np.uint8(frame_read)

            frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (darknet.network_width(netMain), darknet.network_height(netMain)),
                                        interpolation=cv2.INTER_LINEAR)  # CHECK RESIZING KEEPING RATIO

            darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())

            detections = darknet.detect_image(netMain, metaMain, darknet_image, THRESH)  # Uses YOLO to detect
            detect = self.checkSize(detections)  # Gets rid of improper detections

            fps = (1 / (time.time() - prev_time))

            image = self.cvDrawBoxes(detect, frame_resized)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            decoded = []
            if detect:
                sg1 = detect[0][0].decode()
                if len(detect)>1:
                    for i in range(len(detect)):
                        decoded.append(detect[i][0].decode())
                    if 'red' in decoded:
                        index = decoded.index('red')
                    elif 'green' in decoded:
                        index = decoded.index('green')
                    elif 'u-turn' in decoded:
                        index = decoded.index('u-turn')
                    else:
                        index = 0
                    sg1 = decoded[index]

                # prec1 = detect[0][1]
                self.sign[sg1][0] += 1
                # self.sign[sg1][1] += prec1
                mx = max(self.sign, key=lambda key: self.sign[key][0])
                if self.sign[mx][0]:
                    frame_show = str(self.sign[mx][0])
                frame_count = 0

            else:
                frame_count += 1  # In order to know IDLE, count frames without any reading and store in frame_count

            self.high_vals = {k: v for (k, v) in self.sign.items() if v[0] >= SIZE}  # Check if there are any values above size limit

            if self.high_vals:  # If there is any sign > SIZE
                max_sign = max(self.high_vals, key=lambda key: self.high_vals[key][0])  # Finds the key with highest frame_count on the dictionary

                self.mission = max_sign
                self.reset_dict()  # 0 = reset all 1 = reset all but left right inter green




            elif frame_count > IDLE_SIZE:  # If No detection for the last IDLE_SIZE frames -> refresh all  (used to avoid random uncertain and uncontinuos detections)
                self.reset_dict()
                mx = 'SEARCHING'
                frame_show = ''
                frame_count = 0
                self.mission = 'default'

            # DEBUGING: write frame count, last mission, the sign with max count and its count, fps
            cv2.putText(image, str(frame_count), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            cv2.putText(image, mx, (400, 570), font, fontScale, fontColor, lineType)
            cv2.putText(image, frame_show, (550, 570), font, fontScale, fontColor, lineType)
            cv2.putText(image, 'Mission: ' + self.mission, (10, 400), font, fontScale, fontColor, lineType)
            cv2.putText(image, 'fps:' + str(int(fps)), (550, 30), font, 0.5, fontColor, lineType)
            cv2.rectangle(image, (0, 0), (10, 10), (60, 60, 60), 1)
            cv2.rectangle(image, (0, 0), (316, 316), (60, 60, 60), 1)

            out.write(image)  # P
            cv2.imshow('YOLO', image)
            cv2.waitKey(3)

    def reset_dict(self):
        self.sign = {key: [0, 0] for key in self.definer}
        frame_count = 0

    def yolo_mission(self):
        return (self.mission)


if __name__ == '__main__':
    yo = YOLO()
    yo.main()