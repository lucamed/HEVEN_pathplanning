import os, random, copy
from PIL import Image

directory="data"
parent_dir=os.getcwd()
path=os.path.join(parent_dir,directory)
os.mkdir(path)

im1=Image.open('road.jpg')
im2=Image.open('sign.jpg')
(im1_w,im1_h)=im1.size
#print(im1.size)

cropbox=(260,200,370,300)
crop_im2=im2.crop(cropbox)
(crop_w,crop_h)=crop_im2.size
#print(crop_im2.size)

range_w=im1_w-crop_w
range_h=im1_h-crop_h
#crop_im2.show()

for i in range(1,101):
    im11=im1.copy()
    x=random.randint(0,range_w)
    y=random.randint(0,range_h)
    area=(x,y)

    im11.paste(crop_im2, area)
    #im11.show()
    im11.save(os.path.join(path,'road_'+str(i)+'.jpg'))
