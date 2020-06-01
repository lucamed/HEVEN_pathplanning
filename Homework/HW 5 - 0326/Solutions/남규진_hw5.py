import matplotlib.pylab as plt
import cv2
import numpy as np
# youtube Programming Knowledge 채널의 https://www.youtube.com/watch?v=yvfI4p6Wyvk 이 영상을 참고하여 만들었습니다.
# 관심영역의 이미지를 추출하는 함수입니다.
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
# 그려진 실선을 원하는 부분까지만 추출하는 함수입니다.
def region_of_interest_lines(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = (255, 255, 255)
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
# 실선을 그리는 함수입니다.
def drow_the_lines(img, lines):
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 < 400 or x2 < 400:
                cv2.line(blank_image, (x1, y1), (x2, y2), (255, 0, 0), thickness=5)
            if x1 > 560 or x2 > 560:
                    cv2.line(blank_image, (x1, y1), (x2, y2), (0, 0, 255), thickness=5)



    line_region = [(30, 540), (450, 330), (540, 330), (930, 540)]
    blank_image = region_of_interest_lines(blank_image, np.array([line_region], np.int32), )
    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img
#입력받은 이미지에 차선을 그려주는 함수입니다.
def process(image):
    #image = cv2.imread('WW1.jpg')
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_blur = cv2.GaussianBlur(image, (5, 5), 0) #가우시안 블러 사용하였습니다
    image_blur = cv2.GaussianBlur(image, (5, 5), 0)
    #print(image.shape)
    height = image.shape[0]
    width = image.shape[1]
    region_of_interest_vertices = [
        (0, height),
        (width/2, height/2),
        (width, height)
    ]
    gray_image = cv2.cvtColor(image_blur, cv2.COLOR_RGB2GRAY)
    canny_image = cv2.Canny(gray_image, 100, 150)
    cropped_image = region_of_interest(canny_image,
                    np.array([region_of_interest_vertices], np.int32),)
    lines = cv2.HoughLinesP(cropped_image,
                            rho=2,
                            theta=np.pi/180,
                            threshold=50,
                            lines=np.array([]),
                            minLineLength=40,
                            maxLineGap=100)
    image_with_lines = drow_the_lines(image, lines)
    return image_with_lines
#비디오파일의 프레임 이미지를 얻습니다.
cap = cv2.VideoCapture('YW.mp4')
#각 프레임에 대하여 process 함수를 적용합니다.
while(cap.isOpened()):
    ret, frame = cap.read()
    frame = process(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): #q를 누르면 창을 닫습니다.
        break

cap.release()
cv2.destroyAllWindows()


#plt.imshow(image_with_lines)
#plt.show()