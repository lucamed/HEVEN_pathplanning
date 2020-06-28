import cv2
import numpy as np
from math import atan, degrees

#Path의 핵심기능인 라인검출에 필요한 모든 유틸함수들이 들어있는 파일입니다.

BRT_THRESH = 160

# Correction
brightness = -40
contrast = -20


boundaries = [
    (np.array([161, 155, 84], dtype="uint8"), np.array([179, 255, 255], dtype="uint8")), # red1
    (np.array([0, 100, 70], dtype="uint8"), np.array([20, 255, 255], dtype="uint8")), # red2
    (np.array([94, 80, 200], dtype="uint8"), np.array([126, 255, 255], dtype="uint8")), # blue
    (np.array([10, 30, 50], dtype="uint8"), np.array([25, 255, 255], dtype="uint8")), #yellow
    (np.array([0, 0, 220], dtype="uint8"), np.array([180, 20, 255], dtype="uint8")) # white
]

dest = (480, 500)

n_windows = 10

min_pixel_num = 5

#기울기를 구하기 위해 1차식 고정
poly_order = 1

#도로폭(cm)
#277
shift_const = 304
#좌우 concat 시 공백 상수
blank_const = shift_const - 215
def brt_corr(mean_brt, frame_read):
    print("CORR*********")
        #  Brightness Correction
    if mean_brt > BRT_THRESH:
        frame_read = np.int16(frame_read)
        frame_read = frame_read * (contrast / 127 + 1) - contrast + brightness
        frame_read = np.clip(frame_read, 0, 255)
        frame_read = np.uint8(frame_read)
    return frame_read

#shift_const를 리턴합니다.
def ret_shift_const():
    return shift_const

#영상 원근변환, 회전변환, BGR->BGR
def transform(img1, img2): #좌 우 레인 두 영상을 원근변환과 회전변환한 뒤, 이를 각 각 리턴합니다. 
    height, width, channel = img1.shape
    
    #왼쪽 위 왼쪽 아래 오른쪽 아래 오른쪽 위
    pts1 = np.float32([(0*width, 0*height),
                       (0*width, 1*height),
                       (1*width, 1*height),
                       (1*width, 0*height)])
    
    dest_width, dest_height = dest[:2]
    
    #실제 측정한 카메라 시야각을 바탕으로 pts1에서 pts2로 원근변환을 진행합니다.
    pts2 = np.float32([(0*dest_width, 0*dest_height),
                       (0.382*dest_width, 1*dest_height),
                       (0.628*dest_width, 1*dest_height),
                       (1*dest_width, 0*dest_height)])
    
    #원근변환 할 matrix를 구하는 함수입니다.
    matrix1 = cv2.getPerspectiveTransform(pts1, pts2)
    
    #구한 matrix를 바탕으로 원근변환을 진행합니다.
    p_img_left = cv2.warpPerspective(img1, matrix1, dest, flags=cv2.INTER_CUBIC+cv2.INTER_LINEAR)
    p_img_right = cv2.warpPerspective(img2, matrix1, dest, flags=cv2.INTER_CUBIC+cv2.INTER_LINEAR)
    
    #횐전변환 할 matrix를 구합니다. 실제 캠은 정면으로 부터 45도 떨어져 있으므로, 45도 정도 회전합니다.
    matrix2_left = cv2.getRotationMatrix2D((dest[0]/2, dest[1]/2), 43, 1)
    matrix2_right = cv2.getRotationMatrix2D((dest[0]/2, dest[1]/2), -43, 1)
    
    #구한 matrix를 바탕으로 회전변환을 진행합니다.
    r_img_left = cv2.warpAffine(p_img_left, matrix2_left, dest)
    r_img_right = cv2.warpAffine(p_img_right, matrix2_right, dest)
    
    return r_img_left, r_img_right

#감마 보정 + : 색 차이 뚜렷해짐 - : 색 비슷해짐
def gamma_correction(img, correction):
    img = img/255.0
    img = cv2.pow(img, correction)
    img = np.uint8(img*255)
    return img

#정면 영상 원근변환 / BGR -> BGR
def transform2(img_front):
    height, width = img_front.shape[:2]
    
    #roi설정을 위한 vertics, 위부터 차례대로 왼쪽 위, 왼쪽 아래, 오른쪽 아래, 오른쪽 위입니다. 아래 좌표는 실측한 데이터가 아니므로
    #실측한 데이터를 바탕으로 수정해야 합니다.
    vertics = np.array([[(int(0.4*width), int(0.5*height)),
                          (int(-0.35*width), int(1*height)),
                          (int(1.35*width), int(1*height)),
                          (int(0.6*width), int(0.5*height))]])
    
    #roi를 검출하기 위한 mask
    mask = np.zeros_like(img_front)
    cv2.fillPoly(mask, vertics, (255,255,255))
    #and연산을 통해 roi만을 이용
    masked = cv2.bitwise_and(img_front, mask)
    
    #원근 변환을 위한 points, 실측한 데이터를 이용하여 수정해야 함
    pts1 = np.float32([(0.4*width, 0.5*height),
                       (-0.35*width, 1*height),
                       (1.35*width, 1*height),
                       (0.6*width, 0.5*height)])
    pts2 = np.float32([(0*width, 0*height),
                       (0*width, 1*height),
                       (1*width, 1*height),
                       (1*width, 0*height)])
    
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    p_img = cv2.warpPerspective(masked, matrix, (width, height),flags=cv2.INTER_CUBIC+cv2.INTER_LINEAR)
    return p_img

