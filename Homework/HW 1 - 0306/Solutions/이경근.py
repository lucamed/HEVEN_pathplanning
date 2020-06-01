import os

directory="data"

parent_dir="/Users/rudrm/desktop"

path=os.path.join(parent_dir,directory)

os.mkdir(path)

print("Directory '%s' created" % directory)

for X in range(0,100):
    
    f=open("/Users/rudrm/desktop/data/00%d.txt"%X,'w')


    data="%d"%X
    f.write(data)
    f.close

f=open("/Users/rudrm/desktop/files.txt","a")

for i in range(0,100):
    num=str(i)
    f.write("data/"+"00"+num+".txt\n")
f.close()
