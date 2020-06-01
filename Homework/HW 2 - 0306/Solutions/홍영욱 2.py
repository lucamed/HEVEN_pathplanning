import cv2
import numpy as np
import math

img = cv2.imread('cat.jpg')
cv2.imshow('original', img)

height, width = img.shape[:2]
e=round(height/2)
f=round(width/2)


a=e-250
b=e+250
c=f-250
d=f+250
print(a,b,c,d)

subimg = img[a:b, c:d]
cv2.imshow('cutting', subimg)
cv2.imwrite('center.jpg',subimg)

