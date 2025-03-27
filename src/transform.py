import numpy as np
from src.point import Point
from src.line import Line
from src.wireframe import Wireframe

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
	def translate_object(self, vector_coordenate, dx ,dy):
		matrix_result = self.multiply_matrix(self.matrix_translate(dx, dy),vector_coordenate)
		print(f'matriz de translação: {matrix_result}')
		return matrix_result

	def scale_object(self, vector_coordenate, sx, sy):
		pass
	
	def rotate_objet_center_word(self, vector_coordenate, angle):
		pass