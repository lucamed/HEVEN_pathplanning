# Solution using OpenCV

import cv2
 
# Read image
img = cv2.imread('../cat.jpg')
 
# Get dimensions of image
dimensions = img.shape
 
# Height and width in image
height = img.shape[0]
width = img.shape[1]

# Find center of the image
center_H = int(height/2)
center_W = int(width/2)

# Crop 500x500 from the center
cropped = img[center_H-250:center_H+250, center_W-250:center_W+250]

# Save a new image file
cv2.imwrite("crop.jpg", cropped)
