#HW5_2017315484_이주헌

import matplotlib.pyplot as plt
import numpy as np
import cv2

ywlow = np.array([18, 94, 140])        #yellow 색상과 white 색상의 HSV 범위를 지정해준다
ywup = np.array([48, 255, 255]) 
sens = 25
whlow = np.array([0, 0, 255-sens])
whup = np.array([255, sens, 255])

def perp(a) :       #양차선의 가운데 선이 따라갈 점을 찍기위해서 수직의 선을 긋기위한 함수생성
    b = np.empty_like(a)    # 모양과 형태가 동일한 배열을 반환한다
    b[0] = -a[1]
    b[1] = a[0]
    return b

def seg_intersect(a1, a2, b1, b2) :     # 두 개의 선의 교차점을 구한다
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )

    return (num / denom.astype(float))*db + b1

def Middlepoint(p1, p2):         # 입력값 p1과 p2를 이용해서 가운데 값인 얻는다
    lenAB = np.sqrt(np.power(p1[0] - p2[0], 2)+np.power(p1[1] - p2[1], 2))      #두 점의 길이를 구한다
    length = 1          #150 - lenAB
      
    cx = p2[0] + (p2[0] - p1[0]) / lenAB * length
    cy = p2[1] + (p2[1] - p1[1]) / lenAB * length

    p1, p2 = p2, p1
    length = 200 
    cx2 = p2[0] + (p2[0] - p1[0]) / lenAB * length
    cy2 = p2[1] + (p2[1] - p1[1]) / lenAB * length

    return int(cx), int(cy), int(cx2), int(cy2)

def drawLines(line_image, mask, side):       #이력을 받은 이미지의 도로에 선을 긋도록 하는 함수

    rho = 1         #라인을 그리기 위해서 필요한 변수들을 입력
    theta = np.pi/180 
    threshold = 60
    min_line_length = 40
    max_line_gap = 150
    dot1 = dot2 = np.array([0, 0])
    
    lines_ = cv2.HoughLinesP(mask, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)      #OpenCV의 HoughLinesP 함수를 사용한다

    if lines_ is not None:
        dot1 = np.array([lines_[:][:][0][0][2], lines_[:][:][0][0][3]])
        dot2 = np.array([lines_[:][:][0][0][0], lines_[:][:][0][0][1]])
        
        if side == 'left':      #left 라인일경우 빨간색 라인을 그린다
            color = (0, 0, 255)
            dot1, dot2 = dot2, dot1

        elif side == 'right':       #right 라인일경우 파란색 라인을 그린다
            color = (255, 0, 0)

        cx, cy, cx2, cy2 = Middlepoint(dot1, dot2)
        lines_ = np.append(lines_, [[[cx, cy, cx2, cy2]]], axis=0)
        for line in lines_:
            for x1,y1,x2,y2 in line:
                cv2.line(line_image, (x1,y1), (x2,y2), color, 10)

    return line_image, dot1, dot2

def region_of_interest(frame):          #모든 영역이 아닌 차선부분의 영역만 인식이 되도록 관심영역설정 함수만들기
    maskR_ = np.zeros_like(frame)  
    maskL_ = np.zeros_like(frame)  

    ignore_mask_color = 255

    imshape = frame.shape
    
    #관심영역을 vertices에 저장하기
    verticesL = np.array([[(0, imshape[0]),(int(imshape[1]/2), int(55+imshape[0]/2)), (int(imshape[0]/2), imshape[1]), (0, imshape[1])]], dtype=np.int32)
    verticesR = np.array([[(imshape[1], imshape[0]),(int(imshape[1]/2), int(47+imshape[0]/2)), (int(imshape[0]/2), imshape[1]), (imshape[1], imshape[1])]], dtype=np.int32)

    cv2.fillPoly(maskR_, verticesR, ignore_mask_color)      #폴리곤을 그리는 함수를 사용하여 오각형 외곽선과 내부가 채워진 오각형을 그린다
    cv2.fillPoly(maskL_, verticesL, ignore_mask_color)

    maskR = cv2.bitwise_and(frame, maskR_)          #maskR,maskL의 pixel이 nonzero일 경우에만 return을 해준다
    maskL = cv2.bitwise_and(frame, maskL_)

    return maskL, maskR



newvideo = cv2.VideoCapture('YW.mp4')

while(newvideo.isOpened()):
    ret, frame = newvideo.read()
    
    line_image = np.copy(frame)*0       #라인을 그리기 위한 빈 라인을 생성한다
    frame = cv2.GaussianBlur(frame, (5, 5), 0)      #차선을 명확하게 보기 위해 차선이외의 배경은 가우시안블러로 흐릿하게 해주기

    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)        #OpenCV를 이용해 이미지를 gray로 변경
    canny_image = cv2.Canny(gray_image, 100, 200)       #canny edge detection으로 edge로 판단된 부분만 남기고 나머지는 지워서 선으로 표현해주기

    mask_left, mask_right = region_of_interest(canny_image)

    #cv2.imshow('finalL', mask_left)        #진행상황을 확인하기 위한 코드
    #cv2.imshow('fin3al', mask_right)       #진행상황을 확인하기 위한 코드
    
    line_image, dotL1, dotL2 = drawLines(line_image, mask_left, 'left')
    line_image, dotR1, dotR2 = drawLines(line_image, mask_right, 'right')
    final = frame
    if not np.all(line_image):
        inter = seg_intersect(dotL1, dotL2, dotR1, dotR2)

        if not np.isnan(inter[0]) and not np.isnan(inter[1]):
            #print('Target: ', inter)
            cv2.circle(line_image,(int(inter[0]), int(line_image.shape[1]/2.5)), 10, (255,160,255))
            y_findR = line_image.shape[1]
            y_findL = line_image.shape[1]
            slopeR = (dotR2[1] - dotR1[1])/(dotR2[0] - dotR1[0])
            slopeL = (dotL2[1] - dotL1[1])/(dotL2[0] - dotL1[0])
            x_of_yR = dotR1[0] + (y_findR - dotR1[1])/slopeR
            x_of_yL = dotL1[0] + (y_findL - dotL1[1])/slopeL


            cv2.line(line_image,(int(x_of_yL+((x_of_yR-x_of_yL)/2)), line_image.shape[1]),(int(inter[0]), int(line_image.shape[1]/2.5)), (0,255,0), 6)


        final = cv2.addWeighted(frame, 0.8, line_image, 1, 0)        # 영상인식으로 그린 라인을 입히기


            # cv2.imshow('final', final)
            # cv2.waitKey(0)

    # out.write(final)

    cv2.imshow('frame', final)      #최종 결과물을 확인하기 위한 코드
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

newvideo.release()
# out.release()
cv2.destroyAllWindows()
