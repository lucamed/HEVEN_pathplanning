# -*- coding: utf-8 -*-

import math
from copy import deepcopy
from reeds_shepp_path import ReedsSheppPath, draw_point
import numpy as np
from a_star import AStar
from mapinfo import MapInfo
import matplotlib.pyplot as plt

start = [1, 1, 90 / 180.0 * np.pi]
end = [10, 10,  90 / 180.0 * np.pi]
r = 5.0
rspath = ReedsSheppPath(start, end, r)
rspath.calc_paths()
a = rspath._paths
path, xx = rspath.get_shortest_path()
xs, ys, _ = ReedsSheppPath.gen_path(start, path, r,section= False)
#for i in range(len(xs)):
plt.plot(xs,ys)

'''
m = MapInfo(60, 40)
m.show()
m.start = (10.5, 10)
m.end = (50, 30)
m.obstacle = [(20, i) for i in range(30)] + [(40, 40 - i) for i in range(30)]

plan = AStar(m.start, m.end, m)
if plan.run(display=False):
    m.path = plan.reconstruct_path()
    path2 = plan.reconstruct_path()
'''
for i in range(5):
    print(i)
    if i <3:
        continue
    print('바보')