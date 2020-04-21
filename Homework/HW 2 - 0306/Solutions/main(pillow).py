from PIL import Image
import os

# set path with os
basic_path = os.path.join(os.getcwd(), "../")
img_path = os.path.join(basic_path, "cat.jpg")

# open image
im = Image.open(img_path)

# get width, height of image
width, height = im.size

# center crop
new_img = im.crop([width / 2 - 250, height / 2 - 250, width / 2 + 250, height / 2 + 250])

# save image
center_path = os.path.join(basic_path, "center.jpg")
new_img.save(center_path)
