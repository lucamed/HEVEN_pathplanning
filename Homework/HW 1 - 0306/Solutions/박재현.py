import os

bsdir = os.path.dirname(os.path.abspath(__file__))+'\data'

os.mkdir(bsdir)

for i in range(0,100) :
    filepath=os.path.join(bsdir,'00{}.txt'.format(i))
    f = open(filepath,'w')
    i = str(i)
    f.write(i)

with open('files.txt','w') as f:
        file=os.listdir(bsdir)
        for i in file:
            name=str(i)
            f.write('\ndata/')
            f.write(name)

            
