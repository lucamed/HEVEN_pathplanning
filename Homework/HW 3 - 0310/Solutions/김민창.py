from PIL import Image
import random
import os

path = r'C:\Users\sjy26\PycharmProjects\untitled1\data'

os.mkdir(path)

sign = Image.open("sign.jpg")
road = Image.open("road.jpg")

area = (130,90,250,200)  # set the area for getting sign
cropped = sign.crop(area)  # crop the one sign from a lot of signs


for i in range(1,101):
    x=random.randint(0,1579)  # get a random number for x,y coordinates and these number is obtained by calculating
    y=random.randint(0,1021)  # original size of road images(1696*1131) and sign(120*110)
    road.paste(cropped,(x,y))  # paste cropped image into road image
    road.save('data/road_0%d.jpg'%i)  # save the result
    road = Image.open("road.jpg")  # initialize road image

