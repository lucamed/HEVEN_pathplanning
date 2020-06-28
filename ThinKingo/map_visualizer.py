import os
import folium


def convert(loc_data):
    loc_data = loc_data.replace("'", "")
    loc_data = loc_data[1:-2].split(',')

    loc_data[1] = loc_data[1].strip()
    loc_data[3] = loc_data[3].strip()

    lat_int = int(loc_data[1][:2])
    lat_hour = float(loc_data[1][2:])

    real_lat = lat_int + lat_hour / 60

    long_int = int(loc_data[3][:3])
    long_hour = float(loc_data[3][3:])

    real_long = long_int + long_hour / 60

    print(real_lat, real_long)

    return real_lat, real_long


current_dir = os.getcwd()
filename = "/Database/gps2.txt"
file_dir = current_dir + filename

with open(file_dir,"r") as f:
    data = f.readlines()

start_lat, start_long = convert(data[0])
map = folium.Map(location=[start_lat, start_long], zoom_start=15)

cnt = 0

for single_data in data:
    print(single_data)
    mark_lat, mark_long = convert(single_data)

    # 숫자 조정으로 마커 간격 조정 가능
    if cnt % 30 == 0:
        folium.Marker(
            location=[mark_lat, mark_long],
            icon=folium.Icon(color='red', icon='star')
        ).add_to(map)

    cnt+=1

map.save('map_visualize.html')
