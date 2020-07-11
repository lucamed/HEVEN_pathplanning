#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from mapinfo import MapInfo
from copy import deepcopy
import math
import time

class AStar(object):
    def __init__(self, start, end, map_info, step = 2):
        self._s = start
        self._e = end
        self._map_info = map_info
        self._openset = dict()
        self._closeset = dict()
        self.step = step

    def distance(self, p1, p2):
        #return abs(p1[0] - p2[0])+abs(p1[1] - p2[1])
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def neighbor_nodes(self, x):
        plist = [(x[0] - self.step, x[1] - self.step), (x[0] - self.step, x[1]), (x[0] - self.step, x[1] + self.step), (x[0], x[1] + self.step), (x[0] + self.step, x[1] + self.step), (x[0] + self.step, x[1]), (x[0] + self.step, x[1] - self.step), (x[0], x[1] - self.step)]
        for p in plist:
            if not self._map_info.is_collision(point=p):
                yield p
                
#좌표들을 순서를 바꿔서 반환(시작부터로)
    def reconstruct_path(self):
        pt = self._e
        path = []
        while pt:
            path.append(pt)
            pt = self._closeset[pt]['camefrom']
        return path[::-1]

    def run(self, display=False):
        st = time.time()
        epsilon = 2
        h = self.distance(self._s, self._e)
        self._openset[self._s] = {'g': 0, 'h': h, 'f': h, 'camefrom': None,'depth' : 0}
        while self._openset:
            x = min(self._openset, key=lambda key: self._openset[key]['f'])
            self._closeset[x] = self._openset.pop(x)
            
            if self.distance(x, self._e) < self.step:
                if x != self._e:
                    self._closeset[self._e] = {'camefrom': x}
                    print('Astar',time.time() - st)
                return True
            if display:
                self._map_info.close = x
            for y in self.neighbor_nodes(x):
                if y in self._closeset:
                    continue
                tentative_g_score = self._closeset[x]['g'] + self.distance(x, y)
                if y not in self._openset:
                    tentative_is_better = True
                elif tentative_g_score < self._openset[y]['g']:
                    tentative_is_better = True
                else:
                    tentative_is_better = False
                if tentative_is_better:
                    # epsilon * h --> high quality                
                    h = epsilon*self.distance(y, self._e)
                    '''
                    if self._closeset[x]['depth'] < h:
                        w = 1 - self._closeset[x]['depth']/h
                    else:
                        w = 0
                        
                    h = (1+epsilon*w)*h
                    '''
                    self._openset[y] = {'g': tentative_g_score, 'h': h, 'f': tentative_g_score + h, 'camefrom': x,'depth' : self._closeset[x]['depth']+1}
                    if display:
                        self._map_info.open = y
        return False

if __name__ == "__main__":
    m = MapInfo(40, 40)
    m.show()
    m.start = (10, 10)
    m.end = (30, 30)
    m.obstacle = [(20, i) for i in range(30)] + [(40, 40 - i) for i in range(1)]
    input('enter to start ...')
    plan = AStar(m.start, m.end, m)
    if plan.run(display=False):
        m.path = plan.reconstruct_path()
    m.wait_close()