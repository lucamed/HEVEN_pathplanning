#hw3

from PIL import Image
import os
import random

os.mkdir('data') # make a directory named "data"

sign = Image.open('C:/Users/hj971/OneDrive/바탕 화면/성균관대학교/동아리/HEVEN/과제/hw_3/hw_1/안호진/sign.jpg') # open the sign image file

cropImage = sign.crop((130, 200, 250, 310)) # cut the sign image
cropImage.show() # show cropped sign image

a, b = cropImage.size # find size of cropped sign

road = Image.open('C:/Users/hj971/OneDrive/바탕 화면/성균관대학교/동아리/HEVEN/과제/hw_3/hw_1/안호진/road.jpg') # open the road image file

x, y = road.size # find size of road

for i in range(1, 101) :
    
    random_x = random.randint(0, x-a) # Random x-coordinate
    random_y = random.randint(0, y-b) # Random y-coordinate
    road.paste(cropImage, (random_x, random_y)) # Attach sign image to road image

    if i < 10 :
        road.save('C:/Users/hj971/OneDrive/바탕 화면/성균관대학교/동아리/HEVEN/과제/hw_3/hw_1/안호진/data/road_00%d.jpg' %i) # save the road image at 'data' directory
    elif i < 100 :
        road.save('C:/Users/hj971/OneDrive/바탕 화면/성균관대학교/동아리/HEVEN/과제/hw_3/hw_1/안호진/data/road_0%d.jpg' %i) # save the road image at 'data' directory
    else :
        road.save('C:/Users/hj971/OneDrive/바탕 화면/성균관대학교/동아리/HEVEN/과제/hw_3/hw_1/안호진/data/road_%d.jpg' %i) # save the road image at 'data' directory

    road = Image.open('C:/Users/hj971/OneDrive/바탕 화면/성균관대학교/동아리/HEVEN/과제/hw_3/hw_1/안호진/road.jpg') # reopen road image
