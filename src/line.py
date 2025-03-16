from graphic_object import GraphicObject
from point import Point

class Line(GraphicObject):
	def __init__(self,x1,y1,x2,y2):
		self.point1 = Point(x1,y1)
		self.point2 = Point(x2,y2)

	def draw(self):
		pass