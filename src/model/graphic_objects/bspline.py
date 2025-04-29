from src.model.graphic_objects.graphic_object import GraphicObject
from PyQt6.QtCore import Qt
from src.model.graphic_objects.point import Point
import numpy as np
from src.utils.utils import LINE_THICKNESS
from PyQt6.QtGui import QPen

class BSpline(GraphicObject):
	def __init__(self, window, name, points: list[Point], color=Qt.GlobalColor.red):
		super().__init__(name, color, window)
		self.points = points # pontos de entrada
		self.curve_points = [] # pontos da curva
		self.points_draw = [] # pontos a serem desenhados

		for point in self.points:
			point.convert_coordinates()

		self.generate_curve_points()


	def calculate_bspline(self) -> list[Point]:
		curve= []

		delta_t = 0.01
	

		n = int(1/delta_t)

		M =  (1/6) * np.array([
            [-1,  3, -3,  1],
            [ 3, -6,  3,  0],
            [-3,  0,  3,  0],
            [ 1,  4,  1,  0]
        ])


		
		for i in range(0, len(self.points) - 3):
			# gera os pontos de controle
			Px = np.array([p.x for p in self.points[i:i+4]])
			Py = np.array([p.y for p in self.points[i:i+4]])

			# coeficientes da curva
			Cx = M @ Px
			Cy = M @ Py

			# diferenças progressivas

			x = Cx[3]
			dx = Cx[2]*delta_t + Cx[1]*delta_t**2 + Cx[0]*delta_t**3
			d2x = 2*Cx[1]*delta_t**2 + 6*Cx[0]*delta_t**3
			d3x = 6*Cx[0]*delta_t**3

			y = Cy[3]  # termo constante (d)
			dy = Cy[2]*delta_t + Cy[1]*delta_t**2 + Cy[0]*delta_t**3
			d2y = 2*Cy[1]*delta_t**2 + 6*Cy[0]*delta_t**3
			d3y = 6*Cy[0]*delta_t**3

			segment_points = []
			# gera pontos pra esse segmento
			
			for _ in range(n):
				segment_points.append(Point(window=self.window, x=x, y=y))
				x += dx
				dx += d2x
				d2x += d3x
				y += dy
				dy += d2y
				d2y += d3y
			curve.extend(segment_points)

		return curve
	
	def draw(self, painter, viewport) -> None:
		"""Desenha a curva bspline"""
		if len(self.curve_points) == 0:
			return
		
		transformed_points = [viewport.transform(p, self.window) for p in self.points_draw]
		painter.setPen(QPen(self.color, 2))

		for i in range(len(transformed_points) - 2):
			p1 = transformed_points[i]
			p2 = transformed_points[(i + 1)]
			painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))

	def generate_curve_points(self) -> list[Point]:
		"""Gera os pontos da curva bspline"""
		self.curve_points = self.calculate_bspline()

	def receive_transform(self, matrix) -> None:
		"""Recebe a matriz de transformacao e aplica aos pontos"""
		for point in self.points:
			point_matrix = np.array([point.x, point.y, 1])
			new_point = point_matrix @ matrix
			point.x = new_point[0]
			point.y = new_point[1]
		self.curve_points = self.calculate_bspline()

	def __str__(self):
		return f"BSpline: {self.name}, Points: {self.points}, Color: {self.color}"

	def get_points_obj(self):
		return self.points

	def get_type_obj(self):
		return 'curve_spline'

	def geometric_center(self) -> tuple[int, int]:
		"""Calcula o centro geometrico do objeto grafico"""
		x_center = 0
		y_center = 0
		for p in self.points:
			x_center += p.x
			y_center += p.y
		x_center /= len(self.points)
		y_center /= len(self.points)
		return int(x_center), int(y_center)
