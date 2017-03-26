
import numpy as np
import pyglet
import collider
import math

from pyglet.gl import *

from WorkSpace import WorkSpace
from RRT import RRT
from robot import Robot

CIRCLE_POINTS = 30

class WorkSpaceWindow(pyglet.window.Window):
	def __init__(self, ws, rrt, robot, width=800, height=600):
		super(WorkSpaceWindow, self).__init__(width, height)
		self.workspace = ws
		self.graph = rrt
		self.robot = robot
		self.set_caption('Work Space')


	def on_draw(self):
		glClearColor(240,240,240,255)
		glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)

		## Obstacles
		obstacle_batch = pyglet.graphics.Batch()
		for obsticle in self.workspace.obstacles:
			verts = obsticle.getPoints().flatten()
			obstacle_batch.add(len(verts)/2, GL_POLYGON, pyglet.graphics.Group(), ('v2f', verts))
			
		## Tree Lines
		line_batch = pyglet.graphics.Batch()
		for node in self.graph.nodes:
			if node.parent != None:
				x1 = node.point[0]
				y1 = node.point[1]
				x2 = node.parent.point[0]
				y2 = node.parent.point[1]
				line_batch.add(2, GL_LINES, pyglet.graphics.Group(), ('v2f', (x1, y1, x2, y2) ))

		#Robot
		robot_batch = pyglet.graphics.Batch()
		self.robot.setState(self.graph.start)
		verts = self.robot.getPoints().flatten()
		robot_batch.add(len(verts)/2, GL_LINE_LOOP, pyglet.graphics.Group(), ('v2f', verts ))

		## Path
		success = self.graph.solution != None
		if success:
			n = self.graph.solution
			path_batch = pyglet.graphics.Batch()

			while n.parent != None:
				x1 = n.point[0]
				y1 = n.point[1]
				x2 = n.parent.point[0]
				y2 = n.parent.point[1]
				path_batch.add(2, GL_LINES, None, ('v2f', (x1, y1, x2, y2) ))

				self.robot.setState(n.point)
				verts = self.robot.getPoints().flatten()
				robot_batch.add(len(verts)/2, GL_LINE_LOOP, pyglet.graphics.Group(), ('v2f', verts ))

				n = n.parent


		start = self.graph.start
		goal = self.graph.goal

		## Draw
		glColor3f(0.1,0.5,0.1)
		pyglet.graphics.draw(CIRCLE_POINTS, GL_POLYGON, ('v2f', self.makeCircle(goal[0], goal[1], self.graph.goalRadius)))
		glColor3f(1,0,0)
		pyglet.graphics.draw(CIRCLE_POINTS, GL_POLYGON, ('v2f', self.makeCircle(start[0], start[1], 5)))
		
		line_batch.draw()
		glColor3f(0,0,1)
		obstacle_batch.draw()
		
		if success:
			glColor3f(0,1,0)
			glLineWidth(3)
			path_batch.draw()
			glColor3f(0.5,0.5,0.5)
			glLineWidth(1)
			robot_batch.draw()


	def makeCircle(self, px, py, r):
		verts = []
		for i in range(CIRCLE_POINTS):
			angle = math.radians(float(i)/CIRCLE_POINTS * 360.0)
			x = r*math.cos(angle) + px
			y = r*math.sin(angle) + py
			verts += [x,y]
		
		return verts


if __name__ == '__main__':
	ws = WorkSpace()
	ws.readCircleObstacles('obsticles1.csv')
	ws.readRectangleObstacles('rect.csv')

	start = np.array([15, 15, 0])
	goal = np.array([400, 500, 0])
	limits = [[0,800], [0, 600], [0, math.pi]]
	rrt = RRT(ws, 15, 20, limits)
	robot = Robot()
	goalNode = rrt.findPath(start, goal, robot)

	window = WorkSpaceWindow(ws, rrt, robot)

	pyglet.app.run()