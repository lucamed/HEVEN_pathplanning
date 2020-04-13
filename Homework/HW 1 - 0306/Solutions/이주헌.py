#hw1

import os
data = r'C:\Users\dlwng\Desktop\_이주헌\data'

os.makedirs(data)

for i in range(1,100):
    text=open("C:/Users/dlwng/Desktop/_이주헌/data/00%d.txt" % i,'w')
    data = "%d \n" %i
    text.write(data)
    text.close()

txt=open("C:\Users\dlwng\Desktop\_이주헌\files.txt",'w')
txt.write("data/000.txt\n")
for i in range(1,10):    
    data = "data/00%d.txt \n" %i    
    txt.write(data)
    
    for j in range(0,10):
        data = "data/00%d%d.txt \n" %(i,j)
        txt.write(data)

txt.close()


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

