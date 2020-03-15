import os

directory="data/"
parent_dir=os.getcwd()
path=os.path.join(parent_dir,directory)
os.mkdir(path)

for i in range(0,100):

    file=open(path+'00%d.txt' %i,'w')
    file.write('%d' %i)
        
    file=open('files.txt','a' )
    file.write("data/00%d.txt\n" %i)

file.close()
