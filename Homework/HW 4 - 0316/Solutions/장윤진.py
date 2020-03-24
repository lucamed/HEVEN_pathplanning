import matplotlib.pylab as plt
import cv2
import numpy as np

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

xp1 = []
xp2 = []
yp1 = []
yp2 = []
xn1 = []
xn2 = []
yn1 = []
yn2 = []
xx1 = []
xx2 = []
yy1 = []
yy2 = []

def draw_the_lines(img, lines):
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            if slope > 0:
                xp1.append(x1)
                xp2.append(x2)
                yp1.append(y1)
                yp2.append(y2)
                cv2.line(blank_image, (x1,y1), (x2,y2), (0, 0, 255), thickness=10)
            else:
                xn1.append(x1)
                xn2.append(x2)
                yn1.append(y1)
                yn2.append(y2)
                cv2.line(blank_image, (x1, y1), (x2, y2), (255, 0, 0), thickness=10)
    cv2.line(blank_image, (int((xp1[0] + xn2[0])/2), int((yp1[0] + yn2[0])/2)),(int((xp2[0] + xn1[0])/2), int((yp2[0] + yn1[0])/2)), (0, 255, 0), thickness=10)

    img = cv2.addWeighted(img, 0.5, blank_image, 1, 0.0)
    return img

image = cv2.imread('data/YW1.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

height = image.shape[0]
width = image.shape[1]
region_of_interest_vertices = [
    (0, height),
    (width/2, height/2 + 40),
    (width, height)
]
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
canny_image = cv2.Canny(gray_image, 100, 200)
cropped_image = region_of_interest(canny_image,
                np.array([region_of_interest_vertices], np.int32),)
lines = cv2.HoughLinesP(cropped_image,
                        rho=3,
                        theta=np.pi/180,
                        threshold=160,
                        lines=np.array([]),
                        minLineLength=40,
                        maxLineGap=150)
image_with_lines = draw_the_lines(image, lines)
plt.imshow(image_with_lines)
plt.show()