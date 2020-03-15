import os
from PIL import Image
from random import randint

current_dir = os.getcwd()
path = os.path.join(current_dir,'data')
if not os.path.exists(path):
    os.makedirs(path)

road_bg = Image.open('road.jpg')
sign = Image.open('sign.jpg')
area = (140, 90, 240, 190)
cropped_sign = sign.crop(area)


for i in range(100):
    i+=1
    road = road_bg.copy()
    (width,height) = road.size
    m = randint(0, width-100)
    n = randint(0, height-100)
    road.paste(cropped_sign,(m, n))
    road.save(path+'/road_%03d.jpg'%i)
    
    

