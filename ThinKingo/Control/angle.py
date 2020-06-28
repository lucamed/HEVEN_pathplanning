import numpy as np

t1 = [37.24011983, 126.7736726]
t2 = [37.23993, 126.7735523]

targetdir_x = t2[1] - t1[1]
targetdir_y = t2[0] - t1[0]

target_angle = np.arctan2(targetdir_y, targetdir_x) * 180 / np.pi

# 각 변환
target_angle = (450 - target_angle) % 360

print(target_angle)