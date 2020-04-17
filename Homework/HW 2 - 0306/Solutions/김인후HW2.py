import cv2
ori= cv2.imread('cat.jpg', cv2.IMREAD_COLOR)

[a,b,c]=ori.shape
[d,e,f]=[a//2,b//2,c]

fixed = ori.copy()
fixed = ori[d-250:d+250, e-250:e+250]
cv2.imwrite("cropped.jpg",fixed)
cv2.imshow("cat", ori)
cv2.imshow("cropped",fixed)
cv2.waitKey(0)
cv2.destroyAllWindows()
