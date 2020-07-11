import matplotlib.pyplot as plt
import numpy as np

f = open("ThinKingo\\Database\\77.txt", 'r')
logging_file = []
while True:
    line = f.readline()
    if not line: break
    temp = line.replace('[', '').replace(']', '').split(',')
    logging_file.append([float(temp[1]), float(temp[3])])
f.close()

f = open("ThinKingo\Database\K-City 본선전 경로 파일(LLH).txt", 'r')
log = []
while True:
    line = f.readline()
    if not line: break
    temp = line.replace('[', '').replace(']', '').split('\t')
    log.append([float(temp[0]), float(temp[1])])
f.close()

logging_file = np.array(logging_file)

gx = logging_file[:,0]
gy = logging_file[:,1]

gx = gx // 100 + (gx % 100)/60
gy = gy // 100 + (gy % 100)/60

gx *= 110000
gy *= 88800
'''
temp = np.array([[37.23982,126.77336],
[37.23986,126.77327],
[37.23990,126.77320],
[37.23994,126.77311],
[37.23999,126.77308],
[37.24003,126.77308],
[37.24008,126.77307],
[37.24013,126.77309],
[37.24019,126.77313],
[37.24024,126.77317],
[37.24029,126.77321],
[37.24031,126.77325],
[37.24029,126.77332],
[37.24027,126.77338],
[37.24024,126.77344],
[37.24021,126.77351],
[37.24019,126.77359]])

x = temp[:,0] * 110000
y = temp[:,1] * 88800

x = x - x[0]
y = y - y[0]
'''
log = np.array(log)

n = log[:,0] * 110000
e = log[:,1] * 88800

plt.figure(figsize = (8,8))

plt.scatter(gy - e[0], gx - n[0])
#plt.scatter(y,x, c= 'r')
plt.scatter(e - e[0],n - n[0], c = 'black')
#plt.xlim(0,200)
#plt.ylim(0,200)
plt.xscale("linear")
plt.yscale("linear")


for i in range(1,4):
    f = open("ThinKingo\\Database\\park%d.txt"%i)
    l = []
    while True:
        line = f.readline()
        if not line: break
        temp = line.replace('[', '').replace(']', '').split(',')
        l.append([float(temp[1]), float(temp[3])])
    f.close()

    l = np.array(l)

    tx = l[:,0]
    ty = l[:,1]

    tx = tx //100 + (tx % 100)/60
    ty = ty //100 + (ty % 100)/60

    tx *= 110000
    ty *= 88800

    plt.scatter(ty -e[0] , tx - n[0])
    
            

plt.show()