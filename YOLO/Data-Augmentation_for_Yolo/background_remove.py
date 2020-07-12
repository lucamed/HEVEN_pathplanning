# Prevent white road sign from being erased
import cv2
import numpy as np

# img = cv2.cvtColor(cv2.imread('./2.png'),
#                    cv2.COLOR_BGR2RGB) ## openCV works with the BGR order
img = cv2.imread('./2.png')
lower_white = np.array([220, 220, 220], dtype=np.uint8)
upper_white = np.array([255, 255, 255], dtype=np.uint8)
mask = cv2.inRange(img, lower_white, upper_white)  # could also use threshold
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))  # erase the white arrows in the resulting mask
mask = cv2.bitwise_not(mask)  # invert mask

# load background (could be an image too)
bk = np.full(img.shape, 255, dtype=np.uint8)  # white bk

# get masked foreground
fg_masked = cv2.bitwise_and(img, img, mask=mask)

# get masked background, mask must be inverted
mask = cv2.bitwise_not(mask)
bk_masked = cv2.bitwise_and(bk, bk, mask=mask)

# combine masked foreground and masked background
final = cv2.bitwise_or(fg_masked, bk_masked)
mask = cv2.bitwise_not(mask)  # revert mask to original
result = cv2.bitwise_and(final, final, mask=mask)

cv2.imshow("white arrow sign", result)
cv2.imwrite("white arrow sign.png", result)
cv2.waitKey(0)
cv2.destroyAllWindows()