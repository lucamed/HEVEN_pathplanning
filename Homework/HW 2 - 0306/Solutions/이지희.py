from PIL import Image

img = Image.open('cat.jpg')
(width,height) = img.size
area = ( width/2-250, height/2-250 , width/2+250, height/2+250 )


cropped_img = img.crop(area)
cropped_img.save('center.jpg')


