
import math
import numpy as np
import csv

from shapely.geometry import Point, Polygon
from shapely import affinity
from collider import ShapeCollider, PointCollider
from graphics import *
from trajectory import *
from control import SimpleCarControl

class Robot(object):

	def __init__(self):
		self.position = np.array([0,0])
		self.theta = 0
		#self.points = [[25, 0], [-10, -10], [-10, 10]]


	def setPosition(self, pos):
		self.position = pos

	def getPosition(self):
		return self.position


	def setOrientation(self, theta):
		self.theta = theta


	def getPoints(self):
		p = self.shape
		p = affinity.rotate(p, self.theta, origin=[0, 0], use_radians=True)

		coords = np.array(list(p.exterior.coords));
		coords = coords + self.position

		return coords


	def steer(self, p, q, eps):
		raise NotImplementedError()

	def extend(self, p, q, eps=None):
		raise NotImplementedError()		


	def getCollider(self):
		pass


	def setState(self, state):
		self.position = np.array([state[0], state[1]])


	def getDistance(self, p1, p2):
		return np.linalg.norm(p1-p2)


class PointRobot(Robot):

	def __init__(self):

		p = Point([0, 0])
		super(PointRobot, self).__init__(p)


	def getPoints(self):
		return self.position

	def getGraphics(self):
		return PointRobotGraphics(self, 1)

	def getCollider(self):
		p = Point(self.position)
		return ShapeCollider(p)


	def steer(self, p, q, eps=None):
		tj = StraightLine(p, q)
		return tj


	def extend(self, p, q, eps=None):
		if eps:
			v = q-p
			v = v/np.linalg.norm(v)
			v = v * eps
			return p + v
		else:
			return q


class PointCar(Robot):
	def __init__(self, pointFile):
		self.points = self.readPoints(pointFile)

		self.width = (self.points.max(0) - self.points.min(0))[1]

		super(PointCar, self).__init__()

	def setState(self, state):
		# x, y, theta, v, w
		self.position = np.array([state[0], state[1]])
		self.theta = state[2]
		self.velocity = state[3]
		self.angularVelocity = state[4]

	def getCollider(self):
		collider = PointCollider(self.points, self.position, self.theta)
		return collider

	def getWidth(self):
		return self.width

	def getGraphics(self):
		return PointRobotGraphics(self.points, self.position, self.theta)


	def steer(self, p, q, eps):
		v = p[3]
		target_v = q[3]
		v_err = target_v - v
		t = eps/((v+target_v)/2.0) #estimated time it takes to cover the distance

		a = (v_err/t)

		vr = np.array([q[0]-p[0], q[1]-p[1]])
		delta = math.atan2(vr[1], vr[0]) - p[2]
		if delta > math.pi:
			delta = delta - 2*math.pi
		elif delta < -math.pi:
			delta = delta + 2*math.pi
		gamma = (delta/t/t) - (p[4]/t)

		a = min(max(a, 0), 2)
		s = min(max(gamma, -math.pi/2), math.pi/2)

		#print(a, s)
		#print('eps', eps,'t', t, 'delta', delta, 'gamma', gamma)
		cmd = SimpleCarControl(a, s)
		points = cmd.integrate(p, eps)
		tj = Curve(points)
		tj.cmd = [a, s]
		return tj


	def extend(self, p, q, eps=None):
		if eps:
			dist = self.getDistance(p, q)
			t = eps/dist
			if t >= 1:
				return q

			z = p + t*(q-p)
			return z
		else:
			return q


	def getDistance(self, p1, p2, k_delta=1, k_phi=1):

		pos1 = np.array([p1[0], p1[1]])
		pos2 = np.array([p2[0], p2[1]])
		dist = np.linalg.norm(pos2-pos1)
		thetaErr = (p2[2]-p1[2]) % math.pi

		return dist + 2*thetaErr


	def readPoints(self, filename):
		points = []
		with open(filename, 'rb') as csvfile:
			csvReader = csv.reader(csvfile, delimiter=',')
			for row in csvReader:
				x = float(row[0])
				y = float(row[1])
				points.append([x, y])
		return np.array(points)

