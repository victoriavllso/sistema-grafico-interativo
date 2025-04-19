from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.graphic_objects.point import Point
from PyQt6.QtCore import Qt
import numpy as np

class Bezier(GraphicObject):	
	def __init__(self, window, name, points: list[Point], color=Qt.GlobalColor.red):
		super().__init__(name, color)
		self.points = points
		self.color = color
		self.window = window

		for point in self.points:
			point.convert_coordinates()


	def calculate_bezier(self):
		pass