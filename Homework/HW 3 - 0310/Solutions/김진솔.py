from PIL import Image
import os


path = 'data/'
samples = 3

try:
    if not os.path.exists(path):
        os.makedirs(path)
        print ("Successfully created the directory %s " % path)
    else:
        print("Path already exists")
except OSError:
    print ("Creation of the directory %s failed" % path)

for X in range(samples):
    road = Image.open("road.jpg")
    sign = Image.open("sign.jpg")
    print(road.size)
    print(sign.size)

    new_sign = sign.crop((20, 80, 130, 200))
    new_sign.save("crop.jpg")
    new_sign = Image.open("crop.jpg")
    print(new_sign.size)

    import random
    a = random.randint(0, road.size[0]-new_sign.size[0])
    b = random.randint(0, road.size[1]-new_sign.size[1])
    print(a, b)
    area = (a, b, a + new_sign.size[0], b + new_sign.size[1])
    print(area)
    road.paste(new_sign, area)
    road.show()
    road.save(path+"road_"+str(X)+".jpg")









