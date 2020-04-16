import os

os.mkdir("C:/Users/hyun1/Desktop/HEVEN/hw_0306/HW1/data")

for i in range(1,101):
    f = open("C:/Users/hyun1/Desktop/HEVEN/hw_0306/HW1/data/00%d" %i, 'w')
    f.write("%d" %i)
f.close 

file = open("C:/Users/hyun1/Desktop/HEVEN/hw_0306/HW1/data/files", 'w')
for i in range(0,101):
    file.write("data/00%d.txt\n" %i)
file.close
