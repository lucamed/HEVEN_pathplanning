f = open("C:\\Users\\유정현\\Desktop\\heven\\HEVEN-AutonomousCar-2019\\ThinKingo\\Database\\gps_park_test.txt", 'r')
g = open("C:\\Users\\유정현\\Desktop\\gps_park_test_t.txt", 'w')

while True:
    line = f.readline()
    if not line : break
    else:
        temp = line.replace('[', '').replace(']', '').split(',')
        lad = float(temp[1])
        lon = float(temp[3])
        latitude = (lad//100) + (lad%100)/60
        longitude = (lon//100) + (lon%100)/60
        data = str(latitude) + ' ' + str(longitude) + '\n'
        g.write(data)

f.close()
g.close()