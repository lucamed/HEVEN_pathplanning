import cv2
import numpy as np
from util import make_binary, smoothing, draw_points, get_color

'''
#################### PATH PLAN TEAM ####################
## ABOUT
- 차선을 인식해서 왼쪽차선, 오른쪽차선, 정지선의 위치를 반환해주는 코드
## INPUT & OUTPUT
- input: 카메라 원
- output: 각 미션 별 packet
'''
class Line:
    def __init__(self,current_line = None,curve = 0, detect = False):
        self.current_fit = [np.array([False])]
        self.prevx = []
        self.allx = None
        self.ally = None
        self.curve = curve
        self.detect = detect
        # polynomial coefficients for the most recent fit


## Lane_Detection.py
class Lane_Detection: #Lane_Detction 클래스 생성후, original img 변경
    def __init__(self, poly_order = 2, n_windows = 10 , windows_width = 20 , display =(800,600), min_pixel_num = 30):  # 초기화
        self.left = Line()
        self.right = Line()
        self.poly_order = poly_order
        self.n_windows = n_windows
        self.windows_width = windows_width
        self.min_pixel_num = min_pixel_num
        self.display = display
        self.floor_color_buf = []
        
    def run(self,img):
        self.binary_img = make_binary(img,self.display)
        cv2.imshow('bin', self.binary_img)
        #self.map = self.search_lines(self.binary_img)
        #self.get_stop_line(self.binary_img)
        self.get_stop_line(self.binary_img)

    def get_binary(img, display):
        print(0)
        
    def get_stop_line(self,img):  # 정지선을 반환하는 코드(정지선 제일 앞 부분), GRAY로 들어옴
        left_high = (int(0.35*self.display[0]), int(0.96*self.display[1]))
        right_low = (int(0.65*self.display[0]), int(0.98*self.display[1]))
        img1 = img[left_high[1]:right_low[1], left_high[0]:right_low[0]]
        num = cv2.countNonZero(img1)
        img=cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(img, left_high, right_low, (0, 255, 0), 2)
        Area=(right_low[0] - left_high[0])*(right_low[1]-left_high[1])
        cv2.imshow('hi', img)
        cv2.waitKey(1)

        if(num > int(Area*0.6)):
            return True
        else:
            return False
        
    def get_floor_color(self, img):
        flag = get_color(img, self.display)
        if(len(self.floor_color_buf) > 10):
            self.floor_color_buf.pop(0)
        #print(self.floor_color_buf)
        self.floor_color_buf.append(flag)
        for i in self.floor_color_buf :
            if(i == False):
                return False
        return True
            
    def search_lines(self,b_img):
        
        histogram = np.sum(b_img[int(b_img.shape[0]/2):, :], axis=0)

        monitor = np.dstack((b_img, b_img, b_img))
        
        midpoint = np.int(histogram.shape[0] / 2)
        
        left_sk = np.linspace(0.3, 1, 0.85*midpoint)
        left_sk = np.concatenate([left_sk,np.linspace(1, 0, 0.15*midpoint)])
        
        right_sk = np.linspace(0, 1, 0.15*midpoint)
        right_sk = np.concatenate([right_sk,np.linspace(1, 0.3, 0.85*midpoint)])
                    
        left_x_max = np.argmax(left_sk*histogram[:midpoint]) 
        right_x_max = np.argmax(right_sk*histogram[midpoint:]) + midpoint

        window_height = np.int(b_img.shape[0]/self.n_windows)
        
        #print(b_img.nonzero())
        
        current_left = left_x_max
        current_right = right_x_max
        
        left_lane_x = []
        right_lane_x = []
        left_lane_y = []
        right_lane_y = []
        
        for windows in range(self.n_windows):
            win_y_low = b_img.shape[0] - (windows+1) * window_height
            win_y_high = win_y_low + window_height
            left_x_low = current_left - self.windows_width
            left_x_high = current_left + self.windows_width
            right_x_low = current_right - self.windows_width
            right_x_high = current_right + self.windows_width
            
            
            cv2.rectangle(monitor, (left_x_low, win_y_low), (left_x_high, win_y_high), (0, 255, 0), 2)
            cv2.rectangle(monitor, (right_x_low, win_y_low), (right_x_high, win_y_high), (0, 255, 255), 2)
            
            left_x = np.array(b_img[win_y_low:win_y_high,left_x_low:left_x_high].nonzero()[1]) + left_x_low
            left_y = np.array(b_img[win_y_low:win_y_high,left_x_low:left_x_high].nonzero()[0]) + win_y_low
            right_x = b_img[win_y_low:win_y_high,right_x_low:right_x_high].nonzero()[1] + right_x_low
            right_y = b_img[win_y_low:win_y_high,right_x_low:right_x_high].nonzero()[0] + win_y_low

            # If you found > minpix pixels, recenter next window on their mean position
            if len(left_x) > self.min_pixel_num:
                current_left = np.int(np.mean(left_x))
            if len(right_x) > self.min_pixel_num:
                current_right = np.int(np.mean(right_x))
                
            left_lane_x.append(left_x)
            right_lane_x.append(right_x)
            left_lane_y.append(left_y)
            right_lane_y.append(right_y)
        
        
        lx = np.concatenate(left_lane_x)
        ly = np.concatenate(left_lane_y)
        rx = np.concatenate(right_lane_x)
        ry = np.concatenate(right_lane_y)

        self.left.current_line = [lx,ly]
        self.right.current_line = [rx,ry]
        
        ploty = np.linspace(0, b_img.shape[0] - 1, b_img.shape[0])
        
        left_fit = np.polyfit(ly, lx, self.poly_order)
        right_fit = np.polyfit(ry, rx, self.poly_order)
            
        line_left = np.poly1d(left_fit)
        line_right = np.poly1d(right_fit)
                        
        y1 = line_left(ploty)
        y2 = line_right(ploty)
               
        if (len(rx)>2000) & (len(lx) >2000):
            self.left.prevx.append(y1)
            self.right.prevx.append(y2)
    
            self.left.detect = True
            self.right.detect = True
        else:
            self.left.detect = False
            self.right.detect = False
        
        num = 5
        
        if len(self.left.prevx) > num:
            self.left.prevx.pop(0)
            left_avg_line = smoothing(self.left.prevx, num, self.display)
            left_avg_fit = np.polyfit(ploty, left_avg_line, self.poly_order)
            l = np.poly1d(left_avg_fit)
            left_fit_plotx = l(ploty)
            self.left.current_fit = left_avg_fit
            self.left.allx, self.left.ally = left_fit_plotx, ploty
        else:
            
            self.left.current_fit = left_fit
            self.left.allx, self.left.ally = y1, ploty
    
        if len(self.right.prevx) > num:
            self.right.prevx.pop(0)
            right_avg_line = smoothing(self.right.prevx, num, self.display)
            right_avg_fit = np.polyfit(ploty, right_avg_line, self.poly_order)
            r = np.poly1d(right_avg_fit)
            right_fit_plotx = r(ploty)
            self.right.current_fit = right_avg_fit
            self.right.allx, self.right.ally = right_fit_plotx, ploty
            
        else:
            self.right.current_fit = right_fit
            self.right.allx, self.right.ally = y2, ploty
        
        draw_points(monitor,self.left.allx,ploty,(0,0,255),3)
        draw_points(monitor,self.right.allx,ploty,(0,255,0),3)

        cv2.imshow("ss",monitor)
        return monitor
        

def show_video():
    #video="video\pre_lane_Trim.mp4"
    cap = cv2.VideoCapture(2)
    
    cap.set(3,800)
    cap.set(4,600)
    
    lane = Lane_Detection(display=(800,600))
    while True:
        ret, img = cap.read()
        img = cv2.resize(img,(800,600),interpolation = cv2.INTER_AREA)
        cv2.imshow('kkk', img)
        if not ret:
            print('비디오 끝')
            break
        
        #lane.get_floor_color(img)
        lane.run(img)
        #cv2.imshow("zzz",img)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break        

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    show_video()
