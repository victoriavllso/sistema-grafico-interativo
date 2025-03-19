from graphic_object import GraphicObject
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene

class Point(GraphicObject):
	def __init__(self, x: int, y: int):
		super().__init__()
		self.x = x
		self.y = y
	
	#TODO: Draw with API
	def draw(self, scene: QGraphicsScene):
		print(f"Drawing a point at ({self.x}, {self.y})") # Debugging
		radius = 3
		ellipse = QGraphicsEllipseItem(self.x - radius, self.y - radius, 2 * radius, 2 * radius)
		ellipse.setBrush(QBrush(Qt.GlobalColor.black))
		scene.addItem(ellipse)
		print(f"point ({self.x}, {self.y}) drawn") # Debugging
