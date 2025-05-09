import numpy as np
from math import sqrt, sin, cos, atan2, sqrt
from src.model.transform import Transform

class Projection:

	@staticmethod
	def orthogonal_projection(point, vrp, vpn, window):
		# 1. Translação para origem (VRP para (0,0,0))
		translated_points = Projection.translate_to_origin(point, vrp)

		# 2. Rotação para alinhar VPN com o eixo Z
		theta_x, theta_y = Projection.calculate_rotation_angles(vpn)
		rotated_points = Projection.rotate_to_align_z(translated_points, theta_x, theta_y)

		# 3. Aplicar matriz de projeção ortográfica
		projection_matrix = np.array([
		[1, 0, 0, 0],
		[0, 1, 0, 0],
		[0, 0, 0, 0],  # Z é projetado para 0
		[0, 0, 0, 1]
		])

		projected_points = []
		for point in rotated_points:
			# Converter para coordenadas homogêneas se necessário
			if len(point) == 3:
				point = (*point, 1)

			# Aplicar projeção
			projected = projection_matrix @ np.array(point)

			# Normalizar (dividir por w se não for 1)
			if projected[3] != 0:
				projected = projected / projected[3]

			projected_points.append((projected[0], projected[1]))

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
