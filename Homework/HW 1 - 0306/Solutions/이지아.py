#Create Directory
import os

dirName = 'data'
os.mkdir('data')

#Create file
for i in range(100):
    num = str(i)
    f = open("C:/Users/Gia Lee/Desktop/HEAVEN/data/00"+num+".txt", 'w')
    f.write(num)
    f.close()

#Create 'files.txt'
f = open("C:/Users/Gia Lee/Desktop/HEAVEN/files.txt", 'w')
for i in range(100):
    num = str(i)
    f.write("data/00"+num+".txt\n")
f.close()
