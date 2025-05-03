import numpy as np
from math import sqrt, sin, cos, atan2, sqrt
from src.model.transform import Transform

class Projection:

	@staticmethod
	def orthogonal_projection(point, vrp, vpn, window):

		# translada VRP para a origem
		translated_points = Projection.translate_to_origin(point, vrp)

		# determina angulos de rotação para alinhar vpn com z
		theta_x, thetha_y = Projection.calculate_rotation_angles(vpn)

		# rotaciona o mundo para alinha vpn com z

		rotated_points  = Projection.rotate_to_align_z(translated_points, theta_x, thetha_y)

		# ignora a coordenada z
		projected_points = []
		for point in rotated_points:
			projected_points.append((point[0], point[1]))

		return projected_points
	
	@staticmethod
	def translate_to_origin(points, vrp):
		
		# translada VRP para a origem
		tx, ty, tz = -vrp[0], -vrp[1], -vrp[2]


		translation_matrix = Transform.matrix_translate(tx, ty, tz)
		
		translated_points = []
		for point in points:
			point_matrix = np.array([point[0], point[1], point[2], 1])
			new_point = translation_matrix @ point_matrix
			translated_points.append((new_point[0], new_point[1], new_point[2]))
		return translated_points

	@staticmethod
	def calculate_rotation_angles(vpn):

		vx, vy, vz = vpn

		theta_x = atan2(vy, sqrt(vx**2 + vz**2))
		theta_y = atan2(vx, vz)
		return theta_x, theta_y

	@staticmethod
	def rotate_to_align_z(points, theta_x, theta_y):
		
		# ROTAÇÃO EM Y
		rotation_matrix_y = Transform.matrix_rotate_y(theta_y)

		# ROTAÇÃO EM X
		rotation_matrix_x = Transform.matrix_rotate_x(theta_x)

		# aplica rotações

		rotated_points = []
		for point in points:
			point_matrix = np.array([point[0], point[1], point[2], 1])
			new_point = rotation_matrix_y @ point_matrix
			new_point = rotation_matrix_x @ new_point
			rotated_points.append(new_point)
		return rotated_points