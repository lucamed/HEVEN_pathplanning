#Q3-Diva
import cv2,os
from random import randint
rimg = cv2.imread("road.jpg") #getroad
simg = cv2.imread("sign.jpg")#get signboard
cv2.imshow('sign',simg)
cv2.waitKey(1000)
w, h,chan = simg.shape #get sign board dimensions
a, b, chan2 = rimg.shape #get road dimensions
crop_img = simg[int((w/2)-(h/8)):int((w/2)+(h/8)),0:int(h/4)] #crop sign to get board
cv2.imshow("cropped", crop_img)
cv2.waitKey(1000)
if os.path.isdir(os.getcwd()+"\Images")==False: #check if the directory exists if not make one
    os.mkdir(os.getcwd()+"\Images")
for i in range(0,100):
    x,y = randint(1,b-(h/4)),randint(1,a-(h/4)) #get random co-ordinates on the background image
    replace = rimg.copy() #get info of road image
    replace[y: y+int(h/4), x: x+int(h/4)] = crop_img #replace the background image with cropped sign
    cv2.imshow('replace', replace)
    cv2.waitKey(100)
    if os.path.isfile(os.getcwd() + "\Images"+"\road"+str(i)+".jpg") == False: #check if file exists
        cv2.imwrite(os.path.join(os.getcwd()+"\Images", 'road_00'+str(i)+".jpg"), replace) #save the file in given path