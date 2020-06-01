#hw_1

import os

os.mkdir('data')

for i in range(0, 100) :
    f = open("C:/Users/hj971/OneDrive/바탕 화면/성균관대학교/동아리/HEVEN/과제/hw_week1/hw_1/안호진/data/00%d.txt" %i, 'w')
    f.write("%d \n" %i)
    f.close()

t = open("C:/Users/hj971/OneDrive/바탕 화면/성균관대학교/동아리/HEVEN/과제/hw_week1/hw_1/안호진/files.txt", 'w')
t.write("data/000.txt\n")
for i in range(1, 10) :
    t.write("data/00%d.txt\n" %i)
    for j in range(0, 10) :
        t.write("data/00%d%d.txt\n" %(i, j))
t.close()
