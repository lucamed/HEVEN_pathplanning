import sys
import os
sys.path.append(os.path.dirname(__file__))

from mapinfo import MapInfo
import math
from copy import deepcopy
from reeds_shepp_path import ReedsSheppPath, draw_point
from car import Car
from a_star import AStar
import matplotlib.pyplot as plt
import time
import numpy as np

class HybridAStar(object):
    def __init__(self, start, end, map_info, car, r, r_step = 3, grid_step = 10):
        self._s = start
        self._e = end
        self._map_info = map_info
        self._car = car
        self._r = r
        self._openset = dict()
        self._closeset = dict()
        self.step = r_step
        self.grid_step = grid_step

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
    #Span 할때 left, right, straight 를 스텝을 나누어서 진행 후 Map 안에 있는지 확인
    #형식은 ['l or r or s' , angle or 길이] 로 나타 낸 후 Reed 클래스의 gen 함수를 이용하여 좌표 path로 변환
    def neighbors(self, p):
        #self.step = 3.0
        # Path의 Resolution을 나타내는 Step --> 낮을수록 정확하고 느림 but 높을수록 빠름 but 발산 가능성 높아짐!!
        paths = [['l', self.step / self._r], ['s', self.step], ['r', self.step / self._r],
                 ['l', -self.step / self._r], ['s', -self.step], ['r', -self.step / self._r]]
        for path in paths:
            #section이 True면 커브와 직선을 나누어서 데이터를 받고 False면 한꺼번에 하나의 list로 받음
            xs, ys, yaws = ReedsSheppPath.gen_path(p, [path], r=self._r, section=False, step_size = self.step)
            if not self.is_collision_rs_car(xs, ys, yaws):
                yield (round(xs[-1], 1), round(ys[-1], 1), round(yaws[-1], 1)), path, [xs, ys, yaws]
                #xs,ys,yaws의 마지막 수를 소수점 2번째까지 반올림 + path + 반올림 하지 않은 [xs,ys,yaws]
                # local end point, path, 좌표상의 path
                
    #현재 PATH가 유효한지 확인하는 함수                
    def is_collision_rs_car(self, xs, ys, yaws):
        for pt in zip(xs, ys, yaws):
            self._car.set_position(pt)
            if self._map_info.is_collision(car_outline=self._car.get_outline()):
                return True
        return False

    #A star로 경로를 찾았을 때 현재 지점에서 end 까지의 경로거리 = hueristic cost
    def h_cost(self, s):
        path = []
        plan = AStar((s[0], s[1]), (self._e[0], self._e[1]), self._map_info, self.grid_step)
        if plan.run(display=False):
            path = plan.reconstruct_path()
        d = 0
        for i in range(len(path) - 1):
            d += self.distance(path[i], path[i + 1])
        return d

    #좌표들을 순서를 바꿔서 반환(시작부터로)
    def reconstruct_path(self):
        waypoint = []
        xs = []
        ys = []
        yaws = []
        pt = self._e
        while pt != self._s:
            waypoint.append(pt)
            pt = self._closeset[pt]['camefrom']
        for pt in waypoint[::-1]:
            x, y, yaw = self._closeset[pt]['path'][1]
            xs += x
            ys += y
            yaws += yaw
        return xs, ys, yaws
      
    def run(self, display=False):
        st = time.time()
        epsilon = 1.5
        d = self.h_cost(self._s)
        #openset ==> g: 현재노드 코스트 h : 휴리스틱 cost f = g+h camefrom = 부모노드 path = 부모노드에서 현재 노드로 어떻게 왔는지
        #self._openset[self._s] = {'g': 0, 'h': d, 'f': d, 'camefrom':None, 'path': []}
        self._openset[self._s] = {'g': 0, 'h': d, 'f': d, 'camefrom':None, 'path': [],'depth':0}
        
        while self._openset:
            #f 값이 가장 작은 openset 원소 == cost가 가장 낮은!
            x = min(self._openset, key=lambda key: self._openset[key]['f'])
            self._closeset[x] = self._openset.pop(x)
            #x를 pop 한 이후 close set에 넣어서 visited node 확인
            
            if display:
                self._map_info.close = (x[0], x[1])
            rspath = ReedsSheppPath(x, self._e, self._r)
            #x(좌표)를 시작점으로 하는 reed 클래스를 생성
            rspath.calc_paths()
            path, _ = rspath.get_shortest_path()
            #reed 클래스를 통해 가장 짧은 경로를 Dubins path 로 탐색
            xs, ys, yaws = ReedsSheppPath.gen_path(x, path, self._r, section=False, step_size = self.step)
            
            #현재 차의 방향과 도착지점의 방향이 같을때 직선 경로를 생성하는 코드 추가
            #현재 좌표에서 goal까지 직선 이동이 가능할 때 직선으로 이동
            if x[2] == self._e[2]:
                length = self.distance(x,self._e)
                pat = ['s',length]
                xx, yy, yaws2 = ReedsSheppPath.gen_path(x,[pat],self._r,section = False)
                if (xx[-1] == self._e[0] and yy[-1] == self._e[1]):
                    if not self.is_collision_rs_car(xx,yy,yaws2):
                        self._closeset[self._e] = {'camefrom':x , 'path' : [pat,[xx,yy,yaws2]]}
                        print("time:",time.time()-st)
                        print("depth:" , self._closeset[x]['depth'])
                        return True

            # 가장 짧은 Dubins path의 경로를 좌표경로로 반환
            if not self.is_collision_rs_car(xs, ys, yaws):
                #xs,ys,yaws 의 path 좌표가 충돌을 안한다면 현재 path로 결정
                self._closeset[self._e] = {'camefrom': x, 'path': [path, [xs, ys, yaws]]}
                print("time:" , time.time() - st)
                print("depth:" , self._closeset[x]['depth'])
                return True
            for y, path, line in self.neighbors(x):
                # 골 지점에 도착하지 않았다면 현재 좌표 x에서 neighbors 를 통해 자식 노드를 Span
                # STEP 사이즈에 따라 임의의 end point를 만들어서 진행 --> neighbor에서 총 6가지의 방법으로 span (l,s,r,-r,-s,-l)

                if display:
                    self._map_info.open = (y[0], y[1])
                #g = parent's g + x에서 현재까지 주행한 거리
                tentative_g_score = self._closeset[x]['g'] + (abs(path[1]) if path[0] == 's' else abs(path[1]) * self._r)
                if y in self._closeset:
                    continue
                if y not in self._openset:
                    tentative_is_better = True
                elif tentative_g_score < self._openset[y]['g']:
                    tentative_is_better = True
                else:
                    tentative_is_better = False
                if tentative_is_better:
                    # epsilon * h --> high quality
                    d = epsilon * self.h_cost(y)
                    '''
                    if self._closeset[x]['depth'] < d:
                        w = 1 - self._closeset[x]['depth']/d
                    else:
                        w = 0
                        
                    d = (1+epsilon*w)*d 
                    '''
                    #self._openset[y] = {'g': tentative_g_score, 'h': d, 'f': tentative_g_score+d, 'camefrom': x, 'path': [path, line]}
                    self._openset[y] = {'g': tentative_g_score, 'h': d, 'f': tentative_g_score+d, 'camefrom': x, 'path': [path, line],'depth' : self._closeset[x]['depth']+1}
        return False

