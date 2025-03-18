from graphic_object import GraphicObject
from point import Point
from utils import BLACK_RGB

class Line(GraphicObject):
	def __init__(self, point1: Point, point2: Point, color= BLACK_RGB) -> None:
		self.point1 = point1
		self.point2 = point2
		self.color = color

	def draw(self) -> None:
		print(f"Drawing a line from ({self.points[0].x}, {self.points[0].y}) to ({self.points[1].x}, {self.points[1].y})")
