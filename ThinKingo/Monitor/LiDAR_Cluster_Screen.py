from Screen import Screen
from Database import Database
import numpy as np
import cv2

class LiDARClusterScreen(Screen):
    def __init__(self, width: int, height: int, db: Database):
        super().__init__(width=width, height=height)
        self.db = db
        self.__img = np.zeros((324, 576, 3), np.uint8)


    def render(self):
        self.__img = np.zeros((324, 576, 3), np.uint8)
        self.__img = cv2.circle(self.__img, (144, 162), 10, (255, 0, 0), 2)
        dx = self.db.control_data.p_targ[0] - self.db.control_data.p_curr[0]
        dy = self.db.control_data.p_targ[1] - self.db.control_data.p_curr[1]
        self.__img = cv2.circle(self.__img, (int(144 + dx * 10), 162 + int(dy * 10)), 10, (0, 255, 0), 2)
        angle = self.db.control_data.car_angle * np.pi / 180
        self.__img = cv2.line(self.__img, (144, 162), (144 + int(np.sin(angle) * 100), 162 - int(np.cos(angle) * 100)), (255, 0, 0), 1)
        self.__img = cv2.putText(self.__img, f"Angle:{self.db.control_data.car_angle}", (288, 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0))
        # self.__img = cv2.putText(self.__img, f"Angle Error:{self.db.control_data.angle_error}", (288, 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0))
        return self.__img
