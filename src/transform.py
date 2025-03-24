import numpy as np
from src.point import Point
from src.line import Line
from src.wireframe import Wireframe

class Transform:
	def __init__(self):
		pass

	# homogeneous coordinates systems
	def matrix_rotate(self, angle):
		matrix_rotate = [[np.cos(angle), -np.sin(angle), 0],
						 [np.sin(angle), np.cos(angle), 0],
						 [0, 0, 1]]
		return matrix_rotate
	
	
	def rotate_around_point(self, angle,object):
		if isinstance(object, Point):
			return "Não é possível rotacionar um ponto em torno de outro ponto"
		
		if isinstance(object, Line):
			
