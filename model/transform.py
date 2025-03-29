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
	
	def multiply_matrix(self, matrix1, matrix2):
		return np.dot(matrix1, matrix2)
	
	# methods to transform objects
	def translate_object(self, object,dx ,dy):
		result = self.matrix_translate(dx, dy)

		if isinstance(object, Point):
			object.x += dx
			object.y += dy
		elif isinstance(object, Line):
			object.point1.x += dx
			object.point1.y += dy
			object.point2.x += dx
			object.point2.y += dy
		elif isinstance(object, Wireframe):
			for point in object.points:
				point.x += dx
				point.y += dy



	def scale_object(self,object,sx, sy):
		cx, cy = object.geometric_center()
		matrix1 = self.matrix_translate(-cx,-cy)
		matrix2 = self.matrix_scale(sx,sy)
		matrix3 = self.matrix_translate(cx, cy)
		result1 = self.multiply_matrix(matrix1, matrix2)
		result2 = self.multiply_matrix(result1, matrix3)
		
		# aplica a matriz de transformação
		if isinstance(object, Point):
			point_matrix = np.array([[object.x], [object.y], [1]])
			new_point = self.multiply_matrix(result2, point_matrix)
			object.x = new_point[0][0]
			object.y = new_point[1][0]
		elif isinstance(object, Line):
			point1_matrix = np.array([[object.point1.x], [object.point1.y], [1]]) # para uma reta, aplica a trnasformação nos 2 ponntos dela
			new_point1 = self.multiply_matrix(result2, point1_matrix)
			object.point1.x = new_point1[0][0]
			object.point1.y = new_point1[1][0]

			point2_matrix = np.array([[object.point2.x], [object.point2.y], [1]])
			new_point2 = self.multiply_matrix(result2, point2_matrix)
			object.point2.x = new_point2[0][0]
			object.point2.y = new_point2[1][0]
		elif isinstance(object, Wireframe):
			for point in object.points:
				point_matrix = np.array([[point.x], [point.y], [1]])
				new_point = self.multiply_matrix(result2, point_matrix)
				point.x = new_point[0][0]
				point.y = new_point[1][0]
	
	def rotate_origin(self, object, angle, cx, cy): # rotaciona em torno da origem da window
		matrix1 = self.matrix_translate(-cx,-cy)
		matrix2 = self.matrix_rotate(angle)
		matrix3 = self.matrix_translate(cx, cy)
		result1 = self.multiply_matrix(matrix1, matrix2)
		result2 = self.multiply_matrix(result1, matrix3)
		
		if isinstance(object, Point):
			point_matrix = np.array([[object.x], [object.y], [1]])
			new_point = self.multiply_matrix(result2, point_matrix)
			object.x = new_point[0][0]
			object.y = new_point[1][0]
		elif isinstance(object, Line):
			point1_matrix = np.array([[object.point1.x], [object.point1.y], [1]])
			new_point1 = self.multiply_matrix(result2, point1_matrix)
			object.point1.x = new_point1[0][0]
			object.point1.y = new_point1[1][0]

			point2_matrix = np.array([[object.point2.x], [object.point2.y], [1]])
			new_point2 = self.multiply_matrix(result2, point2_matrix)
			object.point2.x = new_point2[0][0]
			object.point2.y = new_point2[1][0]
		elif isinstance(object, Wireframe):
			for point in object.points:
				point_matrix = np.array([[point.x], [point.y], [1]])
				new_point = self.multiply_matrix(result2, point_matrix)
				point.x = new_point[0][0]
				point.y = new_point[1][0]

		
	def rotate_point(self, object, angle, x, y): # rotaciona em torno de um ponto
		matrix1 = self.matrix_translate(-x,-y)
		matrix2 = self.matrix_rotate(angle)
		matrix3 = self.matrix_translate(x, y)
		result1 = self.multiply_matrix(matrix1, matrix2)
		result2 = self.multiply_matrix(result1, matrix3)
		if isinstance(object, Point):
			point_matrix = np.array([[object.x], [object.y], [1]])
			new_point = self.multiply_matrix(result2, point_matrix)
			object.x = new_point[0][0]
			object.y = new_point[1][0]
		elif isinstance(object, Line):
			point1_matrix = np.array([[object.point1.x], [object.point1.y], [1]])
			new_point1 = self.multiply_matrix(result2, point1_matrix)
			object.point1.x = new_point1[0][0]
			object.point1.y = new_point1[1][0]

			point2_matrix = np.array([[object.point2.x], [object.point2.y], [1]])
			new_point2 = self.multiply_matrix(result2, point2_matrix)
			object.point2.x = new_point2[0][0]
			object.point2.y = new_point2[1][0]
		elif isinstance(object, Wireframe):
			for point in object.points:
				point_matrix = np.array([[point.x], [point.y], [1]])
				new_point = self.multiply_matrix(result2, point_matrix)
				point.x = new_point[0][0]
				point.y = new_point[1][0]

	def rotate_center(self, object, angle):
		cx,cy = object.geometric_center()
		matrix1 = self.matrix_translate(-cx,-cy)
		matrix2 = self.matrix_rotate(angle)
		matrix3 = self.matrix_translate(cx, cy)
		result1 = self.multiply_matrix(matrix1, matrix2)
		result2 = self.multiply_matrix(result1, matrix3)

		if isinstance(object, Point):
			point_matrix = np.array([[object.x], [object.y], [1]])
			new_point = self.multiply_matrix(result2, point_matrix)
			object.x = new_point[0][0]
			object.y = new_point[1][0]
		elif isinstance(object, Line):
			point1_matrix = np.array([[object.point1.x], [object.point1.y], [1]])
			new_point1 = self.multiply_matrix(result2, point1_matrix)
			object.point1.x = new_point1[0][0]
			object.point1.y = new_point1[1][0]

			point2_matrix = np.array([[object.point2.x], [object.point2.y], [1]])
			new_point2 = self.multiply_matrix(result2, point2_matrix)
			object.point2.x = new_point2[0][0]
			object.point2.y = new_point2[1][0]
		elif isinstance(object, Wireframe):
			for point in object.points:
				point_matrix = np.array([[point.x], [point.y], [1]])
				new_point = self.multiply_matrix(result2, point_matrix)
				point.x = new_point[0][0]
				point.y = new_point[1][0]

