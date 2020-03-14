import cv2
import random
import os

path = 'data2'
samples = 100

# Make folder
if not os.path.exists(path):
    os.makedirs(path)

# Open images
bg_img = cv2.imread('road.jpg', 1)
target = cv2.imread('sign.jpg', 1)

# Crop desired sign [Y1:Y2 X1:X2]
target = target[86:191, 131:240]

# Get height and width of background img
bg_H = bg_img.shape[0]
bg_W = bg_img.shape[1]

# Loop sample times
for i in range(samples):
    i+=1                                # Match naming 1~100
    result = bg_img.copy()              # Create a copy of the background img

    t_H = target.shape[0]               # Height and width of target sign
    t_W = target.shape[1]

    x = random.randrange(0, bg_W-t_W)
    y = random.randrange(0, bg_H-t_H)

    result[y:t_H+y, x:t_W+x] = target   # Paste target into bg
    cv2.imwrite(os.path.join(path ,'road_0'+str(i)+'.jpg'), result)