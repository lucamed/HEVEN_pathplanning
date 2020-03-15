from PIL import Image

import os
import random
import copy

b = "data/"
filePath = os.getcwd()
path = os.path.join(filePath,b)
os.mkdir(path)

si = Image.open('sign.jpg')

cropImage = si.crop([25, 90, 125, 190])
cropImage.save('sign-crop.jpg')

road = Image.open("road.jpg")
(r_width, r_height) = road.size

w_size = r_width - 100
h_size = r_height - 100

for i in range(0, 100):

    final_road = road.copy()

    r_width = random.randrange(0, w_size)
    r_height = random.randrange(0, h_size)
    final_road.paste(cropImage, (r_width, r_height))

    os.chdir(path)
    final_road.save('road_00{}.jpg'.format(i))
