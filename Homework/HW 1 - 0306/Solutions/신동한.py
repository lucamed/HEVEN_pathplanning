import os

os.mkdirs('C:\\Users\\신동한\\Downloads\\Autonomous-Car-Simulator-master\\heven2020\\data')
for i in range(100):
    file = open('C:\\Users\\신동한\\Downloads\\Autonomous-Car-Simulator-master\\heven2020\\data.00{}.txt'.format(i), 'w')
    file.write("{}".format(i))

files = open('C:\\Users\\신동한\\Downloads\\Autonomous-Car-Simulator-master\\heven2020\\files.txt', 'a')
for i in range(100) :
    files.write('data/00{}.txt\n'.format(i))


