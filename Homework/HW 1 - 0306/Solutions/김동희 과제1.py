import os

os.mkdir('data')

for i in range(0,100):
    f=open("C:\\Users\\ehd48\\Desktop\\올빼미\\data\\00%d.txt"%i,'w')
    data="%d"%i
    f.write(data)
    f.close()

f=open("C:\\Users\\ehd48\\Desktop\\올빼미\\files.txt","w")
for i in range(0,100):
    f.write("data00%d.txt\n"%i)


f.close()
