#Q1
import os
data=os.getcwd() + "\Data"
try:
    # Create target Directory
    os.mkdir(data)
    print("Directory " ,data,  " Created ")
except FileExistsError:
    print("Directory " ,data,  " already exists")

    for i in range (0,100):
        f = open(os.path.expanduser(os.path.join(data, "00"+str(i) + ".txt")), "w")
        f.write(str(i))
