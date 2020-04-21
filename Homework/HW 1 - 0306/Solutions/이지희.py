import os

def createFolder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

current_dir = os.getcwd()
path = os.path.join(current_dir,'data')
createFolder(path)

file = open(os.path.join(current_dir,'files.txt'),'w')
file.close()

for i in range (0, 100):
    f = open(os.path.join(current_dir,'data/00%d.txt'%i),'w')
    f.write('%d'%i)
    f.close()

file_list = os.listdir(path)
file_list.sort()

j=0
while j < len(file_list):
    file = open(os.path.join(current_dir,'files.txt'),'a')
    file.write('data/'+file_list[j]+'\n')
    j = j + 1
    file.close()
