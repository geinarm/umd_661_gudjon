
import math
import numpy as np

class Control(object):
	def __init__(self):
		pass


class SimpleCarControl(Control):

	def __init__(self, w, v, t):
		super(SimpleCarControl, self).__init__()

		self.w = w
		self.velocity = v
		self.time = t


	def integrate(self, p, dt):
		
		steps = int(self.time/dt)
		points = []

		x = p[0]
		y = p[1]
		theta = p[2]

		for i in xrange(steps):
			dx = math.cos(theta)
			dy = math.sin(theta)
			dtheta = self.w

			x = x + (dx*dt*self.velocity)
			y = y + (dy*dt*self.velocity)
			theta = (theta + (dtheta*dt)) % (2*math.pi)

			point = [x, y, theta]
			points.append(point)

		return np.array(points)
