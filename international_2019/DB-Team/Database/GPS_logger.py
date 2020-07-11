from GPS import GPS
import folium
import _thread

class GPS_logger:
    def __init__(self, GPS):
        # 위도 : lad, 경도 : lon
        self.GPS = GPS
        self.data = None
        self.lad = None
        self.lon = None

    def input_thread(self, a_list):
        input()
        a_list.append(True)

    def save_textdata(self):
        input("Press enter to Start&End Logging")
        a_list = []
        _thread.start_new_thread(self.input_thread, (a_list,))

        while not a_list:
            print("!")

        while():
            self.data = self.GPS.data()
            self.lad = self.data[1]
            self.lon = self.data[3]
            str = "위도 : {}, 경도 : {}".format(self.lad, self.lon)
            print(str)

    def visulaize_chart(self):
        pass

    def visualize_map(self):
        m = folium.Map(location=[37.2358, 126.7726], zoom_start=12)
        folium.Marker(location=[37.2358, 126.7726], popup="Marker A",
                      icon=folium.Icon(icon='cloud')).add_to(m)
        folium.Marker(location=[37.2358, 126.7750], popup="한남동",
                      icon=folium.Icon(color='red')).add_to(m)
        m.save('map.html')

if __name__ == '__main__':
    # gps = GPS('COM3', 19200, Flag())
    gps_logger = GPS_logger(GPS)
    gps_logger.save_textdata()
    GPS_logger.visualize()

    GPS_logger.save_textdata()