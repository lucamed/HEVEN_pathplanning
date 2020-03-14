from PIL import Image
import os
import random

sign = Image.open("../sign.jpg")
sign_cropped = sign.crop([135, 200, 250, 310])
sign_w, sign_h = sign_cropped.size
road = Image.open("../road.jpg")
road_w, road_h = road.size

w_limit = road_w - sign_w
h_limit = road_h - sign_h

for i in range(1, 101):
    road = Image.open("../road.jpg")

    random_w = random.randrange(0, w_limit)
    random_h = random.randrange(0, h_limit)

    road.paste(sign_cropped, (random_w, random_h))

    # filename = road_001.jpg, road_002.jpg, ...
    new_path = os.path.join(os.getcwd(), "data", "road_" + f"{i}".zfill(3) + ".jpg")
    road.save(new_path)
