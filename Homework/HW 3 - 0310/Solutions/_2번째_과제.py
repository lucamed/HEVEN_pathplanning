### 1. Crop the road sign picture. (Any sign you want)
### 2. Paste the road sign picture on the random position of the road picture.
###  * The road sign should not be cut off
### 3. Create 100 pictures and save the file as 'road_001.jpg', 'road_002.jpg', ..., 'road_100.jpg' in data directory.

from PIL import Image
from random import randint
import os

os.makedirs("C:/Users/hyun1/Desktop/HEVEN/hw_0307/2번째 과제/data")

sign = Image.open("sign.jpg")

left = 130 ###그림 왼쪽 가장자리부터의 길이
top = 200 ###그림 위쪽 가장자리부터의 길이
width = 120 ###자를 너비 길이
height = 100 ###자를 높이 길이
size = (left, top, left+width, top+height)
crop_sign = sign.crop(size)
crop_sign.save("cropped.jpg")

road = Image.open("road.jpg")

( r_width, r_height ) = road.size
i = randint(0, r_width-120)
j = randint(0, r_height-100)
num = 1
for num in range(1,101):
    road.paste(crop_sign, (i, j))
    if num in range(1,10):
        road.save("C:/Users/hyun1/Desktop/HEVEN/hw_0307/2번째 과제/data/road_00%d.jpg.jpg" %num)
    elif num in range(10,100):
        road.save("C:/Users/hyun1/Desktop/HEVEN/hw_0307/2번째 과제/data/road_0%d.jpg.jpg" %num)
    else:
        road.save("C:/Users/hyun1/Desktop/HEVEN/hw_0307/2번째 과제/data/road_%d.jpg.jpg" %num)