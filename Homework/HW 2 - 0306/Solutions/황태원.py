import cv2
image = cv2.imread("cat.jpg")
[i,j,k]=image.shape
a=i//2;b=j//2;
cut = image.copy()
cut = image[a-250:a+250, b-250:b+250]
cv2.imshow("image", image)
cv2.imshow("cut", cut)
cv2.waitKey(0)
cv2.destroyAllWindows()
