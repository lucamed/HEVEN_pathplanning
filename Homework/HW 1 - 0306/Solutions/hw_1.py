import os

os.makedirs('data')

for i in range(0,100):
    f=open('data/00%d.txt' % i,'w')
    data = "%d" %i
    f.write(data)
    f.close()

g=open("files.txt",'w')

g.write("data/000.txt\n")

for i in range(1,10):    
    data = "data/00%d.txt \n" %i    
    g.write(data)
    
    for j in range(0,10):
        data = "data/00%d%d.txt \n" %(i,j)
        g.write(data)

g.close()