def main1():
    m = MapInfo(200, 800)
    car = Car(50, 20)
    m.show()
    m.start = (100, 10, np.pi/2)
    m.end = (100, 500, np.pi/2)
    car.set_position(m.start)
    car.show()
    m.obstacle = [(20, i) for i in range(15)] + [(35, 30 - i) for i in range(15)]
    m.update()
    #input('enter to start ...')
    plan = HybridAStar(m.start, m.end, m, car, r=10.0)
    if plan.run(False):
        xs, ys, yaws = plan.reconstruct_path()
        m.path = list(zip(xs, ys))
        for i in range(len(xs)):
            if i != len(xs) - 1 and i % 10 != 0:
                continue
            plt.cla()
            m.show()
            #m.start = (10, 10, math.pi / 2)
            #m.end = (50, 30, math.pi / 2)
            #m.obstacle = [(20, i) for i in range(15)] + [(35, 30 - i) for i in range(15)]
            m.path = list(zip(xs, ys))
            car.set_position([xs[i], ys[i], yaws[i]])
            car.show()
            print(car._outline_x,car._outline_y)
            plt.pause(0.1)

    m.wait_close()

def main2():
    m = MapInfo(600, 400)
    car = Car(10.0, 5.0)
    start = (10, 25, 0)
    end = (450, 50, math.pi / 2)
    m.show()
    m.start = start
    m.end = end
    ob = [(40, i) for i in range(15)] + [(50, i) for i in range(15)] + [(i, 15) for i in range(40)]
    m.obstacle = ob
    car.set_position(m.start)
    car.show()
    m.update()
    input('enter to start ...')
    plan = HybridAStar(m.start, m.end, m, car, r=5.0)
    if plan.run(True):
        xs, ys, yaws = plan.reconstruct_path()
        m.path = list(zip(xs, ys))
        m.update()
        for i in range(len(xs)):
            if i != len(xs) - 1 and i % 10 != 0:
                continue
            plt.cla()
            m.show()
            m.start = start
            m.end = end
            m.obstacle = ob
            m.path = list(zip(xs, ys))
            car.set_position([xs[i], ys[i], yaws[i]])
            car.show()
            plt.pause(0.1)
    m.wait_close()
#직선주행에 취약함 --> 직선 주행을 어떻게 할지 생각해보자
def main3():
    m = MapInfo(60, 40)
    car = Car(10.0, 5.0)
    start = (10, 20, 0)
    end = (35, 5, 0)
    m.show()
    m.start = start
    m.end = end
    ob = [(30, i) for i in range(10)] + [(45, i) for i in range(10)] + [(i, 10) for i in range(31)] + [(i+45, 10) for i in range(15)]
    m.obstacle = ob
    car.set_position(m.start)
    car.show()
    m.update()
    #input('enter to start ...')
    plan = HybridAStar(m.start, m.end, m, car, r=5.0)
    
    plan.run(False)
    xs,ys,yaws = plan.reconstruct_path()
    '''
    if plan.run(False):
        xs, ys, yaws = plan.reconstruct_path()
        m.path = list(zip(xs, ys))
        m.update()
        for i in range(len(xs)):
            if i != len(xs) - 1 and i % 10 != 0:
                continue
            plt.cla()
            m.show()
            m.start = start
            m.end = end
            m.obstacle = ob
            m.path = list(zip(xs, ys))
            car.set_position([xs[i], ys[i], yaws[i]])
            car.show()
            plt.pause(0.1)
    m.wait_close()
    '''
if __name__ == "__main__":
    main1()