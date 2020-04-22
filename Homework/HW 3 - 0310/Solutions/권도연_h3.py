from PIL import Image
import random
import os
img = Image.open("sign.jpg")
(a,b)=img.size #신호 이미지 크기 조사
area=(140,80,250,200) #자를려는 신호의 위치 (왼쪽끈,위쪽끝,오른쪽끝,아래끝)
cropped_img=img.crop(area) #이미지 자르기
(c,d)=(cropped_img.size) #자른 이미지 크기
cropped_img.save("cropped_img.jpg") #자른 이미지 저장
e=Image.open("cropped_img.jpg")  #자른 신호 이미지 불러오기
os.mkdir('data')#파일만들기
m=1
while m<=100:
    f = Image.open("road.jpg")  # 붙일려는 이미지 불러오기
    (g, h) = (f.size)  # 길사진 이미지 크기 조사
    i = random.randrange(0, g) #가로 크기에 대한 랜덤
    j = random.randrange(0, h) #세로 크기에 대한 랜덤
    k = i - c #사진 넣을 위치(가로)
    l = j - d #사진 넣을 위치(세로)
    f.paste(e, (k, l)) #사진 추가하가(f에 e를 (k.l)위치에 추가
    f.save("data/road%d.jpg"%m) #추가된 사진 저장하기
    f.show()
    m += 1
    f.close()