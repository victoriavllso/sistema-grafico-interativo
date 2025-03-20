from graphic_object import GraphicObject
from point import Point
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene, QGraphicsView
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QGraphicsLineItem

class Line(GraphicObject):
	def __init__(self, point1: Point, point2: Point, name: str =
		"Line"):
		super().__init__(name)
		self.point1 = point1
		self.point2 = point2

	def draw(self, scene: QGraphicsScene, viewport, window) -> None:
		# Transforma os pontos para a viewport
		transformed_p1 = viewport.transform(self.point1, window)
		transformed_p2 = viewport.transform(self.point2, window)

		# Cria um QGraphicsLineItem com os pontos transformados
		line_item = QGraphicsLineItem(transformed_p1.x, transformed_p1.y,
										transformed_p2.x, transformed_p2.y)

		line_item.setPen(pen)

		print("linha desenhada")