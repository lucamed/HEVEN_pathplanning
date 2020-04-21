import os


b = "data/"
filePath = os.getcwd()
path = os.path.join(filePath,b)

os.mkdir(path)

for i in range(0, 100):
    a = open(path + '00{}.txt'.format(i), 'w')
    a.write('{}'.format(i))
a.close()


with open('files.txt','w') as hello:
        file = os.listdir(path)
        for i in file:
            c = str(i)
            hello.write('\ndata/')
            hello.write(c)

