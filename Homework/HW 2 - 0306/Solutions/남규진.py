import cv2
image1 = cv2.imread("cat.jpg",cv2.IMREAD_COLOR)
[a,b,c]=image1.shape
image2 = image1[a//2-250:a//2+250, b//2-250:b//2+250]
cv2.imshow("center", image2)
cv2.imwrite("center.jpg",image2)
cv2.waitKey(0)
cv2.destroyAllWindows()