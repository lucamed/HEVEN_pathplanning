import os

os.mkdir("C:/Users/박승현/Desktop/hw/data")
for i in range(0,100):
    f=open("C:/Users/박승현/Desktop/hw/data/00%d.txt" %i, "w")
    f.write(str(i))

f=open("C:/Users/박승현/Desktop/hw/files.txt", "w")
for i in range(0,100):
    f.write("data/00"+str(i)+".txt\n")

f.close()
