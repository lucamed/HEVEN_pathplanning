import matplotlib.pylab as plt
import cv2
import numpy as np

def region_of_interest(img,vertices):
    mask=np.zeros_like(img)
    match_mask_color=255
    cv2.fillPoly(mask,vertices,match_mask_color)
    masked_image=cv2.bitwise_and(img,mask)
    return masked_image

def draw_the_lines(img,lines):
    img=np.copy(img)
    blank_image=np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint8)

    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(blank_image,(x1,y1),(x2,y2),(0,0,255),thickness=5)

    img=cv2.addWeighted(img,0.8,blank_image,1,0)
    return img

def process(image):        
    height=image.shape[0]
    width=image.shape[1]

    region_of_interest_vertices=[
        (0,height),
        (width,height),
        (500,300)
]

    gray_image=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    canny_image=cv2.Canny(gray_image,100,200)
    cropped_image=region_of_interest(canny_image,np.array([region_of_interest_vertices],np.int32),)

    lines=cv2.HoughLinesP(cropped_image,
                          rho=2,
                          theta=np.pi/180,
                          threshold=100,
                          lines=np.array([]),
                          minLineLength=40,
                          maxLineGap=50)

    image_with_lines=draw_the_lines(image,lines)
    return image_with_lines

cap=cv2.VideoCapture('WW.mp4')

while(cap.isOpened()):
    ret,frame=cap.read()
    frame=process(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
