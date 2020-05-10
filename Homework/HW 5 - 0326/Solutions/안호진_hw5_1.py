import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import random

cap = cv2.VideoCapture('YW.mp4')
fit_result, l_fit_result, r_fit_result, L_lane, R_lane = [], [], [], [], []

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def canny(img, low, high):
    return cv2.Canny(img, low, high)

def gaussian_blur(img, size):
    return cv2.GaussianBlur(img, (size, size), 0)

def region_of_interest(img, vertices):
    
    mask = np.zeros_like(img)   
    
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    cv2.fillPoly(mask, vertices, ignore_mask_color)

    roi_image = cv2.bitwise_and(img, mask)
    return roi_image

def draw_lines(img, lines):
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), [255, 0, 0], 2)

def hough_lines(img, rho, theta, threshold, len_min, gap_max):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), len_min, gap_max)
    line_arr = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    return lines

def weighted_img(img, initial_img, a=0.8, b=1., c=0.):
    return cv2.addWeighted(initial_img, a, img, b, c)

def Collect_points(lines):
    interp = lines.reshape(lines.shape[0]*2,2)
    for line in lines:
        if np.abs(line[3]-line[1]) > 5:
            tmp = np.abs(line[3]-line[1])
            a = line[0] ; b = line[1] ; c = line[2] ; d = line[3]
            slope = (line[2]-line[0])/(line[3]-line[1]) 
            for m in range(0,tmp,5):
                if slope>0:
                    new_point = np.array([[int(a+m*slope),int(b+m)]])
                    interp = np.concatenate((interp,new_point),axis = 0)
                elif slope<0:
                    new_point = np.array([[int(a-m*slope),int(b-m)]])
                    interp = np.concatenate((interp,new_point),axis = 0)                
    return interp

def get_random_samples(lines):
    one = random.choice(lines)
    two = random.choice(lines)
    if(two[0]==one[0]):
        while two[0]==one[0]:
            two = random.choice(lines)
    one, two = one.reshape(1,2), two.reshape(1,2)
    three = np.concatenate((one,two),axis=1)
    three = three.squeeze()
    return three

def compute_model_parameter(line):
    m = (line[3] - line[1])/(line[2] - line[0])
    n = line[1] - m*line[0]
    a, b, c = m, -1, n
    par = np.array([a,b,c])
    return par

def compute_distance(par, point):  
    return np.abs(par[0]*point[:,0]+par[1]*point[:,1]+par[2])/np.sqrt(par[0]**2+par[1]**2)

def model_verification(par, lines):
    distance = compute_distance(par,lines) 
    sum_dist = distance.sum(axis=0)
    avg_dist = sum_dist/len(lines)
    return avg_dist

def draw_extrapolate_line(img, par,color=(0,0,255), thickness = 2):
    x1, y1 = int(-par[1]/par[0]*img.shape[0]-par[2]/par[0]), int(img.shape[0])
    x2, y2 = int(-par[1]/par[0]*(img.shape[0]/2+100)-par[2]/par[0]), int(img.shape[0]/2+100)
    cv2.line(img, (x1 , y1), (x2, y2), color, thickness)
    return img

def get_fitline(img, f_lines):
    rows,cols = img.shape[:2]
    output = cv2.fitLine(f_lines,cv2.DIST_L2,0, 0.01, 0.01)
    vx, vy, x, y = output[0], output[1], output[2], output[3]
    x1, y1 = int(((img.shape[0]-1)-y)/vy*vx + x) , img.shape[0]-1
    x2, y2 = int(((img.shape[0]/2+100)-y)/vy*vx + x) , int(img.shape[0]/2+100)
    result = [x1,y1,x2,y2]
    return result

def draw_fitline(img, result_l,result_r, color=(255,0,255), thickness = 10):
    lane = np.zeros_like(img)
    cv2.line(lane, (int(result_l[0]) , int(result_l[1])), (int(result_l[2]), int(result_l[3])), color, thickness)
    cv2.line(lane, (int(result_r[0]) , int(result_r[1])), (int(result_r[2]), int(result_r[3])), color, thickness)
    final = weighted_img(lane, img, 1,0.5)  
    return final

def erase_outliers(par, lines):
    distance = compute_distance(par,lines)
    filtered_lines = lines[distance<13,:]
    return filtered_lines

def smoothing(lines, pre_frame):
    lines = np.squeeze(lines)
    avg_line = np.array([0,0,0,0])
    
    for ii,line in enumerate(reversed(lines)):
        if ii == pre_frame:
            break
        avg_line += line
    avg_line = avg_line / pre_frame

    return avg_line

def ransac_line_fitting(img, lines, min=100):
    global fit_result, l_fit_result, r_fit_result
    best_line = np.array([0,0,0])
    if(len(lines)!=0):                
        for i in range(30):           
            sample = get_random_samples(lines)
            parameter = compute_model_parameter(sample)
            cost = model_verification(parameter, lines)                        
            if cost < min:
                min = cost
                best_line = parameter
            if min < 3: break
        filtered_lines = erase_outliers(best_line, lines)
        fit_result = get_fitline(img, filtered_lines)
    else:
        if (fit_result[3]-fit_result[1])/(fit_result[2]-fit_result[0]) < 0:
            l_fit_result = fit_result
            return l_fit_result
        else:
            r_fit_result = fit_result
            return r_fit_result

    if (fit_result[3]-fit_result[1])/(fit_result[2]-fit_result[0]) < 0:
        l_fit_result = fit_result
        return l_fit_result
    else:
        r_fit_result = fit_result
        return r_fit_result

def detect_lanes_img(img):

    height, width = img.shape[:2]

    vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32)
    ROI_img = region_of_interest(img, vertices)
    
    blur_img = gaussian_blur(ROI_img, 3)
        
    canny_img = canny(blur_img, 70, 210)
    vertices2 = np.array([[(52,height),(width/2-43, height/2+62), (width/2+43, height/2+62), (width-52,height)]], dtype=np.int32)
    canny_img = region_of_interest(canny_img, vertices2)

    line_arr = hough_lines(canny_img, 1, 1 * np.pi/180, 30, 10, 20)

    line_arr = np.squeeze(line_arr)
    slope_degree = (np.arctan2(line_arr[:,1] - line_arr[:,3], line_arr[:,0] - line_arr[:,2]) * 180) / np.pi

    line_arr = line_arr[np.abs(slope_degree)<160]
    slope_degree = slope_degree[np.abs(slope_degree)<160]
    line_arr = line_arr[np.abs(slope_degree)>95]
    slope_degree = slope_degree[np.abs(slope_degree)>95]
    L_lines, R_lines = line_arr[(slope_degree>0),:], line_arr[(slope_degree<0),:]
    
    L_interp = Collect_points(L_lines)
    R_interp = Collect_points(R_lines)

    left_fit_line = ransac_line_fitting(img, L_interp)
    right_fit_line = ransac_line_fitting(img, R_interp)

    L_lane.append(left_fit_line), R_lane.append(right_fit_line)

    if len(L_lane) > 10:
        left_fit_line = smoothing(L_lane, 10)    
    if len(R_lane) > 10:
        right_fit_line = smoothing(R_lane, 10)
    final = draw_fitline(img, left_fit_line, right_fit_line)

    return final

while(cap.isOpened()):
    ret, frame = cap.read()
    if frame.shape[0] !=540:
        frame = cv2.resize(frame, None, fx=3/4, fy=3/4, interpolation=cv2.INTER_AREA) 
    result = detect_lanes_img(frame)

    cv2.imshow('result',result)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

cap.release()
cv2.destroyAllWindows()
