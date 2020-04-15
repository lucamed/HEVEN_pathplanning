import os

path = r'C:\Users\sjy26\Desktop\HEVEN\HW#1\data'

os.mkdir(path)

for i in range(1,100):
    f = open ("C:/Users/sjy26/Desktop/HEVEN/HW#1/data/00%d.txt" %i,'w')
    content = "%d" %i
    f.write(content)
    f.close()

f = open("C:/Users/sjy26/Desktop/HEVEN/HW#1/files.txt",'w')

for i in range(0,100):
    number = str(i)
    f.write("data" + "00" + number + ".txt\n")

f.close()
