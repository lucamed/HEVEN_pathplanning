import cv2
import numpy as np

#이미지열기
img = cv2.imread("YW1.jpg")

# 이미지 흑백으로 만들고 블러처리
img_gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
img_gray_blur=cv2.GaussianBlur(img_gray,(5,5),0)
# canny edge
img_gray_blur_canny=cv2.Canny(img_gray_blur,50,200)
#검게 만들기, 관심영역 잡고 해당 edge들만 그리기
mask=np.zeros_like(img_gray_blur_canny)
channel_count=img.shape[2]
ignore_mask_color=(255,)*channel_count
imshape=img_gray_blur_canny.shape
vertices=np.array([[(100,imshape[0]),(450,320),(550,320),(imshape[1]-20,imshape[0])]], dtype=np.int32)
cv2.fillPoly(mask,vertices,ignore_mask_color)
masked_image=cv2.bitwise_and(img_gray_blur_canny,mask)

cv2.imshow("masked_image", masked_image)
cv2.waitKey()


# lines
lines = cv2.HoughLinesP(
    masked_image,
    rho=1.0,
    theta=np.pi/180,
    threshold=20,
    minLineLength=30,
    maxLineGap=10
)

# 선그리기
line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
line_color = [0, 255, 0]
line_color2 = [255, 0, 0]
line_color3 = [0, 0, 255]
line_thickness = 5

for line in lines:
    for x1, y1, x2, y2 in line:
        if x1<480:
            cv2.line(line_img, (x1, y1), (x2, y2), line_color, line_thickness)
        else:
            cv2.line(line_img, (x1, y1), (x2, y2), line_color2, line_thickness)

cv2.imshow("lineimage", line_img)
cv2.waitKey()

#덮어쓰기
overlay = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
cv2.imshow("Overlay", overlay)
cv2.waitKey()
cv2.destroyAllWindows()


#가운데선 긋는 법과 오른쪽선 길게 그리는 법을 모르겠습니다.
# 그리고 그냥 흑백화시켜서 가운데영역 선인식시켰는데 노란선만 따로 하얀선만 따로 인식시키는것을 모르겟습니다.