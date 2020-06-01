'''
이지아 HW5
Lane detection for a video

1. Open the given videos.
2. There are several ways to solve this. You can google and study about lane detection. 
	HSV colors, HoughlinesP, CannyEdge and GaussianBlur are some of the functions you might need.
	Usage of OpenCV is more than recommended.

3. Draw the left side line as RED and the right side BLUE. Also, find the middle point (desired path) and draw a line in GREEN
4. Use addWeighted to add all masks on the original image.
5. The program should work for finding the lanes in at least YW.mp4 and YW.mp4
'''

# Import the required libraries 
import matplotlib.pyplot as plt
import cv2
import numpy as np 

def HSV_color(image):
	hsv_frame = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            
        # Yellow
	lowerYellow = np.array([22,90,20])
	upperYellow = np.array([255, 255, 255])
	yellowMask = cv2.inRange(hsv_frame, lowerYellow, upperYellow)
           
        # White
	lowerWhite = np.array([0, 0, 200])
	upperWhite = np.array([255, 20, 255])
	whiteMask = cv2.inRange(hsv_frame, lowerWhite, upperWhite)

        # Combine the two masks
	mask = cv2.bitwise_or(whiteMask, yellowMask)
	masked_image = cv2.bitwise_and(image, image, mask = mask)
	return masked_image

def canny_edge(image): 
	
	# Convert image color to grayscale 
	gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) 
	
	# Reduce noise from the image 
	blur = cv2.GaussianBlur(gray_image, (5, 5), 0) 
	canny = cv2.Canny(blur, 50, 150) 
	return canny 

def ROI(image):
	height = image.shape[0] 
	polygons = np.array([ 
		[(200, height), (800, height), (550, 270)] 
		]) 
	mask = np.zeros_like(image) 
	
	# Filling in polygons
	cv2.fillPoly(mask, polygons, 255) 
	
	# Bitwise operation between canny image and mask image 
	and_image = cv2.bitwise_and(image, mask) 
	return and_image 

def create_coordinates(image, line_parameters): 
	try:
		slope, intercept = line_parameters
	except TypeError:
		slope, intercept = 0.000000001,0
	y1 = image.shape[0] 
	y2 = int(y1/2) 
	x1 = int((y1 - intercept) / slope) 
	x2 = int((y2 - intercept) / slope) 
	return np.array([x1, y1, x2, y2]) 

def average_slope(image, lines): 
	left_fit = [] 
	right_fit = [] 
	for line in lines: 
		x1, y1, x2, y2 = line.reshape(4) #value error: not enough values to unpack (expected 4, got 1)
		parameters = np.polyfit((x1, x2), (y1, y2), 1) 
		slope = parameters[0] 
		intercept = parameters[1] 
		if slope < 0: 
			left_fit.append((slope, intercept)) 
		else: 
			right_fit.append((slope, intercept)) 
			
	left_fit_average = np.average(left_fit, axis = 0) 
	right_fit_average = np.average(right_fit, axis = 0) 
	left_line = create_coordinates(image, left_fit_average) 
	right_line = create_coordinates(image, right_fit_average) 
	return np.array([left_line, right_line]) 

def highlight_lines(image, lines):
	copy_image = np.copy(image)
	line_image = np.zeros_like(image) 
	for line in lines:  
		for x1, y1, x2, y2 in lines:
			cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), thickness = 10) 
	line_image = cv2.addWeighted(copy_image, 0.8, line_image, 1, 0.0)
	return line_image

# Path of video
cap = cv2.VideoCapture("YW.mp4") 
while(cap.isOpened()): 
	ret, frame = cap.read()
	masked_image = HSV_color(frame)
	canny_image = canny_edge(masked_image) 
	cropped_image = ROI(canny_image) 
	lines = cv2.HoughLinesP(cropped_image, rho = 2, theta = np.pi/180, threshold = 100, 
				lines = np.array([]), minLineLength = 30, maxLineGap = 10) 
	averaged_lines = average_slope(frame, lines) 
	line_image = highlight_lines(frame, lines) 
	result_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1) 
	cv2.imshow("results", result_image) 
    
	if cv2.waitKey(0) & 0xFF == ord('q'):
		break

# release the capture and close windows 
cap.release() 

cv2.destroyAllWindows()
