
import numpy as np
import pyglet
import collider
import math

from pyglet.gl import *

from WorkSpace import WorkSpace
from RRT import RRT
from robot import *
from graphics import *

CIRCLE_POINTS = 30

class WorkSpaceWindow(pyglet.window.Window):
	def __init__(self, ws, rrt, robot, width=800, height=600, scale=1):
		super(WorkSpaceWindow, self).__init__(width, height)
		self.workspace = ws
		self.graph = rrt
		self.robot = robot
		self.scale = scale
		self.set_caption('Work Space')

		self.updateGraph()


	def updateGraph(self):
		self.treeGraphics = []
		self.nodeGraphics = []
		for node in self.graph.nodes:
			if node.trajectory != None:
				self.treeGraphics.append(TrajectoryGraphics(node.trajectory, self.scale))
				self.robot.setState(node.point)
				self.nodeGraphics.append(self.robot.getGraphics())

		## Path
		self.pathLines = []
		success = self.graph.solution != None
		if success:
			n = self.graph.solution
			path_batch = pyglet.graphics.Batch()

			while n.parent != None:
				graphics = TrajectoryGraphics(n.trajectory, self.scale)
				self.pathLines.append(graphics)
				n = n.parent				


	def on_draw(self):
		glClearColor(240,240,240,255)
		glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
		glLineWidth(1)

		## Obstacles
		obstacle_batch = pyglet.graphics.Batch()
		for obsticle in self.workspace.obstacles:
			points = obsticle.getPoints() * self.scale
			verts = points.flatten()
			obstacle_batch.add(len(verts)/2, GL_POLYGON, pyglet.graphics.Group(), ('v2f', verts))
			
		## Draw Tree
		line_batch = pyglet.graphics.Batch()
		for g in self.treeGraphics:
			g.draw(line_batch)
		node_batch = pyglet.graphics.Batch()
		for g in self.nodeGraphics:
			g.draw(node_batch, self.scale)
				

		#Robot
		robot_batch = pyglet.graphics.Batch()
		self.robot.setState(self.graph.start)
		robotGraphics = self.robot.getGraphics()
		robotGraphics.draw(robot_batch, self.scale)

		## Path
		path_batch = pyglet.graphics.Batch()
		for tj in self.pathLines:
			tj.draw(path_batch)

		start = self.graph.start
		goal = self.graph.goal

		#if (type(self.robot) != PointRobot):
		#self.robot.setState(goal)
		#points = self.robot.getPoints() * self.scale
		#goalVerts = points.flatten()

		glColor3f(1,0,0)
		start_batch = pyglet.graphics.Batch()
		self.robot.setState(start)
		startGraphics = self.robot.getGraphics()
		startGraphics.draw(start_batch, self.scale)
		start_batch.draw()

		glColor3f(0.2,0.8,0.2)
		goal_batch = pyglet.graphics.Batch()
		self.robot.setState(goal)
		goalGraphics = CircleGraphics([goal[0], goal[1]], self.graph.goalRadius)
		goalGraphics.draw(goal_batch, self.scale)
		goal_batch.draw()

		#points = self.robot.getPoints() * self.scale
		#startVerts = points.flatten()			
		#else:
		#	goalVerts = self.makeCircle(goal[0], goal[1], self.graph.goalRadius)
		#	startVerts = self.makeCircle(start[0], start[1], 2)

		#glLineWidth(1)
		##Draw goal
		#glColor3f(0.1,0.5,0.1)
		#pyglet.graphics.draw(len(goalVerts)/2, GL_POLYGON, ('v2f', goalVerts))
		##Draw start
		#glColor3f(1,0,0)
		#pyglet.graphics.draw(len(startVerts)/2, GL_POLYGON, ('v2f', startVerts))
		
		glColor3f(1,0,0)
		line_batch.draw()

		glColor3f(0,1,0)
		glLineWidth(3)
		path_batch.draw()

		glColor3f(0.3,0.3,0.3)
		node_batch.draw()

		glColor3f(0,0,1)
		obstacle_batch.draw()

		#glColor3f(0.5,0.5,0.5)
		#glLineWidth(1)
		#robot_batch.draw()


	def makeCircle(self, px, py, r):
		verts = []
		r = r * self.scale
		for i in range(CIRCLE_POINTS):
			angle = math.radians(float(i)/CIRCLE_POINTS * 360.0)
			x = r*math.cos(angle) + px
			y = r*math.sin(angle) + py
			verts += [x,y]
		
		return verts


if __name__ == '__main__':


	##Problem1
	#start = np.array([80, 60, math.pi, 0, 0])
	#goal = np.array([0, 0, 0, 1, 0])
	#goalRadius = 20
	#eps = 5.0
	#filename = 'P1_path.csv'

	##Problem2
	#start = np.array([5, 60, 0, 0, 0])
	#goal = np.array([100, 60, 0, 0, 0])
	#goalRadius = 20
	#eps = 10.0
	#filename = 'P2_path.csv'

	##Problem3
	#start = np.array([10, 90, 3*math.pi/2, 0, 0])
	#goal = np.array([100, 90, 0, 0, 0])
	#goalRadius = 10
	#eps = 5.0
	#filename = 'P3_path.csv'

	##Problem4
	#start = np.array([63, 80, math.pi/2, 0, 0])
	#goal = np.array([60, 10, 0, 0, 0])
	#goalRadius = 10
	#eps = 10.0
	#filename = 'P4_path.csv'

	##Problem5
	start = np.array([40, 40, math.pi/4, 0, 0])
	goal = np.array([0, 0, 0, 0, 0])
	goalRadius = 20
	eps = 20.0
	filename = 'P5_path.csv'


	robot = PointCar('H5_robot.txt')
	limits = [[0,100], [0, 100], [0, 2*math.pi], [0, 5], [-math.pi/2, math.pi/2]]

	##Polygon robot
	#limits = [[0,100], [0, 100], [0, 2*math.pi]]
	#robot = PointRobot()
	#start = np.array([91, 39, 4.7])
	#goal = np.array([62, 55, 1.5])
	#goal = np.array([60, 10, 3.1])
	#goalRadius = 2.0
	#eps = 15.0

	ws = WorkSpace(limits)
	ws.readCircleObstacles('obstaclesH4.txt')
	#ws.readRectangleObstacles('rect.csv')

	rrt = RRT(ws, eps, goalRadius, limits)
	
	goalNode = rrt.findPath(start, goal, robot, maxNodes=500)
	if goalNode:
		plan = goalNode.getPlan()

		with open('solutions/'+filename, 'w+') as f:
			f.seek(0)
			for i in xrange(len(plan)):
				p = plan[i].trajectory.start
				cmd = plan[i].trajectory.cmd
				f.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(i, p[0], p[1], p[2], p[3], p[4], cmd[0], cmd[1]))
			f.truncate()

	window = WorkSpaceWindow(ws, rrt, robot, width=800, height=800, scale=8)

	pyglet.app.run()