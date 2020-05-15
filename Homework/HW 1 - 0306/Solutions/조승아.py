import os

p='C:\\Users\\USER\\Desktop\\헤븐\\HW1-1\\data'
os.mkdir(p)

for i in range(1,100):
    file=open('C:\\Users\\USER\\Desktop\\헤븐\\HW1-1\\data\\00%d.txt'%i,'w')
    file.write('%d'%i)
    file.close()
    
    file_path=os.path.abspath('.\\00%d.txt'%i)
    files=open('C:\\Users\\USER\\Desktop\\헤븐\\HW1-1\\files.txt','a')
    files.write(file_path)
    files.write('\n')
    files.close()

