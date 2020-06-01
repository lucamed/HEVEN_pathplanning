import os

dir = "/data/"
parent_dir = os.getcwd()
path = parent_dir+dir

os.mkdir(path)

for i in range(0,100):
    a = open(path+'00%d.txt' %i, 'w')
    a.write('%d' %i)

for j in range(0,100):
    b = open('files.txt','a' )
    b.write("data/00%d.txt\n" %j)
    b.close()
