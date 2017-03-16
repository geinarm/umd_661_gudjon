import csv
import numpy as np

from collider import Collider

class WorkSpace:

	def __init__(self):
		self.obsticles = []


	def addObsticle(self, collider):
		self.obsticles.append(collider)


	def pointInCollision(self, point):
		for c in self.obsticles:
			dist = np.linalg.norm(c.center - point)
			if dist < c.radius:
				return True

		return False

	def readObsticles(self, filename):
		with open(filename, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',')
			for row in spamreader:
				x = float(row[0])
				y = float(row[1])
				r = float(row[2])

				c = Collider(np.array([x, y]), r)
				self.addObsticle(c)
