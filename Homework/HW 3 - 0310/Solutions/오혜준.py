from PIL import Image
import random
import os

# make folder
os.mkdir('C:\\Users\\USER\\PycharmProjects\\HW2_오혜준\\data')

# crop sign
img=Image.open('C:\\Users\\USER\\PycharmProjects\\HW2_오혜준\\sign.jpg')
imgcrop = img.crop((25, 85, 125, 195))


for i in range(1,101):
    # open road
    img2=Image.open('C:\\Users\\USER\\PycharmProjects\\HW2_오혜준\\road.jpg')

    # random position
    a=random.randrange(0, 1696)
    b=random.randrange(0, 1131)

    # paste
    img2.paste(imgcrop, (a, b))

    #save
    if i<10:
        img2.save('data/road_00{}.jpg'.format(i))
    elif i>=10 and i<100:
        img2.save('data/road_0{}.jpg'.format(i))
    else:
        img2.save('data/road_{}.jpg'.format(i))
