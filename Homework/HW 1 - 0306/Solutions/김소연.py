import os

os.mkdir('C:/Users/LG/Desktop/data')

i=0
while i<100 :
    f=open("C:/Users/LG/Desktop/data/00%d.txt"%i,'w')
    f.write("%d" %i)
    i=i+1
    f.close()

a=open("C:/Users/LG/Desktop/files.txt","a")

j=0
while j<100 :
    a.write("data/00%d.txt\n"%j)
    j=j+1
a.close()
