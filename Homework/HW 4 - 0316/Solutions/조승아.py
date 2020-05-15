import cv2
import numpy as np


def canny(img):
    gray_img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    gaussian_img=cv2.GaussianBlur(gray_img,(5,5),0)
    canny_img=cv2.Canny(gaussian_img,50,100)
    return canny_img

def interest(img):
    mask=np.zeros_like(img)
    imshape=img.shape
    vertices=np.array([[(100,imshape[0]),
                    (450,320),
                    (550,320),
                    (imshape[1]-20,imshape[0])]],dtype=np.int32)
    
    if len(img.shape)>2:
        channel_count=img.shape[2]
        ignore_mask_color=(255,)

    else:
        ignore_mask_color=255

    cv2.fillPoly(mask,vertices,ignore_mask_color)
    masked_image=cv2.bitwise_and(img,mask)
    return masked_image

def draw_line(img,lines):
    l=0
    r=0
    x_l1=0
    x_l2=0
    y_l1=0
    y_l2=0
    x_r1=0
    x_r2=0
    y_r1=0
    y_r2=0
    
    for line in lines:
        for x1,y1,x2,y2 in line:
            parameter=np.polyfit((x1,x2),(y1,y2),1)
            slope=parameter[0]
            if slope>0:
                l+=1
                x_l1+=x1
                x_l2+=x2
                y_l1+=y1
                y_l2+=y2

            else:
                r+=1
                x_r1+=x1
                x_r2+=x2
                y_r1+=y1
                y_r2+=y2

    x_l1/=l
    x_l2/=l
    y_l1/=l
    y_l2/=l
    x_r1/=r
    x_r2/=r
    y_r1/=r
    y_r2/=r

    cv2.line(img,(int(x_l1),int(y_l1)),(int(x_l2),int(y_l2)),(255,0,0),5)
    cv2.line(img,(int(x_r1),int(y_r1)),(int(x_r2),int(y_r2)),(0,0,255),5)            

    x_top=(x_l1+x_r2)/2
    y_top=(y_l1+y_r2)/2
    x_bottom=(x_l2+x_r1)/2
    y_bottom=(y_l2+y_r1)/2
    cv2.line(img,(int(x_top),int(y_top)),(int(x_bottom),int(y_bottom)),(0,255,0),5)
    cv2.circle(img,(int(x_top),int(y_top)),10,(255,255,255),1)
 
def hough_line(img):
    r=2
    theta=np.pi/180
    threshold=100
    min_line=100
    max_line=200
    lines=cv2.HoughLinesP(img,r,theta,threshold,np.array([]),
                          minLineLength=min_line,
                          maxLineGap=max_line)
    line_img=np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint8)
    draw_line(line_img,lines)
    return line_img

road=cv2.imread("WW1.jpg")      #파일명 바꾸면 WW1, YW1, YW2 적용가능

mask=interest(canny(road))
lines=hough_line(mask)
line_road=cv2.addWeighted(road,0.8,lines,1,0)

cv2.imshow("road",line_road)
cv2.waitKey(0)

