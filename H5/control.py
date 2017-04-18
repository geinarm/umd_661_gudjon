
import math
import numpy as np

class Control(object):
	def __init__(self):
		pass


class SimpleCarControl(Control):

	def __init__(self, a, g):
		super(SimpleCarControl, self).__init__()

		self.acceleration = a
		self.steering = g


	def integrate(self, p, eps, dt=0.1):
		points = []
		dist = 0
		lastPosition = np.array([p[0], p[1]])
		itter = 0
		x = p[0]
		y = p[1]
		theta = p[2]
		v = p[3]
		w = p[4]

		while (dist < eps):
			itter += 1
			dx = math.cos(theta)*v
			dy = math.sin(theta)*v

			x = x + (dx*dt)
			y = y + (dy*dt)
			theta = (theta + (w*dt)) % (2*math.pi)
			v = v + (self.acceleration*dt)
			w = w + (self.steering*dt)

			v = min(max(v, 0.0), 5.0)
			w = min(max(-math.pi/2, w), math.pi/2)

			point = [x, y, theta, v, w]
			points.append(point)

			position = np.array([x, y])
			travel = math.sqrt((dx*dt)**2 + (dy*dt)**2)
			if travel == 0 and itter >10:
				break
			dist += travel
			lastPosition = position

		return np.array(points)
