from PIL import Image

def crop_center(pil_img, crop_width, crop_height):
    (img_width, img_height)=pil_img.size
    return pil_img.crop(((img_width-crop_width)//2,
                         (img_height-crop_height)//2,
                         (img_width+crop_width)//2,
                         (img_height+crop_height)//2))

im=Image.open('cat.jpg')
cropImage=crop_center(im,500,500)
cropImage.save('cat-thumb.jpg')
