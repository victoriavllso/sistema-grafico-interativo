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

		delta1 = 0.001
		delta2 = delta1**2
		delta3 = delta2 * delta1

		n = 1/delta1

		mbs = np.array([[-1/6, 3/6, -3/6, 1/6],
				 		[3/6, -6/6, 3/6, 0],
						[-3/6, 0, 3/6, 0],
						[1/6, 4/6, 1/6, 0]])

		d = np.array([[0, 0, 0, 1],
			   		[delta3, delta2, delta1, 0],
					[6*delta3, 2*delta2, 0, 0],
					[6*delta3, 0, 0, 0]])
		
		for i in range(0, len(self.points) - 3):
			gx = np.array([self.points[i].x, self.points[i+1].x, self.points[i+2].x, self.points[i+3].x])
			gy = np.array([self.points[i].y, self.points[i+1].y, self.points[i+2].y, self.points[i+3].y])
			cx = np.dot(mbs,gx)
			cy = np.dot(mbs, gy)
			dx = np.dot(d, cx)
			dy = np.dot(d,cy)
			curve = curve + self.draw_foward_differences(int(n), dx[0], dx[1],dx[2],dx[3],dy[0],dy[1],dy[2],dy[3])

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

	def draw_foward_differences(self,n ,x, dx,d2x,d3x,y,dy,d2y,d3y) -> list[Point]:
		curve = []

		x_old = x # guarda inicio do segmento de curva quando i=1
		y_old = y 
		i = 1

		while i < n:
			i+=1
			x += dx
			dx += d2x
			d2x += d3x
			y += dy
			dy += d2y
			d2y += d3y
			curve.append(Point(window=self.window, x=x_old, y=y_old))
			curve.append(Point(window=self.window, x=x, y=y))
			x_old, y_old = x, y

		return curve

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
		self.curve_points = self.calculate_bspline() # _--------------- to do

	def __str__(self):
		return f"BSpline: {self.name}, Points: {self.points}, Color: {self.color}"

	def get_points_obj(self):
		return self.points

	def get_type_obj(self):
		return super().get_type_obj()

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
