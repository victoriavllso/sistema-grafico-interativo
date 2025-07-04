from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.graphic_objects.point import Point
from PyQt6.QtCore import Qt
import numpy as np
from src.utils.utils import LINE_THICKNESS
from PyQt6.QtGui import QPen


class Bezier(GraphicObject):	
	def __init__(self, window, name, points: list[Point], color=Qt.GlobalColor.red):
		super().__init__(name, color, window)
		self.points = points # pontos de entrada
		self.curve_points = [] # pontos da curva
		self.points_draw = [] # pontos a serem desenhados

		for point in self.points:
			point.convert_coordinates()

		self.generate_curve_points()

	def calculate_bezier(self, point1: Point, point2: Point, point3: Point, point4: Point) -> list[Point]:
		"""Calcula os pontos da curva de bezier"""
		curve = []
		t = 0.0 # 1001 pontos gerados
		step = 0.001

		mb = np.array([ [-1,3,-3,1],  # matriz de Bernstein
			 [3,-6,3,0],
			 [-3,3,0,0],
			 [1,0,0,0] ])

		gbx = np.array([[point1.x], # matriz de geometria (pontos de controle)
			 [point2.x],
			 [point3.x],
			 [point4.x] ])

		gby = np.array([[point1.y], # matriz de geometria (pontos de controle)
			 [point2.y],
			 [point3.y],
			 [point4.y] ])
		
		
		point = Point(window=self.window, x=point1.x, y=point1.y)
		curve.append(point)

		while t <= 1.0:

			t += step
			mt = np.array([[t**3, t**2,t,1] ])
			mtmb = np.dot(mt, mb)
			x = np.dot(mtmb, gbx)[0][0] # Mb * G *T extrai o numero da matriz resultante
			y = np.dot(mtmb, gby)[0][0]
			point = Point(window=self.window, x=x, y=y)
			curve.append(point)

		point4 = Point(window=self.window, x=point4.x, y=point4.y)
		curve.append(point4)
		return curve

	def draw(self, painter, viewport) -> None:
		"""Desenha a curva de bezier na tela"""

		if len(self.curve_points) == 0:
			return

		transformed_points = [viewport.transform(p, self.window) for p in self.points_draw]
		painter.setPen(QPen(self.color, 2))

		for i in range(len(transformed_points) - 2):
			p1 = transformed_points[i]
			p2 = transformed_points[(i + 1)]
			painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))

	def generate_curve_points(self) -> list[Point]:
		"""Gera os pontos da curva de bezier"""
		if len(self.points) == 4:
			self.curve_points = self.calculate_bezier(self.points[0], self.points[1], self.points[2], self.points[3])
		else:
			self.curve_points = []
		
		return self.curve_points

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
	
	def receive_transform(self, matrix) -> None:
		"""Recebe a matriz de transformação e aplica aos pontos do objeto gráfico"""
		for point in self.points:
			point_matrix = np.array([point.x, point.y, 1])
			new_point = point_matrix @ matrix
			point.x = new_point[0]
			point.y = new_point[1]
		self.curve_points = self.calculate_bezier(self.points[0], self.points[1], self.points[2], self.points[3])

	def __str__(self):
		return f'Bezier {self.name} color {self.color}'

	def get_points_obj(self):
		"""Retorna os pontos do objeto gráfico em formato .obj"""
		return self.points

	def get_type_obj(self):
		"""Retorna o tipo do objeto gráfico"""
		return 'curve'
