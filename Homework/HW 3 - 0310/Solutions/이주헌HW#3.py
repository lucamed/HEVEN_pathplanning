import random                                                  #random 함수를 이용하기 위한 패키지
import numpy                                                   #배열을 생성하기 위한 패키지
import cv2                                                     #OpenCV를 불러오는 패키지 

signimage = cv2.imread("hw_0307\\hw_0307\\hw_1\\sign.jpg")     #sign.jpg를 불러와서 signimage에 저장한다.
cut = signimage.copy()                                         #signimage를 cut이라는 변수에 저장한다.
cut = signimage[310:440, 250:380]                              #원하는 크기만큼의 이미지를 cut에 저장한다.

cv2.imshow("cut", cut)                                         #cut에 저장된 이미지를 보여준다.

[a, b, c] = cut.shape                                          #cut에 저장된 이미지의 좌표를 받아 a,b,c에 저장한다.

for i in range(1, 101):                                        #100번의 반복문을 실행하는 for문이다.
    x = random.randint(0, 1131-a)                              #랜덤한 수를 x에 저장하는데, 이미지의 세로축의 최대길이 1131을 넘어가지 않도록 한다.
    y = random.randint(0, 1696-b)                              #램덤한 수를 y에 저장하는데, 이미지의 가로축의 최대길이 1696을 넘어가지 않도록 한다.
    roadimage= cv2.imread("hw_0307\\hw_0307\\hw_1\\road.jpg")  #road.jpg르 불러와서 roadimage에 저장한다.
    roadimage[x:x+a, y:y+b] = cut                              #roadimage에 랜덤한 수로 입력된 좌표에 cut의 사이즈 만큼의 좌표를 더하고 cut에 저장된 이미지를 덧붙인다.
    cv2.imshow("roadimage", roadimage)                         #roadimage에 저장된 이미지를 보여준다.
    cv2.imwrite("road_00%d.jpg" %i, roadimage)                 #road_00%d.jpg라는 이름으로 roadimage를 저장하고 d의 자리에 반복문을 통해 1~100의 수가 차례로 들어간다.
    
cv2.waitKey(0)
cv2.destroyAllWindows()                                        #아무키나 누를시에 창 종료.
