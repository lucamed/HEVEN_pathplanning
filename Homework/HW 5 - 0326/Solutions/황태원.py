import cv2
import numpy as np
import matplotlib.pyplot as plt
##Lane detection에 대한 이해가 부족하여 github에 올려주신 솔루션 코드를
##바탕으로 코드한줄씩 의미를 분석해보고 있습니다. 더 노력할게요 ㅠ
# HSV Parameters 
low_yellow = np.array([18, 94, 140])  #노란색의 범위 지정 H는 18 S는 94 V는 140부터
up_yellow = np.array([48, 255, 255])  #H는 48 S는 255 V는 255 까지

sens = 25
low_white = np.array([0, 0, 255-sens])  #흰색의 범위 지정
up_white = np.array([255, sens, 255]) #

## 두 선에 대해 각각 수직인 선을 그어 교차점을 찾는 코드
def perp(a) :# Computes a perpendicular to a line a = (ax, ay)
    b = np.empty_like(a)  #주어진 어레이의 형태와 타입을 갖는 새로운 어레이로 반환, 
    b[0] = -a[1]             #empty like를 사용하면 반응속도가 빠르다는 장점이 있음
    b[1] = a[0] 
    return b
                                       
# Intersection of both lines (path target)
def seg_intersect(a1, a2, b1, b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da) 
    denom = np.dot( dap, db) #np.dot 행렬곱
    num = np.dot( dap, dp ) 
    
    # Returns x, y
    return (num / denom.astype(float))*db + b1
 ##
##두 차선의 중심점: 왼쪽차선의 점과 오른쪽차선의 점의 중간값+ 왼쪽좌표값
# Given 2 points, find a 3rd at certain distance
def pointC(p1, p2): #C점 좌표 정의
    lenAB = np.sqrt(np.power(p1[0] - p2[0], 2)+np.power(p1[1] - p2[1], 2))  #두 점 사이의 거리 공식
    length = 1 #150 - lenAB  
       
    cx = p2[0] + (p2[0] - p1[0]) / lenAB * length
    cy = p2[1] + (p2[1] - p1[1]) / lenAB * length

    p1, p2 = p2, p1  ##
    length = 200 
    cx2 = p2[0] + (p2[0] - p1[0]) / lenAB * length
    cy2 = p2[1] + (p2[1] - p1[1]) / lenAB * length

    return int(cx), int(cy), int(cx2), int(cy2)

def drawLines(line_image, mask, side):

    rho = 1 # distance resolution in pixels of the Hough grid
    threshold = 60     # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 40  #minimum number of pixels making up a line
    max_line_gap = 150    # maximum gap in pixels between connectable line segments
    dot1 = dot2 = np.array([0, 0])
    lines_ = cv2.HoughLinesP(mask, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)#하프변환
    # line_arr = np.squeeze(lines_) 

    if lines_ is not None:
        dot1 = np.array([lines_[:][:][0][0][2], lines_[:][:][0][0][3]])
        dot2 = np.array([lines_[:][:][0][0][0], lines_[:][:][0][0][1]])
        
        if side == 'left':
            color = (0, 0, 255)
            # Swaps points in order to maintain format: dot1 being on the bottom and dot2 end of line
            dot1, dot2 = dot2, dot1

        elif side == 'right':
            color = (255, 0, 0)

        cx, cy, cx2, cy2 = pointC(dot1, dot2)
        # cv2.line(line_image,(int(cx2), int(cy2)), (int(cx), int(cy)), color, 10)
        lines_ = np.append(lines_, [[[cx, cy, cx2, cy2]]], axis=0)
        for line in lines_:
            for x1,y1,x2,y2 in line:
                cv2.line(line_image, (x1,y1), (x2,y2), color, 10)

    return line_image, dot1, dot2

def ROI(frame):
    # Mask ROI for left and right 
    maskR_ = np.zeros_like(frame)  
    maskL_ = np.zeros_like(frame)  

    ignore_mask_color = 255

    imshape = frame.shape
    
    verticesL = np.array([[(0, imshape[0]),(int(imshape[1]/2), int(55+imshape[0]/2)), (int(imshape[0]/2), imshape[1]), (0, imshape[1])]], dtype=np.int32)
    verticesR = np.array([[(imshape[1], imshape[0]),(int(imshape[1]/2), int(47+imshape[0]/2)), (int(imshape[0]/2), imshape[1]), (imshape[1], imshape[1])]], dtype=np.int32)

    cv2.fillPoly(maskR_, verticesR, ignore_mask_color)
    cv2.fillPoly(maskL_, verticesL, ignore_mask_color)

    maskR = cv2.bitwise_and(frame, maskR_)
    maskL = cv2.bitwise_and(frame, maskL_)

    return maskL, maskR



cap = cv2.VideoCapture('data/YW.mp4')

# Record Video
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (frame_width, frame_height))

while(cap.isOpened()):
    ret, frame = cap.read()
    
    line_image = np.copy(frame)*0 # creating a blank to draw lines on
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny_image = cv2.Canny(gray_image, 100, 200)

    mask_left, mask_right = ROI(canny_image)

    cv2.imshow('finalL', mask_left)
    cv2.imshow('fin3al', mask_right)

    line_image, dotL1, dotL2 = drawLines(line_image, mask_left, 'left')
    line_image, dotR1, dotR2 = drawLines(line_image, mask_right, 'right')
    final = frame
    if not np.all(line_image):
        inter = seg_intersect(dotL1, dotL2, dotR1, dotR2)

        if not np.isnan(inter[0]) and not np.isnan(inter[1]):
            print('Target: ', inter)
            cv2.circle(line_image,(int(inter[0]), int(line_image.shape[1]/2.5)), 10, (255,160,255))
            y_findR = line_image.shape[1]
            y_findL = line_image.shape[1]
            slopeR = (dotR2[1] - dotR1[1])/(dotR2[0] - dotR1[0])
            slopeL = (dotL2[1] - dotL1[1])/(dotL2[0] - dotL1[0])
            x_of_yR = dotR1[0] + (y_findR - dotR1[1])/slopeR
            x_of_yL = dotL1[0] + (y_findL - dotL1[1])/slopeL


        cv2.line(line_image,(int(x_of_yL+((x_of_yR-x_of_yL)/2)), line_image.shape[1]),(int(inter[0]), int(line_image.shape[1]/2.5)), (0,255,0), 6)


        final = cv2.addWeighted(frame, 0.8, line_image, 1, 0)


            # cv2.imshow('final', final)
            # cv2.waitKey(0)

    # out.write(final)

    cv2.imshow('frame', final)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
# out.release()
cv2.destroyAllWindows()
