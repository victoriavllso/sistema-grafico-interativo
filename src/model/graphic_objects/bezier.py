from src.model.graphic_objects.graphic_object import GraphicObject
from src.model.graphic_objects.point import Point
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen
import numpy as np
from src.utils.utils import LINE_THICKNESS


class Bezier(GraphicObject):	
	def __init__(self, window, name, points: list[Point], color=Qt.GlobalColor.red):
		super().__init__(name, color, window)
		self.points = points
		self.curve_points = []
		self.points_draw = []

		for point in self.points:
			point.convert_coordinates()

		self.generate_curve_points()

	def calculate_bezier(self, p1: Point, p2: Point, p3: Point, p4: Point) -> list[Point]:
		curve = []
		t = 0.0
		step = 0.001

		mb = np.array([[-1, 3, -3, 1],
		               [3, -6, 3, 0],
		               [-3, 3, 0, 0],
		               [1, 0, 0, 0]])

		gbx = np.array([[p1.x], [p2.x], [p3.x], [p4.x]])
		gby = np.array([[p1.y], [p2.y], [p3.y], [p4.y]])
		gbz = np.array([[p1.z], [p2.z], [p3.z], [p4.z]])

		while t <= 1.0:
			mt = np.array([[t**3, t**2, t, 1]])
			mtmb = np.dot(mt, mb)

			x = float(np.dot(mtmb, gbx))
			y = float(np.dot(mtmb, gby))
			z = float(np.dot(mtmb, gbz))
			point = Point(window=self.window, x=x, y=y, z=z)
			curve.append(point)

			t += step

		return curve

	def draw(self, painter, viewport) -> None:
		if not self.curve_points:
			return

		transformed_points = [viewport.transform(p, self.window) for p in self.curve_points]
		painter.setPen(QPen(self.color, 2))

		for i in range(len(transformed_points) - 1):
			p1 = transformed_points[i]
			p2 = transformed_points[i + 1]
			painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))

	def generate_curve_points(self) -> list[Point]:
		if len(self.points) == 4:
			self.curve_points = self.calculate_bezier(*self.points)
		else:
			self.curve_points = []
		return self.curve_points

	def geometric_center(self) -> tuple[int, int, int]:
		x = sum(p.x for p in self.points) / len(self.points)
		y = sum(p.y for p in self.points) / len(self.points)
		z = sum(p.z for p in self.points) / len(self.points)
		return int(x), int(y), int(z)

	def receive_transform(self, matrix: np.ndarray) -> None:
		for point in self.points:
			vec = np.array([point.x, point.y, point.z, 1])
			new_point = matrix @ vec
			point.x, point.y, point.z = new_point[:3]

		self.curve_points = self.calculate_bezier(*self.points)

	def __str__(self):
		return f'Bezier {self.name} color {self.color}'

	def get_points_obj(self):
		return self.points

	def get_type_obj(self):
		return 'curve'
