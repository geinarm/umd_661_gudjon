
import numpy as np

from shapely.geometry import Point, Polygon
from shapely import affinity
from collider import ShapeCollider

class Robot:

	def __init__(self, shape):
		self.position = [0,0]
		self.theta = 0
		self.points = [[25, 0], [-10, -10], [-10, 10]]


	def setPosition(self, pos):
		self.position = pos


	def setOrientation(self, theta):
		self.theta = theta


	def setState(self, state):
		self.position = [state[0], state[1]]
		self.theta = state[2]


	def getPoints(self):
		p = Polygon(self.points)
		p = affinity.rotate(p, self.theta, origin=[0, 0], use_radians=True)

		coords = np.array(list(p.exterior.coords));
		coords = coords + self.position

		return coords


	def getCollider(self):
		coords = self.getPoints()
		p = Polygon(coords)
		return ShapeCollider(p)


class PointRobot(Robot):
	def __init__(self):

		p = Point([0, 0])
		super(PointRobot, self).__init__(p)


class TriangleRobot(Robot):
	def __init__(self):

		p = Point([0, 0])
		super(PointRobot, self).__init__(p)