from PIL import Image
im = Image.open('cat.jpg')

(width, height) = im.size

print(width, height)

cropImage = im.crop( [width/2-250, height/2-250, width/2+250, height/2+250])
cropImage.save('python-crop.jpg')



