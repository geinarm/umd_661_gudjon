
import numpy as np

from shapely import affinity
from shapely.geometry import Point, MultiPoint

from pyglet.gl import *

from trajectory import *


class Graphics(object):
	def __init__(self, scale=1):
		self.scale = scale

	def draw(self, batch):
		raise NotImplementedError()


class CircleGraphics(Graphics):
	def __init__(self, center, radius):
		self.shape = Point(center).buffer(radius)
		self.coords = np.array(list(self.shape.exterior.coords));
		super(CircleGraphics, self).__init__()

	def draw(self, batch, scale=1):
		coords = self.coords * scale
		verts = coords.flatten()
		batch.add(len(verts)/2, GL_POLYGON, pyglet.graphics.Group(), ('v2f', verts ))


class PointRobotGraphics(Graphics):
	def __init__(self, points, pos, theta):
		self.points = points
		self.pos = pos
		self.theta = theta
		super(PointRobotGraphics, self).__init__()

	def draw(self, batch, scale=1):
		shape = MultiPoint(self.points)
		shape = affinity.rotate(shape, self.theta, origin=(0,0), use_radians=True)
		for point in shape:
			point = point.buffer(0.1)
			coords = np.array(list(point.exterior.coords))
			coords = coords + self.pos
			coords = coords * scale

			verts = coords.flatten()
			batch.add(len(verts)/2, GL_POLYGON, pyglet.graphics.Group(), ('v2f', verts ))


class TrajectoryGraphics(Graphics):
	def __init__(self, tj, scale=1):
		super(TrajectoryGraphics, self).__init__(scale)

		if type(tj) == StraightLine:
			self.points = np.array([tj.start[0:2], tj.end[0:2]])

		elif type(tj) == Curve:
			self.points = tj.points[:,0:2]


	def draw(self, batch):
		points = self.points * self.scale
		verts = points.flatten()
		#batch.add(2, GL_LINES, pyglet.graphics.Group(), ('v2f', verts ))
		batch.add(len(verts)/2, GL_LINE_STRIP, pyglet.graphics.Group(), ('v2f', verts ))


class RobotGraphics(Graphics):
	def __init__(self, robot, scale=1):
		super(RobotGraphics, self).__init__(scale)

		self.robot = robot


	def draw(self, batch):
		if(type(self.robot) != PointRobot):
			points = self.robot.getPoints() * self.scale
			verts = points.flatten()
			robot.add(len(verts)/2, GL_LINE_LOOP, pyglet.graphics.Group(), ('v2f', verts ))
