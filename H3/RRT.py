import numpy as np
import random

from WorkSpace import WorkSpace

class Node:

	def __init__(self, point, parent):
		self.parent = parent
		self.point = point


class RRT:

	def __init__(self, ws, eps, goalR, limits):
		self.ws = ws
		self.epsilon = eps
		self.goalRadius = goalR
		self.limits = limits
		self.dimentions = len(limits)


	def closestNode(self, point):
		minDist = 9999
		closest = None
		for node in self.nodes:
			dist = np.linalg.norm(point-node.point)
			if dist < minDist:
				minDist = dist
				closest = node

		return closest


	def inGoalRegion(self, node):
		dist = np.linalg.norm(node.point-self.goal)
		return dist < self.goalRadius


	def findPath(self, start, goal, robot, maxNodes=1000):
		self.nodes = []
		self.start = start
		self.goal = goal
		self.solution = None

		self.nodes.append(Node(start, None))
		done = False
		

		while len(self.nodes) < maxNodes:
			##Pick random point
			if random.random() > 0.95:
				point = goal
			else:
				values = []
				for i in range(self.dimentions):
					val = random.uniform(self.limits[i][0], self.limits[i][1])
					values.append(val)
				point = np.array(values)

			##Find closest node
			n = self.closestNode(point)

			##Push back to max reach
			v = point-n.point
			v = v/np.linalg.norm(v)
			point = n.point+v*self.epsilon

			##Check for collision
			robot.setState(point)
			collider = robot.getCollider()

			#if not self.ws.pointInCollision(point):
			if not self.ws.inCollision(collider):
				##Add new node
				newNode = Node(point, n)
				self.nodes.append(newNode)

				##Check goal
				if self.inGoalRegion(newNode):
					print('Success')
					self.solution = newNode
					return newNode

		print('Failed')


if __name__ == '__main__':

	ws = WorkSpace()
	ws.readObsticles('obsticles1.csv')

	rrt = RRT(ws, 30, 20)
	rrt.findPath(np.array([10, 10]), np.array([400, 400]))
