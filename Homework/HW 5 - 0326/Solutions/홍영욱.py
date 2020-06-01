
import cv2
import numpy as np


def grayscale(img):  # 흑백이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def canny(img, low_threshold, high_threshold):  # Canny 알고리즘
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):  # 가우시안 필터
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  # ROI 셋팅

    mask = np.zeros_like(img)  # img 크기와 같은 마스크를 만듬.

    if len(img.shape) > 2:  # Color 이미지(3채널)라면 :
        color = color3
    else:  # 흑백 이미지(1채널)라면 :
        color = color1

    # vertices의 점으로 이뤄진 도형을 color로 채움
    cv2.fillPoly(mask, vertices, color)

    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image


def draw_linesr(img, lines, color=[0, 0, 255], thickness=2):  # 빨강선 그리기
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def draw_linesl(img, lines, color=[255, 0, 0], thickness=2):  # 파랑선 그리기
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_linesr(img, rho, theta, threshold, min_line_len, max_line_gap):  # 왼쪽 허프 변환
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_linesr(line_img, lines)

    return line_img

def hough_linesl(img, rho, theta, threshold, min_line_len, max_line_gap):  # 오른쪽 허프 변환
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_linesl(line_img, lines)

    return line_img

def weighted_img(img, initial_img, α=1, β=1., λ=0.):  # 두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, α, img, β, λ)


cap = cv2.VideoCapture('YW.mp4')

while(cap.isOpened()):

    ret, image = cap.read()

    height, width = image.shape[:2]
    
    gray_img = grayscale(image)  # 흑백이미지로 변환

    blur_img = gaussian_blur(gray_img, 3)  # Blur 효과주기

    canny_img = canny(blur_img, 70, 210)  # Canny edge 알고리즘

    verticesleft = np.array(
    [[(50, height), (width / 2, height / 2 + 40), (width / 2, height / 2 + 40), (width/2, height)]],
    dtype=np.int32)
    ROI_imgleft = region_of_interest(canny_img, verticesleft)  # 왼쪽 interest한 부분 ROI 설정하기

    hough_imgr = hough_linesr(ROI_imgleft, 1, 1 * np.pi / 180, 30, 10, 20)  # 허프 변환


    verticesright = np.array([[(width / 2+50, height), (width / 2+50, height / 2 + 40), (width / 2, height / 2 + 40), (width, height)]],dtype=np.int32)
    ROI_imgright = region_of_interest(canny_img, verticesright)  # 오른쪽 interest한 부분 ROI 설정하기
    hough_imgl = hough_linesl(ROI_imgright, 1, 1 * np.pi / 180, 30, 10, 20)
    results = weighted_img(hough_imgl, hough_imgr) # 두 선 합치기
    result = weighted_img(results,image) # 원본 이미지에 선 합치기

    cv2.imshow('result', result)  # 결과 이미지 출력

    if cv2.waitKey(10000) & 0xFF == ord('q'):
        break

# Release
cap.release()
cv2.destroyAllWindows()
