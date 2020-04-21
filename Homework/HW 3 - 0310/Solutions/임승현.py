# -*- coding: cp949 -*-
"""
1. Crop the road sign picture. (Any sign you want)
2. Paste the road sign picture on the random position of the road picture.
 * The road sign should not be cut off
3. Create 100 pictures and save the file as 'road_001.jpg', 'road_002.jpg', ..., 'road_100.jpg' in data directory.

Samples are attached in this file.
"""
import numpy as np
import cv2
from random import *
import os
parent_dir="C:\Users\�ӽ���\Desktop\HEVEN\week2"
directory="data"
path=os.path.join(parent_dir,directory)
os.mkdir(path)

sign=cv2.imread("C:\Users\�ӽ���\Desktop\HEVEN\week2\hw_0307\hw_0307\hw_1\sign.jpg",cv2.IMREAD_COLOR)

cropped=sign.copy()
cropped=sign[91:91+98,31:31+91]
#Roi �����
for i in range (1,101):
    n=str(i)
    road=cv2.imread("C:\Users\�ӽ���\Desktop\HEVEN\week2\hw_0307\hw_0307\hw_1\\road.jpg",cv2.IMREAD_COLOR)
    row=randint(1+49,1131-49)
    col=randint(1+46,1696-46)
    roi=road[row-49:row+49,col-46:col+45]
    #����ũ �����
    sign2gray=cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
    ret, mask=cv2.threshold(sign2gray,10,255,cv2.THRESH_BINARY)
    mask_inv=cv2.bitwise_not(mask)

    #Roi���� �ΰ� �ش��ϴ� �κи� ���������� �����
    backgr=cv2.bitwise_and(roi,roi,mask=mask_inv)
    #���� �̹������� ���� �κи� �����ϱ�
    sign_image=cv2.bitwise_and(cropped,cropped,mask=mask)
    #ǥ���� �̹��� ����� cv2.add�� �������� ����� Roi�� ǥ���� �̹��� �ֱ�
    dst=cv2.add(backgr,sign_image)
    road[row-49:row+49,col-46:col+45]=dst
    if(1<=i<=9):
        
        cv2.imwrite(os.path.join(path,"road_00"+n+".jpg"),road)
        cv2.destroyAllWindows()
    elif(i==100):
        cv2.imwrite(os.path.join(path,"road_"+n+".jpg"),road)
        cv2.destroyAllWindows()
    else:
        cv2.imwrite(os.path.join(path,"road_0"+n+".jpg"),road)
        cv2.destroyAllWindows()
