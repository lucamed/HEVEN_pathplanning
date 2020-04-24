from PIL import Image
import random
import os
img=Image.open("sign.jpg")
(i,j)=img.size #sign 이미지 크기
area=(140,80,250,200)
cropped_img=img.crop(area)
(a,b)=(cropped_img.size)
cropped_img.save("cropped_img.jpg")
cut=Image.open("cropped_img.jpg")
c=image.open("road.jpg")
(d,e)=(f.size)
os.mkdir('date')
m=1
while m<=100:
    f=random.randrange(0,d)
    g=random.randrange(0,e)
    h=f-a
    k=g-b

    l=f.paste(cut,(h,k))
    l.save("data/road%d.jpg"%m)
    l.show()
    c=image.open("road.jpg")
    m+=1
    l.close()

    
