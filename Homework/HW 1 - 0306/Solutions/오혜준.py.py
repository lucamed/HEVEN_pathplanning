import os
os.mkdir('C:\\Users\\USER\\Downloads\\hw_1\\hw_1\\data')
for i in range(100):
    file = open('C:\\Users\\USER\\Downloads\\hw_1\\hw_1\\data\\00{}.txt'.format(i), 'w')
    file.write("{}".format(i))

files = open('C:\\Users\\USER\\Downloads\\hw_1\\hw_1\\files.txt', 'a')
for i in range(100):
    files.write("data/00{}.txt\n".format(i))
