from graphic_object import GraphicObject
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene, QGraphicsView
from PyQt6.QtGui import QPen

class Point(GraphicObject):
	def __init__(self, x: int, y: int, name: str = "Point"):
		super().__init__(name)
		self.x = x
		self.y = y
	
	def draw(self, scene: QGraphicsScene, window, viewport):
		# Aplica a transformação para obter a posição correta na viewport

		# transformed_point = viewport.transform(self, window)
		radius = 3
		#painter.setBru?sh(QBrush(Qt.GlobalColor.blue)
		# point_item = QGraphicsEllipseItem(transformed_point.x - radius, transformed_point.y - radius, 2 * radius, 2 * radius)
		point_item = QGraphicsEllipseItem(self.x - radius, self.y - radius, 2 * radius, 2 * radius)
		pen = QPen(Qt.GlobalColor.blue)
		point_item.setPen(pen)
		scene.addItem(point_item)
		print("ponto desenhado")
