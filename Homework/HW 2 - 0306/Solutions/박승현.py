import cv2

img=cv2.imread("cat.jpg")
(x,y)=img.shape
cropimage=img[x//2-250:x//2+250, y//2-250:y//2+250]
cv2.imshow("img", img)
cv2.waitKey(0)
cv.destroyAllWindows()
