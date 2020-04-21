from PIL import Image

img=Image.open("cat.jpg")

size=img.size
a=size[0]/2
b=size[-1]/2

cropImage = img.crop((a-250,b-250,a+250,b+250))
cropImage.save('cat-crop.jpg')
