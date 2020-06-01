import cv2

src=cv2.imread("cat.jpg", cv2.IMREAD_COLOR)

dst = src.copy()
[i,j,k]=src.shape

dst = src[i//2-250:i//2+250, j//2-250:j//2+250]

cv2.imwrite("cat2.jpg",dst)
cv2.imshow("src",src)
cv2.imshow("dst",dst)

cv2.waitKey(0)
cv2.destryAllWindows()

