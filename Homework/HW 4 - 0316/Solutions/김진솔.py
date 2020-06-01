import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

image = mpimg.imread('YW1.jpg')
def region_of_interest(img, vertices): #원하는 부분만 보는 함수 정의
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=3): #선그리기
    img = np.copy(img)
    line_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), color, thickness)
    img = cv2.addWeighted(img, 0.8, line_image, 1.0, 0.0)
    return img


height = image.shape[0]
width = image.shape[1]
region_of_interest_vertices = [
    (0, height),
    (width* 3/7, height*3/5),(width* 4/7, height*3/5),
    (width, height),
]

gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
cannyed_image = cv2.Canny(gray_image, 100, 200)


cropped_image = region_of_interest(
    cannyed_image,
    np.array([region_of_interest_vertices], np.int32)
)
plt.figure()
plt.imshow(cropped_image)
plt.show()

lines = cv2.HoughLinesP(
    cropped_image,
    rho=6,
    theta=np.pi / 60,
    threshold=160,
    lines=np.array([]),
    minLineLength=40,
    maxLineGap=25
)
print(lines)


real_line_image = draw_lines(image, lines)
plt.figure()
plt.imshow(real_line_image)
plt.show()

