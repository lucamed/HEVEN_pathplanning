from PIL import Image

img = Image.open("Cat.jpg")

width, height = img.size
area = (width/2-250, height/2-250, width/2+250, height/2+250)
cropped_img = img.crop(area)

print(img.size)
print(cropped_img.size)

cropped_img.save("center.jpg")