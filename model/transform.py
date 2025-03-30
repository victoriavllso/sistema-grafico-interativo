import numpy as np
from model.point import Point
from model.line import Line
from model.wireframe import Wireframe

class Transform:
	def __init__(self):
		pass

	# homogeneous coordinates systems
	def matrix_translate(self, dx, dy):
		
		matrix_translate = [[1, 0, 0],
							[0, 1, 0],
							[dx, dy, 1]]
		return matrix_translate
	
	def matrix_scale(self,sx, sy):
	
		matrix_scale = [[sx, 0, 0],
						[0, sy, 0],
						[0, 0, 1]]
		return matrix_scale
	
	def matrix_rotate(self, angle):
		
		matrix_rotate = [[np.cos(angle), -np.sin(angle), 0],
						 [np.sin(angle), np.cos(angle), 0],
						 [0, 0, 1]]
		return matrix_rotate
	
	# methods to transform objects
	def translate_object(self, object,dx ,dy):
		result = self.matrix_translate(dx, dy)

		if isinstance(object, Point):
			point_matrix = np.array([object.x, object.y, 1])
			new_point = np.dot(point_matrix, result)
			object.x = new_point[0]
			object.y = new_point[1]
		elif isinstance(object, Line):
			point1_matrix = np.array([object.point1.x, object.point1.y, 1])
			new_point1 = np.dot(point1_matrix, result)
			object.point1.x = new_point1[0]
			object.point1.y = new_point1[1]

			point2_matrix = np.array([object.point2.x, object.point2.y, 1])
			new_point2 = np.dot(point2_matrix, result)
			object.point2.x = new_point2[0]
			object.point2.y = new_point2[1]
		elif isinstance(object, Wireframe):
			for point in object.points:
				point_matrix = np.array([point.x, point.y, 1])
				new_point = np.dot(point_matrix, result)
				point.x = new_point[0]
				point.y = new_point[1]
		else:
			print("Objeto não suportado para translação.")


	def scale_object(self,object,sx, sy):
		obj_center = object.geometric_center()
		cx, cy = obj_center[0], obj_center[1]

		if isinstance(object, Point):
			point_matrix = np.array([object.x, object.y, 1])
			new_point = np.dot(point_matrix, self.matrix_translate(-cx, -cy))
			new_point = np.dot(new_point, self.matrix_scale(sx, sy))
			new_point = np.dot(new_point, self.matrix_translate(cx, cy))
			object.x = new_point[0]
			object.y = new_point[1]
		elif isinstance(object, Line):
			point1_matrix = np.array([object.point1.x, object.point1.y, 1])
			new_point1 = np.dot(point1_matrix, self.matrix_translate(-cx, -cy))
			new_point1 = np.dot(new_point1, self.matrix_scale(sx, sy))
			new_point1 = np.dot(new_point1, self.matrix_translate(cx, cy))
			object.point1.x = new_point1[0]
			object.point1.y = new_point1[1]
			point2_matrix = np.array([object.point2.x, object.point2.y, 1])
			new_point2 = np.dot(point2_matrix, self.matrix_translate(-cx, -cy))
			new_point2 = np.dot(new_point2, self.matrix_scale(sx, sy))
			new_point2 = np.dot(new_point2, self.matrix_translate(cx, cy))
			object.point2.x = new_point2[0]
			object.point2.y = new_point2[1]
		elif isinstance(object, Wireframe):
			for point in object.points:
				point_matrix = np.array([point.x, point.y, 1])
				new_point = np.dot(point_matrix, self.matrix_translate(-cx, -cy))
				new_point = np.dot(new_point, self.matrix_scale(sx, sy))
				new_point = np.dot(new_point, self.matrix_translate(cx, cy))
				point.x = new_point[0]
				point.y = new_point[1]
		else:
			print("Objeto não suportado para escalonamento.")
	
	def rotate_origin(self, object, angle, cx, cy): # rotaciona em torno da origem da window
		matrix1 = self.matrix_translate(-cx,-cy)
		matrix2 = self.matrix_rotate(angle)
		matrix3 = self.matrix_translate(cx, cy)

		if isinstance(object, Point):
			point_matrix = np.array([object.x, object.y, 1])
			new_point = np.dot(point_matrix, matrix1)
			new_point = np.dot(new_point, matrix2)
			new_point = np.dot(new_point, matrix3)
			object.x = new_point[0]
			object.y = new_point[1]
		elif isinstance(object, Line):
			point1_matrix = np.array([object.point1.x, object.point1.y, 1])
			new_point1 = np.dot(point1_matrix, matrix1)
			new_point1 = np.dot(new_point1, matrix2)
			new_point1 = np.dot(new_point1, matrix3)
			object.point1.x = new_point1[0]
			object.point1.y = new_point1[1]
			point2_matrix = np.array([object.point2.x, object.point2.y, 1])
			new_point2 = np.dot(point2_matrix, matrix1)
			new_point2 = np.dot(new_point2, matrix2)
			new_point2 = np.dot(new_point2, matrix3)
			object.point2.x = new_point2[0]
			object.point2.y = new_point2[1]
		elif isinstance(object, Wireframe):
			for point in object.points:
				point_matrix = np.array([point.x, point.y, 1])
				new_point = np.dot(point_matrix, matrix1)
				new_point = np.dot(new_point, matrix2)
				new_point = np.dot(new_point, matrix3)
				point.x = new_point[0]
				point.y = new_point[1]
		else:
			print("Objeto não suportado para rotação.")

		
	def rotate_point(self, object, angle, x, y): # rotaciona em torno de um ponto
		matrix1 = self.matrix_translate((-1) * x,(-1) * y)
		matrix2 = self.matrix_rotate(angle)
		matrix3 = self.matrix_translate(x, y)


		if isinstance(object, Point):
			point_matrix = np.array([object.x, object.y, 1])
			new_point = np.dot(point_matrix, matrix1)
			new_point = np.dot(new_point, matrix2)
			new_point = np.dot(new_point, matrix3)
			object.x = new_point[0]
			object.y = new_point[1]
		elif isinstance(object, Line):
			point1_matrix = np.array([object.point1.x, object.point1.y, 1])
			new_point1 = np.dot(point1_matrix, matrix1)
			new_point1 = np.dot(new_point1, matrix2)
			new_point1 = np.dot(new_point1, matrix3)
			object.point1.x = new_point1[0]
			object.point1.y = new_point1[1]
			point2_matrix = np.array([object.point2.x, object.point2.y, 1])
			new_point2 = np.dot(point2_matrix, matrix1)
			new_point2 = np.dot(new_point2, matrix2)
			new_point2 = np.dot(new_point2, matrix3)
			object.point2.x = new_point2[0]
			object.point2.y = new_point2[1]
		elif isinstance(object, Wireframe):
			for point in object.points:
				point_matrix = np.array([point.x, point.y, 1])
				new_point = np.dot(point_matrix, matrix1)
				new_point = np.dot(new_point, matrix2)
				new_point = np.dot(new_point, matrix3)
				point.x = new_point[0]
				point.y = new_point[1]
		else:
			print("Objeto não suportado para rotação.")

	def rotate_center(self, object, angle):
		cx,cy = object.geometric_center()
		matrix1 = self.matrix_translate(-cx,-cy)
		matrix2 = self.matrix_rotate(angle)
		matrix3 = self.matrix_translate(cx, cy)

		if isinstance(object, Point):
			point_matrix = np.array([object.x, object.y, 1])
			new_point = np.dot(point_matrix, matrix1)
			new_point = np.dot(new_point, matrix2)
			new_point = np.dot(new_point, matrix3)
			object.x = new_point[0]
			object.y = new_point[1]
		elif isinstance(object, Line):
			point1_matrix = np.array([object.point1.x, object.point1.y, 1])
			new_point1 = np.dot(point1_matrix, matrix1)
			new_point1 = np.dot(new_point1, matrix2)
			new_point1 = np.dot(new_point1, matrix3)
			object.point1.x = new_point1[0]
			object.point1.y = new_point1[1]
			point2_matrix = np.array([object.point2.x, object.point2.y, 1])
			new_point2 = np.dot(point2_matrix, matrix1)
			new_point2 = np.dot(new_point2, matrix2)
			new_point2 = np.dot(new_point2, matrix3)
			object.point2.x = new_point2[0]
			object.point2.y = new_point2[1]
		elif isinstance(object, Wireframe):
			for point in object.points:
				point_matrix = np.array([point.x, point.y, 1])
				new_point = np.dot(point_matrix, matrix1)
				new_point = np.dot(new_point, matrix2)
				new_point = np.dot(new_point, matrix3)
				point.x = new_point[0]
				point.y = new_point[1]
		else:
			print("Objeto não suportado para rotação.")
