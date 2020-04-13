#hw2

import cv2

old = cv2.imread("cat.jpg", cv2.IMREAD_COLOR)
[i,j,k]=old.shape
new = old.copy()
new = old[i//2-250:i//2+250, j//2-250:j//2+250]
cv2.imshow("old", old)
cv2.imshow("new", new)
cv2.waitKey(0)
cv2.destroyAllWindows()

