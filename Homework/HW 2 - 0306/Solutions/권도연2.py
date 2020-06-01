from PIL import Image
img = Image.open("cat.jpg")
(a,b)=img.size
c=a//2-250
d=b//2 -250
print("%d"%a)
print("%d"%b)
area=(c,d,c+500,d+500)
cropped_img=img.crop(area)
cropped_img.show()