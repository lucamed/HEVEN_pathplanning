import os

path='C:/Users/yeeun/happyseo/data'

os.mkdir(path)

for i in range(0,100):
    file= open("C:/Users/yeeun/happyseo/data/00%d.txt" %i,'w')
    file.write(str(i))
    file.close()

for j in range(0,100):
    f=open("C:/Users/yeeun/happyseo/files.txt",'a')
    f.write('data/'+'00'+str(j)+'txt\n')
f.close()