# -*- coding: cp949 -*-
"""
1. Make a directory called "data" using the OS library in python 
2. Create inside the folder 'data' 100 txt files with the name "00X.txt" (while X is the number of that file) eg: 
 	000.txt 001.txt 0096.txt 
3. Inside every txt file should contain written X (file number). eg: 
 	inside 0019.txt -> 19 
4. Create a txt file called 'files.txt' with the paths to all the new txt files outside the data folder. eg: 
 	data/000.txt 
 	data/001.txt 
 	... 
 	data/0098.txt 
 	data/0099.txt 
  
 Use the given files as example! 
 """
import os
parent_dir="C:\Users\임승현\Desktop\HEVEN\week1"
directory="data"
path=os.path.join(parent_dir,directory)

os.mkdir(path)
for i in range (0,100):
    n=str(i)
    file=open("C:\Users\임승현\Desktop\HEVEN\week1\data\\"+"00"+n+".txt",'w')
    file.write(n)
    file.close()
    
f=open("C:\Users\임승현\Desktop\HEVEN\week1\data\\files.txt",'w')
for i in range(0,100):
    n=str(i)
    
    f.write("data\00%d.txt\n" %i)
    
f.close()
             
