import cv2
import numpy
import random

# 사진 불러오기
background = cv2.imread('road.jpg', cv2.IMREAD_COLOR)
sign = cv2.imread('cropped_sign.jpg', cv2.IMREAD_COLOR)

# 합성할 구역 뽑아내기
bg_rows, bg_cols, _ = background.shape
rows, cols, channels = sign.shape
for i in range(1, 101):
    ran_rows = random.randrange(bg_rows - rows)
    ran_cols = random.randrange(bg_cols - cols)
    roi = background[ran_rows:ran_rows + rows, ran_cols:ran_cols + cols]  # 좌표위치를 바꿔야 함.

    # mask만들기
    gray_sign = cv2.cvtColor(sign, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_sign, 240, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # roi와 표지판 합성하기
    img1 = cv2.bitwise_and(roi, roi, mask=mask)
    img2 = cv2.bitwise_and(sign, sign, mask=mask_inv)
    dst = cv2.add(img1, img2)

    # 원래 그림에 붙이기
    copy = background.copy()
    copy[ran_rows:ran_rows + rows, ran_cols:ran_cols + cols] = dst
    #파일저장하기
    name = 'data/road_%03d.jpg' %i
    print(name)
    cv2.imwrite(name, copy)
