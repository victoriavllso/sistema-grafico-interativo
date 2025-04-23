from src.model.graphic_objects.graphic_object import GraphicObject
from PyQt6.QtCore import Qt
from src.model.graphic_objects.point import Point
import numpy as np

class BSpline(GraphicObject):
	def __init__(self, window, name, points: list[Point], color=Qt.GlobalColor.red):
		super().__init__(name, color, window)
		self.points = points # pontos de entrada
		self.curve_points = [] # pontos da curva
		self.points_draw = [] # pontos a serem desenhados

		for point in self.points:
			point.convert_coordinates()

		self.generate_curve_points()

	def calculate_bspline(self, points: list[Point], degree: int):
		pass



	def draw(self, painter, viewport):
		pass


	def receive_transform(self, matrix):
		for point in self.points:
			point_matrix = np.array([point.x, point.y, 1])
			new_point = point_matrix @ matrix
			point.x = new_point[0]
			point.y = new_point[1]
		self.curve_points = self.calculate_bspline() # _--------------- to do

	def __str__(self):
		return f"BSpline: {self.name}, Points: {self.points}, Color: {self.color}"

	def get_points_obj(self):
		return self.points


	def get_type_obj(self):
		return super().get_type_obj()
	