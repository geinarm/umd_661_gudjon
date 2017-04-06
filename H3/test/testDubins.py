
import math
import numpy as np
from dubins import DubinsCalculator


calc = DubinsCalculator(2)

p = [10, 10, 0]

left = calc.getLeft(p)
right = calc.getRight(p)

print(left)
assert(left[0] == 10)
assert(left[1] == 12)

print(right)
assert(right[0] == 10)
assert(right[1] == 8)


c1 = np.array([2, 2])
c2 = np.array([10, 2])

T = calc.getTangentPoints(c1, c2, -1, -1)
print(T)

calc = DubinsCalculator(1)
p1 = np.array([0, 1])
p2 = np.array([1, 0])
center = np.array([0, 0])

l1 = calc.arcLength(center, p1, p2, False)
l2 = calc.arcLength(center, p1, p2, True)
print(l1)
print(l2)
assert(math.pi/2 - l1 < 0.01)
assert(math.pi*1.5 - l2 < 0.01)
