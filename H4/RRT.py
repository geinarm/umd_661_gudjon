import numpy as np
import random

from WorkSpace import WorkSpace
from collider import *

class Node:

	def __init__(self, point, parent, tj=None):
		self.parent = parent
		self.point = point
		self.trajectory = tj


	def getPlan(self):
		plan = []
		n = self
		while(n.parent != None):
			plan.append(n)
			n = n.parent

		plan.reverse()
		return plan


class RRT:

	def __init__(self, ws, eps, goalR, limits):
		self.ws = ws
		self.epsilon = eps
		self.goalRadius = goalR
		self.limits = limits
		self.dimentions = len(limits)


	def closestNode(self, point, robot, theshold=0):
		minDist = 99999
		closest = None
		for node in self.nodes:
			#dist = np.linalg.norm(point-node.point)
			dist = robot.getDistance(node.point, point)
			if dist < theshold:
				continue
			if dist < minDist:
				closest = node
				minDist = dist

		return closest


	def inGoalRegion(self, node, robot):
		pos1 = node.point[0:2]
		pos2 = self.goal[0:2]
		dist = np.linalg.norm(pos1-pos2)
		return (dist < self.goalRadius)


	def findPath(self, start, goal, robot, maxNodes=1000, maxSamples=10000):
		self.nodes = []
		self.start = start
		self.goal = goal
		self.solution = None

		self.nodes.append(Node(start, None))
		done = False

		#MyRand = [ [20, 80, 4], [70, 50, 5], [75, 30, 4] ]
		#ri = 0
		ng = 0
		samples = 0
		while len(self.nodes) < maxNodes and samples < maxSamples:
			numNodes = len(self.nodes)
			pg = (float(numNodes)/maxNodes) * 0.1
			useGoal = False
			##Pick random point
			if random.random() > (1.0-pg):
				ng += 1
				#print('Use goal', ng)
				useGoal = True
				point = goal
			else:
				values = []
				for i in range(self.dimentions):
					val = random.uniform(self.limits[i][0], self.limits[i][1])
					values.append(val)
				point = np.array(values)

			samples += 1
			##Find closest node
			n = self.closestNode(point, robot)

			##Extend node towards sample point
			goalDist = robot.getDistance(n.point, goal)
			z = robot.extend(n.point, point, self.epsilon)
			eps = min(goalDist, self.epsilon)
			trajectory = robot.steer(n.point, z, eps)

			if trajectory == None:
				continue
			newNode = Node(trajectory.end, n, trajectory)

			##Check for collision
			if not self.ws.pointInBounds(newNode.point):
				continue

			robot.setState(newNode.point)
			collider = robot.getCollider()
			if self.ws.inCollision(collider):
				continue
			pathCollider = TrajectoryCollider(trajectory, 0.01)
			if self.ws.inCollision(pathCollider):
				continue

			##Add new node
			self.nodes.append(newNode)
			#print(newNode.point)

			##Check goal
			if self.inGoalRegion(newNode, robot):
				print('Success')
				self.solution = newNode
				return newNode

		print('Failed')


if __name__ == '__main__':

	ws = WorkSpace()
	ws.readObsticles('obsticles1.csv')

	rrt = RRT(ws, 30, 20)
	rrt.findPath(np.array([10, 10]), np.array([400, 400]))
