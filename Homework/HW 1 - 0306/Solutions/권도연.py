Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 22:45:29) [MSC v.1916 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import os
dir_path = 'C:/Users/권도연/Desktop' 
dir_name = 'data'
os.mkdir(dir_path + "/" + dir_name + "/")
 i=0
while i<100:
	f = open ('C:/Users/권도연/Desktop/data/00%d.txt'%i,'w')
	f.write('%d'%i)
	f.close()
	i+=1
j=0
k = open('C:/Users/권도연/Desktop/files.txt','a')
while j<100:
          k.write('data/00%d.txt\n' %j)
	j+=1
k.close()
