
import numpy as np
import math
from robot import TriangleRobot

robot = TriangleRobot()

p1 = np.array([0,0,0])
p2 = np.array([1,1,0])
dist = robot.getDistance(p1, p2)
print(dist)
assert (abs(dist-3.0) < 0.1)

p1 = np.array([0,1,0])
p2 = np.array([1,1,0])
dist = robot.getDistance(p1, p2)
print(dist)
assert (abs(dist-1.0) < 0.1)

p1 = np.array([2,1,0])
p2 = np.array([1,1,0])
dist = robot.getDistance(p1, p2)
print(dist)
assert (abs(dist-7.7) < 0.1)

p1 = np.array([1,1,0])
p2 = np.array([2,1, math.pi])
dist = robot.getDistance(p1, p2)
print(dist)
assert (abs(dist-4.1) < 0.1)

p1 = np.array([1,1, math.pi])
p2 = np.array([1,1.1, math.pi])
dist = robot.getDistance(p1, p2)
print(dist)
assert (abs(dist-4.1) < 0.1)

p1 = np.array([1,1, math.pi])
p2 = np.array([1,1.5, math.pi])
dist = robot.getDistance(p1, p2)
print(dist)
assert (abs(dist-4.2) < 0.1)