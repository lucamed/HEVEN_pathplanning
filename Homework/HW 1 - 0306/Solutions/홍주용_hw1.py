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

os.mkdir("data_")


for i in range (0,100):

    num = str(i)

    f= open("C:/Users/홍주용/Desktop/hw_0306/hw_week1/hw_1/data_/"+"00"+num+".txt","w")   # 경로 설정

 
    
    f.write(num)

    f.close()
    

f= open("C:/Users/홍주용/Desktop/hw_0306/hw_week1/hw_1/files_.txt","a")

for i in range(0,100):
    num_=str(i)

    f.write("data/"+"00"+num_+"txt\n")

f.close()
