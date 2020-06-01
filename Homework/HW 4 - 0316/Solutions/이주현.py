
'''
The main
problem of this HW is to detect both lines in a lane and its center line.

1. Open the given images.
2. There are several ways to solve this. You can google and study about lane detection. 
	HSV colors, HoughlinesP, CannyEdge and GaussianBlur are some of the functions you might need.
	Usage of OpenCV is more than recommended.

3. Draw the left side line as RED and the right side BLUE. Also, find the middle point (desired path) and draw a line in GREEN
4. Use addWeighted to add all masks on the original image.
5. The program should work for finding the lanes in at least YW1.jpg and YW2.jpg
	WW3.jpg is extra question, if you solve for it... I'll be happy.

Check the attached example [EX] images, it will be helpful in understanding the question.
'''

import cv2
import matplotlib.pylab as plt
import numpy as np

def region_of_interest(img, vertices):              #관심영역
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_the_lines_red(or_img, img, lines):         #빨간선 긋는 함수
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(blank_image, (x1,y1), (x2,y2), (255,0,0), thickness=5)

    or_img = cv2.addWeighted(or_img, 0.8, blank_image, 1, 0.0)
    return or_img
        
def draw_the_lines_blue(or_img, img, lines):        #파란선 긋는 함수
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(blank_image, (x1,y1), (x2,y2), (0,0,255), thickness=5)

    or_img = cv2.addWeighted(or_img, 0.8, blank_image, 1, 0.0)
    return or_img
            


YW1 = cv2.imread("C:/Users/user/Desktop/YW1.jpg", cv2.IMREAD_COLOR)
YW2 = cv2.imread("C:/Users/user/Desktop/YW2.jpg", cv2.IMREAD_COLOR) #이미지 불러오기

YW1 = cv2.cvtColor(YW1, cv2.COLOR_BGR2RGB)

print(YW1.shape)
height = YW1.shape[0]
width = YW1.shape[1]

region_of_interest_vertices = [         #관심영역1: 좌측 lane
    (0,height),
    (width/2, height/2),
    (width/2, height)
]




gray_image = cv2.cvtColor(YW1, cv2.COLOR_RGB2GRAY)

gray_image_blur = cv2.GaussianBlur(gray_image, (5,5), 0)

canny_image = cv2.Canny(gray_image_blur, 100, 200)




cropped_image = region_of_interest(canny_image,
                np.array([region_of_interest_vertices], np.int32))

lines = cv2.HoughLinesP(cropped_image,
                        rho=6,
                        theta=np.pi/60,
                        threshold=160,
                        lines=np.array([]),
                        minLineLength=40,
                        maxLineGap=25)

image_with_lines = draw_the_lines_red(YW1, cropped_image, lines)
#image_with_lines = cv2.addWeighted(canny_image, 0.8, image_only_lines, 1, 0.0)

region_of_interest_vertices = [         #관심영역2: 우측 lane
    (width/2, height),
    (width/2, height/2),
    (width, height)
]

cropped_image = region_of_interest(canny_image,
                np.array([region_of_interest_vertices], np.int32))

lines = cv2.HoughLinesP(cropped_image,
                        rho=6,
                        theta=np.pi/60,
                        threshold=160,
                        lines=np.array([]),
                        minLineLength=40,
                        maxLineGap=25)


image_with_lines = draw_the_lines_blue(image_with_lines, cropped_image, lines)


#plt.imshow(cropped_image)
plt.imshow(image_with_lines)
plt.show()


#middle point를 찾아서 라인 그리는 것은 완성하지 못했습니다 죄송합니다..
