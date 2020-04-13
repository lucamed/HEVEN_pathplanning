import os

os.mkdir('data')
for i in range(1, 100):
 f = open("C:/Users/황태원/Desktop/data/00%d.txt"% i, 'w')
 data = "%d \n" % i
 f.write(data)
 f.close()

f = open("C:/Users/황태원/Desktop/files.txt", 'w')
f.write("data/000.txt\n")
for i in range(1, 10):
 data = "data/00%d.txt \n" % i
 f.write(data)
 for j in range(0, 10):   
  text = "data/00%d%d.txt \n" %(i,j)
  f.write(text)

f.close()
