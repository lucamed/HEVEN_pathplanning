import glob, os
os.chdir("./negative_data")
for file in glob.glob("*.JPG"):
    f = open(file[:-4]+'.txt','w+')
    f.close() 