#주차 영상 원근변환, 회전변환, BGR->BGR, 위 transform2 함수와 원리는 같습니다.
def parking_transform(img):
    height, width, channel = img.shape
    
    #왼쪽 위 왼쪽 아래 오른쪽 아래 오른쪽 위
    pts1 = np.float32([(0*width, 0*height),
                       (0*width, 1*height),
                       (1*width, 1*height),
                       (1*width, 0*height)])
    
    dest_width, dest_height = dest[:2]
    
    pts2 = np.float32([(0*dest_width, 0*dest_height),
                       (0.382*dest_width, 1*dest_height),
                       (0.628*dest_width, 1*dest_height),
                       (1*dest_width, 0*dest_height)])
    
    matrix1 = cv2.getPerspectiveTransform(pts1, pts2)
    p_img_parking = cv2.warpPerspective(img, matrix1, dest, flags=cv2.INTER_CUBIC+cv2.INTER_LINEAR)

    matrix2_parking = cv2.getRotationMatrix2D((dest[0]/2, dest[1]/2), 10, 1)
    
    r_img_parking = cv2.warpAffine(p_img_parking, matrix2_parking, dest)
    
    return r_img_parking

# 정지선을 검출하는 함수
def get_stop_line(img_bin):
    height, width = img_bin.shape[:2]
    
    #일정한 사각형 지역을 설정한다.
    left_high = (int(0.2*width), int(0.97*height))
    right_low = (int(0.8*width), int(1*height))
    Area = (right_low[0]-left_high[0]) * (right_low[1]-left_high[1])
    s_img = img_bin[left_high[1]:right_low[1], left_high[0]:right_low[0]]
    s_img = cv2.cvtColor(s_img, cv2.COLOR_BGR2GRAY)
    
    #사각형 지역 안에 일정 비율 이상 하얀 픽셀이 존재하면 정지선으로 판단한다.
    if(cv2.countNonZero(s_img) > (Area*0.5)):
        return True
    else:
        return False

