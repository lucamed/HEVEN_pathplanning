import os
cur_dir = os.getcwd()
new_dir = "data"
if not os.path.isdir(cur_dir + "/" + new_dir + "/"):
    os.mkdir(cur_dir+"/"+new_dir+"/")
os.chdir(cur_dir+"/"+new_dir+"/")
for i in range(100):
    name = "00"+str(i)+".txt"
    f = open(name,"w")
    f.write(str(i))
    f.close()