
import numpy as np
import pyglet
from pyglet.gl import *
from math import *

from WorkSpace import WorkSpace
from RRT import RRT

CIRCLE_POINTS = 30

class WorkSpaceWindow(pyglet.window.Window):
	def __init__(self, ws, rrt, width=800, height=600):
		super(WorkSpaceWindow, self).__init__(width, height)
		self.workspace = ws
		self.graph = rrt
		self.label = pyglet.text.Label('Work Space')
		self.goalNode = None


	def on_draw(self):
		glClearColor(240,240,240,255)
		glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)

		## Obsticles
		obsticle_batch = pyglet.graphics.Batch()
		for obj in self.workspace.obsticles:
			verts = self.makeCircle(obj.center[0], obj.center[1], obj.radius)
			obsticle_batch.add(CIRCLE_POINTS, GL_POLYGON, pyglet.graphics.Group(), ('v2f', verts))
			

		## Tree Lines
		line_batch = pyglet.graphics.Batch()
		for node in self.graph.nodes:
			if node.parent != None:
				x1 = node.point[0]
				y1 = node.point[1]
				x2 = node.parent.point[0]
				y2 = node.parent.point[1]
				line_batch.add(2, GL_LINES, pyglet.graphics.Group(), ('v2f', (x1, y1, x2, y2) ))

		## Path
		n = self.graph.solution
		path_batch = pyglet.graphics.Batch()
		while n.parent != None:
			x1 = n.point[0]
			y1 = n.point[1]
			x2 = n.parent.point[0]
			y2 = n.parent.point[1]
			path_batch.add(2, GL_LINES, None, ('v2f', (x1, y1, x2, y2) ))
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
		obsticle_batch.draw()
		glColor3f(0,1,0)
		path_batch.draw()


	def makeCircle(self, px, py, r):
		verts = []
		for i in range(CIRCLE_POINTS):
			angle = radians(float(i)/CIRCLE_POINTS * 360.0)
			x = r*cos(angle) + px
			y = r*sin(angle) + py
			verts += [x,y]
		
		return verts
		#return pyglet.graphics.vertex_list(CIRCLE_POINTS, ('v2f', verts))



if __name__ == '__main__':
	ws = WorkSpace()
	ws.readObsticles('obsticles1.csv')

	rrt = RRT(ws, 15, 20, [[0,800], [0, 600]])
	goalNode = rrt.findPath(np.array([10, 10]), np.array([400, 400]))

	window = WorkSpaceWindow(ws, rrt)

	pyglet.app.run()