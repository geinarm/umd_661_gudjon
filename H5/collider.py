
import numpy as np
from shapely.geometry import Polygon, Point, LineString, MultiPoint
from shapely import affinity, geometry


class ShapeCollider(object):
	def __init__(self, shape):
		self.shape = shape


	def inCollision(self, other):
		return self.shape.intersects(other.shape)


	def getPoints(self):
		return np.array(list(self.shape.exterior.coords))


class CircleCollider(ShapeCollider):

	def __init__(self, center, radius):

		p = Point(center).buffer(radius)
		super(CircleCollider, self).__init__(p)


class PointCollider(ShapeCollider):

	def __init__(self, points, pos, theta):
		points = points + pos
		p = MultiPoint(points)
		p = affinity.rotate(p, theta, origin=(pos[0], pos[1]), use_radians=True)
		super(PointCollider, self).__init__(p)


class RectangleCollider(ShapeCollider):

	def __init__(self, center, width, height, theta):

		left = center[0] - width/2
		right = center[0] + width/2
		bottom = center[1] - height/2
		top = center[1] + height/2

		p = geometry.box(left, bottom, right, top)
		p = affinity.rotate(p, theta, origin='center', use_radians=True)
		super(RectangleCollider, self).__init__(p)


class TrajectoryCollider(ShapeCollider):
	def __init__(self, tj, width):

		points = tj.points[:, 0:2]
		shape = LineString(points)
		shape = shape.buffer(width/2, cap_style=2)

		super(TrajectoryCollider, self).__init__(shape)
		