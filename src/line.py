from graphic_object import GraphicObject
from point import Point
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene

class Line(GraphicObject):
	def __init__(self, point1: Point, point2: Point):
		super().__init__()
		self.point1 = point1
		self.point2 = point2

	#TODO: Draw with API
	def draw(self) -> None:
		print(f"Drawing a line from ({self.points[0].x}, {self.points[0].y}) to ({self.points[1].x}, {self.points[1].y})")
