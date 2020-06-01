import os
os.mkdir("data")
for i in range(1,100):
   a = str(i)
   f = open("C:/Users/a/Desktop/대외활동/heven/파이썬/data/"+"00"+a+".txt" ,"w")
   f.write(a)
   f.close()

g = open("C:/Users/a/Desktop/대외활동/heven/파이썬/data/files.txt","w")
for j in range(1,100) :
    b = str(j)
    g.write("data/00" + b + ".txt\n")

g.close()
