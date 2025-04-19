from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.graphic_objects.point import Point
from PyQt6.QtCore import Qt
import numpy as np
from src.utils.utils import LINE_THICKNESS
from PyQt6.QtGui import QPen


class Bezier(GraphicObject):	
	def __init__(self, window, name, points: list[Point], color=Qt.GlobalColor.red):
		super().__init__(name, color)
		self.points = points
		self.color = color
		self.window = window

		for point in self.points:
			point.convert_coordinates()


	def calculate_bezier(self, point1: Point, point2: Point, point3: Point, point4: Point):
		
		curve = []
		t = 0.0 # 1001 pontos gerador
		step = 0.001

		mb = [ [-1,3,-3,1],  # matriz de Bernstein
			 [3,-6,3,0],
			 [-3,3,0,0],
			 [1,0,0,0] ]

		gbx = [[point1.x], # matriz de geometria (pontos de controle)
			 [point2.x],
			 [point3.x],
			 [point4.x] ]

		gby = [[point1.y], # matriz de geometria (pontos de controle)
			 [point2.y],
			 [point3.y],
			 [point4.y] ]
		
		
		point = Point(window=self.window, x=point1.x, y=point1.y)
		curve.append(point)

		while t <= 1.0:

			t += step
			mt = [[t**3], # matriz de tempo
				 [t**2],
				 [t],
				 [1] ]
			mtmb = np.dot(mt, mb)
			x = np.dot(mtmb, gbx)[0][0] # Mb * G *T extrai o numero da matriz resultante
			y = np.dot(mtmb, gby)[0][0]
			point = Point(window=self.window, x=x, y=y)
			curve.append(point)

		point4 = Point(window=self.window, x=point4.x, y=point4.y)
		curve.append(point4)
		return curve

	def draw(self, painter, viewport):
		for point in self.points:
			if not point.inside_window:
				return

		# Converte os pontos para o sistema de coordenadas da viewport
		transformed_points = [viewport.transform(p, self.window) for p in self.points]
		painter.setPen(Qpen(self.color, LINE_THICKNESS))

		for i in range(len(transformed_points)):
			p1 = transformed_points[i]
			p2 = transformed_points[(i + 1) % len(transformed_points)]
			painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))

	def geometric_center(self):
		x_center = 0
		y_center = 0
		for p in self.points:
			x_center += p.x
			y_center += p.y
		x_center /= len(self.points)
		y_center /= len(self.points)
		return int(x_center), int(y_center)