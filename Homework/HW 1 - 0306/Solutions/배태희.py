import os

os.mkdir('C:\\workspace\\heven_week1\\data')
for i in range(100):
    file = open('C:\\workspace\\heven_week1\\data\\00{}.txt'.format(i), 'w')
    file.write("{}".format(i))

files = open('C:\\workspace\\heven_week1\\files.txt' ,'a')
for i in range(100):
    files.write("date/00{}.txt\n".format(i))