# 주차선을 검출하는 함수, get_stop_line과 원리가 같습니다.
def get_parking_line(img_bin):
    height, width = img_bin.shape[:2]
    left_high = (int(0.3*width), int(0.02*height))
    right_low = (int(0.33*width), int(0.6*height))
    cv2.rectangle(img_bin, left_high, right_low, (0,255,255), 3)
    Area = (right_low[0]-left_high[0]) * (right_low[1]-left_high[1])
    s_img = img_bin[left_high[1]:right_low[1], left_high[0]:right_low[0]]
    s_img = cv2.cvtColor(s_img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Parking_line", img_bin)
    if(cv2.countNonZero(s_img) > (Area*0.8)):
        return True
    else:
        return False
    
#영상을 합침/ BGR -> BGR
def combine(img_left, img_right):
    
    #cv2.imshow("left", img_left)
    #도로 중간만큼 띄우는 공백
    blank = np.zeros((dest[1],blank_const,3), np.uint8)
    height, width = img_left.shape[:2]
    
    img_left_temp = img_left[0:height,0:int(0.9*width)]
    img_right_temp = img_right[0:height,int(0.1*width):width]
    
    #좌우로 영상 이어붙이기
    img_concat = cv2.hconcat([img_left_temp, blank])
    img_concat = cv2.hconcat([img_concat, img_right_temp])
    
    height, width = img_concat.shape[:2]
    
    #ROI 왼쪽 위, 왼쪽 아래, 오른쪽 아래, 오른쪽 위
    vertics = np.array([[(int(0.5*width-300), int(0*height)),
                         (int(0.5*width-300), int(1*height)),
                         (int(0.5*width+300), int(1*height)),
                         (int(0.5*width+300), int(0*height))]])
    
    mask = np.zeros_like(img_concat, np.uint8)
    cv2.fillPoly(mask, vertics, (255,255,255))
    img_concat = cv2.bitwise_and(img_concat, mask)
    
    return img_concat[int(0*height):int(1*height), int(0.5*width-300):int(0.5*width+300)]

# 영상 이진화, BGR->BGR
def detect(img, list = ['y', 'w']):
    combined_hsv = cv2.cvtColor(np.zeros_like(img), cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    for color in list:
        detected = detectcolor(img_hsv, color)
        combined_hsv = cv2.bitwise_or(combined_hsv, detected)
        
    combined_bgr = cv2.cvtColor(combined_hsv,cv2.COLOR_GRAY2BGR)
    #cv2.imshow("detect", combined_bgr)
    return combined_bgr

# color = b, r, w, y / 이미지 상에서 색을 찾아 리턴 / HSV->HSV
def detectcolor(img, color):
    if color == "w":
        (minRange, maxRange) = boundaries[4]
        mask = cv2.inRange(img, minRange, maxRange)
    elif color == "y":
        (minRange, maxRange) = boundaries[3]
        mask = cv2.inRange(img, minRange, maxRange)
    elif color == "b":
        (minRange, maxRange) = boundaries[2]
        mask = cv2.inRange(img, minRange, maxRange)
    elif color == "r":
        (minRange, maxRange) = boundaries[0]
        mask = cv2.inRange(img, minRange, maxRange)
        (minRange, maxRange) = boundaries[1]
        mask = mask + cv2.inRange(img, minRange, maxRange)
    else:
        print("In Image_util.py DetectColor - Wrong color Argument")
    return mask

def draw_points(img, x_points, y_points, color, thickness):
    try:
        for i in range(len(x_points)):
            if(x_points[i]!=None):
                cv2.line(img, (int(x_points[i]), int(y_points[i])), (int(x_points[i]), int(y_points[i])),
                         color, thickness)
    except:
            print("error2")

# 차선 검출 // BGR -> BGR
def lane_detect(b_img): 
    b_img = cv2.cvtColor(b_img, cv2.COLOR_BGR2GRAY)
    histogram = np.sum(b_img[int(b_img.shape[0]*(1/3)):, :], axis=0)
    midpoint = np.int(histogram.shape[0] / 2)
    ret_img = np.zeros_like(b_img)
                    
    left_x_max = np.argmax(histogram[:midpoint])
    right_x_max = np.argmax(histogram[midpoint:]) + midpoint

    window_height = np.int(b_img.shape[0]/n_windows)
    window_width = np.int(b_img.shape[1]/40)
    left_pos = 0
    
    left_lane_x = []
    left_lane_y = []
    right_lane_x = []
    right_lane_y = []
    lx = []
    ly = []
    
    #수직 히스토그램을 조사하여 이미지 왼쪽과 오른쪽 중 더 많은 픽셀이 있는 곳(라인)을 기준으로 나머지 라인은 다른 라인을 shift합니다.
    if(histogram[left_x_max] >= histogram[right_x_max]): #왼쪽 라인이 더 진한 경우
        current_left = left_x_max
        left_pos = left_x_max
       
        # 설정한 n_windows만큼 아래 과정을 반복합니다.
        for windows in range(n_windows):
            win_y_low = b_img.shape[0] - (windows+1) * window_height
            win_y_high = win_y_low + window_height
            left_x_low = current_left - window_width
            left_x_high = current_left + window_width
            
            # current_left를 기준으로 일정한 사각형을 설정하여 각 필셀의 x 좌표와 y 좌표를 추출합니다.
            cv2.rectangle(ret_img, (left_x_low, win_y_low), (left_x_high, win_y_high), (255, 255, 255), 2)
            
            left_x = np.array(b_img[win_y_low:win_y_high,left_x_low:left_x_high].nonzero()[1]) + left_x_low
            #left x가 더 크다면 right x는 left x를 const shift하여 옮깁니다.
            right_x = left_x + shift_const
            left_y = np.array(b_img[win_y_low:win_y_high,left_x_low:left_x_high].nonzero()[0]) + win_y_low
            right_y = np.array(b_img[win_y_low:win_y_high,left_x_low:left_x_high].nonzero()[0]) + win_y_low
            
            
            # If you found > minpix pixels, recenter next window on their mean position
            # 일정 픽셀이상 채워진 사각형(정상적인 레인)이라면 current_left를 현재 사각형 내부 픽셀들의 x값 평균으로 옮겨 다음 사각형의
            # 픽셀들을 조사합니다.
            if len(left_x) > min_pixel_num:
                current_left = np.int(np.mean(left_x))
            
            left_lane_x.append(left_x)
            left_lane_y.append(left_y)
            right_lane_x.append(right_x)
            right_lane_y.append(right_y)
            
    else: #오른쪽 라인이 더 진한경우, logic은 왼쪽 라인이 더 진한 경우와 같습니다.
        current_right = right_x_max
        left_pos = right_x_max - shift_const
        
        for windows in range(n_windows):
            win_y_low = b_img.shape[0] - (windows+1) * window_height
            win_y_high = win_y_low + window_height
            left_x_low = current_right - window_width
            left_x_high = current_right + window_width
            
            cv2.rectangle(ret_img, (left_x_low, win_y_low), (left_x_high, win_y_high), (255, 255, 255), 2)
            
            right_x = np.array(b_img[win_y_low:win_y_high,left_x_low:left_x_high].nonzero()[1]) + left_x_low
            left_x =  right_x - shift_const
            left_y = np.array(b_img[win_y_low:win_y_high,left_x_low:left_x_high].nonzero()[0]) + win_y_low
            right_y = np.array(b_img[win_y_low:win_y_high,left_x_low:left_x_high].nonzero()[0]) + win_y_low
            
            
            # If you found > minpix pixels, recenter next window on their mean position
            if len(right_x) > min_pixel_num:
                current_right = np.int(np.mean(right_x))
            
            left_lane_x.append(left_x)
            left_lane_y.append(left_y)
            right_lane_x.append(right_x)
            right_lane_y.append(right_y)
    
    lx = np.concatenate(left_lane_x)
    ly = np.concatenate(left_lane_y)
    rx = np.concatenate(right_lane_x)
    ry = np.concatenate(right_lane_y)
    ret_img = cv2.cvtColor(ret_img, cv2.COLOR_GRAY2BGR)
    
    position = ((midpoint-(left_pos))/shift_const)*2-1
    #To find shift_const
    #print(left_x_max, right_x_max, left_x_max+right_x_max ,left_right_sum)
    
    #추출한 픽셀들의 x값들과 y값들을 바탕으로 np.polyfit 함수를 이용하여 회귀하는 과정입니다.
    try:
        #왼쪽 라인과 오른쪽 라인을 각각 추출합니다.
        left_fit = np.polyfit(ly, lx, poly_order) # ly lx 순서 고정
        right_fit = np.polyfit(ry, rx, poly_order)
        line_left = np.poly1d(left_fit)
        line_right = np.poly1d(right_fit)
        x = np.linspace(0, b_img.shape[0], b_img.shape[0])
        y = np.round(line_left(x))
        
        #추출한 라인을 바탕으로 선을 그립니다.
        draw_points(ret_img, y, x, [0,255,0], thickness=2) # y x 순서 고정
        y = np.round(line_right(x))
        draw_points(ret_img, y, x, [0,255,0], thickness=2)
        
        #추출한 라인의 기울기를 리턴합니다.(차량이 기울어진 정도)
        degree = -degrees(atan(line_left[1]))
    
    #추출한 픽셀들을 바탕으로 회귀를 진행했을 때, 실패한 경우입니다.
    except:
        ret_img = cv2.line(ret_img, (int(ret_img.shape[1]*0.3), 0), (int(ret_img.shape[1]*0.3), ret_img.shape[0]), (0,255, 0), 5)
        ret_img = cv2.line(ret_img, (int(ret_img.shape[1]*0.7), 0), (int(ret_img.shape[1]*0.7), ret_img.shape[0]), (0,255, 0), 5)
        
        #이때는 차량이 정면을 보고있다고 가정하고, 차량을 직진시킵니다.
        degree = 0
        position = 0

    str_1 = "position: "+ str(position)
    str_2 = "degree: "+ str(degree)
    cv2.putText(ret_img, str_1, (200, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
    cv2.putText(ret_img, str_2, (200, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
    return position, degree, ret_img

if __name__=='__main__':
    
    '''
    video1="C:\photo\cam_left_1.avi"
    video2="C:\photo\cam_right_1.avi"    
    cap1 = cv2.VideoCapture(video1)
    cap2 = cv2.VideoCapture(video2)
    '''
    '''
    video1 = "C:\photo\cam_front_1.avi"
    cap1 = cv2.VideoCapture(video1)
    '''
    try:
        print('카메라를 구동합니다.')
        cap1 = cv2.VideoCapture(1)
        cap2 = cv2.VideoCapture(0)
    except:
        print('카메라 구동 실패')
    
    while True:
        ret1, img1 = cap1.read()
        ret2, img2 = cap2.read()
        
#        if not (ret1 and ret2)
        if not ret1:
            print("비디오 끝")
            break
        '''
        img_front = transform2(img1)
        img_bin = detect(img_front)
        cv2.imshow("front", img1)
        cv2.imshow("trans", img_front)
        cv2.imshow("detect", img_bin)
        get_stop_line(img_bin)
        '''
        img_left, img_right = transform(img1, img2)
        img_concat = combine(img_left, img_right)
        cv2.imshow("concat", img_concat)
        img_bin = detect(img_concat)
        lane_detect(img_bin)
        
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break
    
    cap1.release()
    #cap2.release()
    cv2.destroyAllWindows()
