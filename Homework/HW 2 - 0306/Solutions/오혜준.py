from PIL import Image

img=Image.open('C:\\Users\\USER\\Downloads\\hw_0306\\hw_week1\\hw_2\\cat.jpg')
print(img.size)
imgcrop = img.crop((550, 283, 1050, 783))
imgcrop.show()
imgcrop.save('catcrop.jpg')
