"""
The main problem of this HW is to detect both lines in a lane and its center line.

1. Open the given videos.
2. There are several ways to solve this. You can google and study about lane detection. 
	HSV colors, HoughlinesP, CannyEdge and GaussianBlur are some of the functions you might need.
	Usage of OpenCV is more than recommended.

3. Draw the left side line as RED and the right side BLUE. Also, find the middle point (desired path) and draw a line in GREEN
4. Use addWeighted to add all masks on the original image.
5. The program should work for finding the lanes in at least YW.mp4 and YW.mp4
	

Check the attached example output videos, it will be helpful in understanding the question.
"""


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def cannyed_for_yw(frame):
     #converts frame to grayscale
    gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    #make yellow mask and white one
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask_white = cv2.inRange(frame, 200, 255)
    mask_yellow=cv2.inRange(img_hsv,lower_yellow,upper_yellow)
    mask_image = cv2.bitwise_or(mask_yellow, mask_white)
    mask_final=cv2.bitwise_and(mask_image,gray)
    ##now do a canny edge
    blur=cv2.GaussianBlur(gray,(5,5),0)
    canny=cv2.Canny(blur,50,150)
    return canny
def cannyed(frame): ##we have to do canny edge dQetection
    #converts frame to grayscale
    gray=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    ##apply a gaussian blur and canny
    blur=cv2.GaussianBlur(gray,(5,5),0)
    canny=cv2.Canny(blur,50,150)
    return canny
def do_segment(frame): ## to get rid of the useless area(focus on the lane)
    height=frame.shape[0]
    width=frame.shape[1]
    ##creates a polygon that draw the lines and make masks
    polygons=np.array([[[width,height],[0,height],[width/2,height*3/5]]],dtype='int64')
    mask=np.zeros_like(frame)
    ## make the poly inside white and otherwise black
    cv2.fillPoly(mask,polygons,255)
    ##put the frame into a mask
    segment=cv2.bitwise_and(frame,mask)
    return segment
def draw_lines(img,lines,color):
    img=img.copy()
    line_img=np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint8,)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_img, (x1,y1),(x2,y2),color,5)
    return line_img
def calculate_lines(lines,frame):
    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []
    min_y=frame.shape[0]*0.6 ##find max and min of y coordinates
    max_y=frame.shape[0]
    for line in lines:
        for x1,y1,x2,y2 in line:
            slope= np.polyfit((x1,x2),(y1,y2),1)
            if slope[0]<0 : #left line
                left_line_x.extend([x1,x2])
                left_line_y.extend([y1,y2])
            else: #right line
                right_line_x.extend([x1,x2])
                right_line_y.extend([y1,y2])

    try :
        poly_left=np.poly1d(np.polyfit(left_line_y,left_line_x,deg=1))
        left_x_start=poly_left(max_y)
        left_x_end=poly_left(min_y) ## making left line
        poly_right=np.poly1d(np.polyfit(right_line_y,right_line_x,deg=1))
        print(poly_right)
        right_x_start=poly_right(max_y)
        print(max_y)
        print(right_x_start)
        right_x_end=poly_right(min_y)##making right line
        ##finding intersection to draw center line
        left=np.polyfit(left_line_y,left_line_x,deg=1)
        right=np.polyfit(right_line_y,right_line_x,deg=1)
        intersection_x=(right[1]-left[1])/(left[0]-right[0])
        intersection_y=(right[1]-left[1])*left[0]/(left[0]-right[0])+left[1]
 
    ##making center line
        tangent_of_centerline=(left[0]+right[0])/2
        yaxis=tangent_of_centerline*(-1)*intersection_x+intersection_y
        poly_center=np.poly1d(np.array([tangent_of_centerline,yaxis]))

        center_x_start=poly_center(max_y)
        center_x_end=poly_center(min_y)
        ##making arrays that would be use to draw lines
        left_array=np.array([[[left_x_start,max_y,left_x_end,min_y]]],np.int32)
        right_array=np.array([[[right_x_start,max_y,right_x_end,min_y]]],np.int32)
        center_array=np.array([[[center_x_start,max_y,center_x_end,min_y]]],np.int32)
        ##draw lines with appropriate colors
    
        left_final=draw_lines(frame,left_array,[0,0,255])
        right_final=draw_lines(frame,right_array,[255,0,0])
        center_final=draw_lines(frame,center_array,[0,255,0])
        ##add them altogether
        lines_final=cv2.add(cv2.add(left_final,right_final),center_final,)
        img=cv2.addWeighted(frame,0.8,lines_final,1.0,0.0)
        cv2.imshow("final",img)
    except TypeError:
            return True
    
  ##########################
    
WW=cv2.VideoCapture('C:\HEVEN\week4\WW.mp4')
if(WW.isOpened()==False): ##when it fails to run
    print("Error opening file")
while(WW.isOpened()):
    ret,frame=WW.read()
    try :
        canny=cannyed(frame)
        segment=do_segment(canny) 
        ##do hough transform to get details
        hough=cv2.HoughLinesP(segment,2,np.pi/180,100,np.array([]),minLineLength=100,maxLineGap=50)
        ##now draw lines based on hough transform
        lines=calculate_lines(hough,frame)

        if cv2.waitKey(10)&0xFF==ord('q'):
            break
    except cv2.error:
            break
WW.release()
cv2.destroyAllWindows()
################

YW=cv2.VideoCapture('C:\HEVEN\week4\YW.mp4')
if(YW.isOpened()==False): ##when it fails to run
    print("Error opening file")
else: print("im opened")
while(YW.isOpened()):
    ret,frame=YW.read()
    canny=cannyed_for_yw(frame)
    segment=do_segment(canny) 
    ##do hough transform to get details
    hough=cv2.HoughLinesP(segment,2,np.pi/180,100,np.array([]),minLineLength=100,maxLineGap=50)
    ##now draw lines based on hough transform
    lines=calculate_lines(hough,frame)

    if cv2.waitKey(10)&0xFF==ord('q'):
        break

YW.release()
cv2.destroyAllWindows()



