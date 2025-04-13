from src.model.graphic_objects.line import Line
from src.model.graphic_objects.point import Point
from src.model.graphic_objects.wireframe import Wireframe
from src.utils.utils import MARGIN_FACTOR

class Cliper:
	def __init__(self, window, viewport):
		self.inside = 0 # 0000
		self.left = 1 # 0001
		self.right = 2 # 0010
		self.bottom = 4 # 0100
		self.top = 8 	# 1000
		self.window = window
		self.viewport = viewport

		self.x_min = -1 + 2* MARGIN_FACTOR
		self.x_max = 1 - 2* MARGIN_FACTOR
		self.y_min = -1 + 2* MARGIN_FACTOR
		self.y_max = 1 - 2* MARGIN_FACTOR

	def clip_object(self, graphic_objects, clipping_algorithm):
		

		for obj in graphic_objects:

			if isinstance(obj, Point): 
					obj.convert_coordinates()
					self.clip_point(obj)

			if isinstance(obj, Line):
				for point in obj.points:
					point.convert_coordinates()
				self.clip_line(obj, clipping_algorithm)

			if isinstance(obj, Wireframe):
				for point in obj.points:
					point.convert_coordinates()
				print('clip wireframe chamado')
				self.clip_wireframe(obj)
			


	def clip_point(self, point):
		x, y = point.scn_x, point.scn_y

		if ((x <= self.x_max) and (x >= self.x_min)) and ((y<= self.y_max) and (y >= self.y_min)):
		
			point.inside_window = True
		else:
			point.inside_window = False
		
			 
	def clip_line(self, line, clipping_algorithm):
			
			# pega as coordenadas normalizadas
			x1, y1 = line.points[0].scn_x, line.points[0].scn_y
			x2, y2 = line.points[1].scn_x, line.points[1].scn_y

			result = None

			############## verifica a clipagem selecionada
			
			if clipping_algorithm == "cohen-sutherland":
				# chama o algoritmo de cohen-sutherland
				result = self.cohen_sutherland(x1, y1, x2, y2, self.x_min, self.x_max, self.y_min, self.y_max)

				if result is not None:
					# atualiza as coordenadas da reta
					line.points[0].scn_x, line.points[0].scn_y = result[0][0], result[0][1]
					line.points[1].scn_x, line.points[1].scn_y = result[1][0], result[1][1]
					line.points[0].inside_window = True
					line.points[1].inside_window = True

				else:
					line.points[0].inside_window = False
					line.points[1].inside_window = False

			elif clipping_algorithm == "liang-barsky":
				# chama o algoritmo de liang-barsky
				result = self.liang_barsky(x1, x2, y1, y2, self.x_min, self.x_max, self.y_min, self.y_max)

				if result is not None:
					# atualiza as coordenadas da reta
					line.points[0].scn_x, line.points[0].scn_y = result[0][0], result[0][1]
					line.points[1].scn_x, line.points[1].scn_y = result[1][0], result[1][1]
					line.points[0].inside_window = True
					line.points[1].inside_window = True
				else:
					line.points[0].inside_window = False
					line.points[1].inside_window = False

	def cohen_sutherland(self, x1, y1, x2, y2, x_min, x_max, y_min, y_max):
		inside = False # linha fora da viewport
		
		#  associa código de região a cada ponto da linha
		code1, code2 = self.get_code(x1, y1, x_min, x_max, y_min, y_max), self.get_code(x2, y2, x_min, x_max, y_min, y_max)


		# verifica se a linha é totalmente isível, invisível ou parcialmente visível
		while True:
			# completamente visível
			if code1 == 0 and code2 == 0:
				inside = True
				break
				
			# completamente invisível
			elif code1 & code2 != 0:
				break
			# parcialmente visível
			else:
				code_outside = code1 if code1 != 0 else code2
				x_intersection, y_intersection = 0,0

				if x2 != x1:
					# calculamos o coeficiente angular
					m = (y2 - y1) / (x2 - x1)
				else:
					# linha vertical
					m = float('inf')
				
				# calclamos as intersecções

				if code_outside & self.top:
					x_intersection = x1 + 1/m * (y_max - y1)
					y_intersection = y_max
				elif code_outside & self.bottom:
					x_intersection = x1 + 1/m * (y_min - y1)
					y_intersection = y_min
				elif code_outside & self.right:
					x_intersection = x_max
					y_intersection = y1 + m * (x_max - x1)
				elif code_outside & self.left:
					x_intersection = x_min
					y_intersection = y1 + m * (x_min - x1)

				if code_outside == code1:
					x1, y1 = x_intersection, y_intersection
					code1 = self.get_code(x1, y1, x_min, x_max, y_min, y_max)
				else:
					x2, y2 = x_intersection, y_intersection
					code2 = self.get_code(x2, y2, x_min, x_max, y_min, y_max)
		if inside:
			return (x1, y1), (x2, y2)	

		else:
			return 
				

	def get_code(self, x, y, x_min, x_max, y_min, y_max):
		code = 0
		if x < x_min:
			code |= self.left
		elif x > x_max:
			code |= self.right
		if y < y_min:
			code |= self.bottom
		elif y > y_max:
			code |= self.top
		return code
		
	def liang_barsky(self, x1,x2,y1,y2, x_min, x_max, y_min, y_max):

		dx = x2 - x1
		dy = y2 - y1
		directions = [-dx, dx, -dy, dy]
		distances = [x1 - x_min, x_max - x1, y1 - y_min, y_max - y1]
		limit_inferior = 0
		limit_superior = 1


		for i in range(4):
			if directions[i] == 0:
				if distances[i] < 0:
					break
			else:
				t = distances[i] / directions[i]
				if directions[i] < 0:
					limit_inferior = max(limit_inferior, t)
				else:
					limit_superior = min(limit_superior, t)
		if limit_inferior > limit_superior:
			return
		else:
			x1_clipped = x1 + limit_inferior * dx
			y1_clipped = y1 + limit_inferior * dy
			x2_clipped = x1 + limit_superior * dx
			y2_clipped = y1 + limit_superior * dy
			return (x1_clipped, y1_clipped), (x2_clipped, y2_clipped)
	
	def clip_wireframe(self, wireframe):
		clipper_edges = [
			(self.x_min, self.y_min, self.x_max, self.y_min),  # Bottom
			(self.x_max, self.y_min, self.x_max, self.y_max),  # Right
			(self.x_max, self.y_max, self.x_min, self.y_max),  # Top
			(self.x_min, self.y_max, self.x_min, self.y_min)   # Left
		]

		# Pega as coordenadas SCN (normalizadas) dos pontos
		wireframe_points = [(p.scn_x, p.scn_y) for p in wireframe.points]

		clipped = wireframe_points  # Inicializa com os pontos do wireframe original

		# Aplica o corte cumulativo para cada aresta da janela
		for edge in clipper_edges:
			x1, y1, x2, y2 = edge
			clipped = self.sutherland_hodgman(clipped, x1, y1, x2, y2)  # Aplica o corte da aresta

			if not clipped:  # Se o recorte resultar em uma lista vazia, não há interseção
				print('Nenhum ponto recortado')
				return  # Retorna imediatamente se nenhum ponto foi recortado

		# Atualiza diretamente os pontos em wireframe com os pontos recortados
		for i, point in enumerate(wireframe.points):
			if i < len(clipped):
				point.scn_x, point.scn_y = clipped[i][0], clipped[i][1]
				point.scx_x = clipped[i][0]  # Atribuindo a coordenada X
				point.scx_y = clipped[i][1]  # Atribuindo a coordenada Y
				point.inside_window = True
				print(f'Novas coordenadas do wireframe: x={point.scn_x}, y={point.scn_y}')
			else:
				point.inside_window = False  # Marca o ponto como fora da janela

		print(f'Coordenadas da janela: ({self.x_min}, {self.y_min}, {self.x_max}, {self.y_max})')

	def sutherland_hodgman(self, subject_polygon, x1, y1, x2, y2):
		def inside(p):
			# Determina se o ponto p está à esquerda da aresta (x1,y1) -> (x2,y2)
			return (x2 - x1)*(p[1] - y1) - (y2 - y1)*(p[0] - x1) >= 0

		def compute_intersection(p1, p2):
			# Calcula a interseção entre a aresta do polígono e a borda do clipper
			dx = p2[0] - p1[0]
			dy = p2[1] - p1[1]
			dx_clip = x2 - x1
			dy_clip = y2 - y1

			denominator = dx * dy_clip - dy * dx_clip
			if denominator == 0:
				return p1  # Linhas paralelas, sem interseção

			t = ((x1 - p1[0]) * dy_clip - (y1 - p1[1]) * dx_clip) / denominator
			return (p1[0] + t * dx, p1[1] + t * dy)

		output_list = []
		n = len(subject_polygon)

		for i in range(n):
			current = subject_polygon[i]
			prev = subject_polygon[i - 1]

			# Verifica se o ponto atual está dentro da borda
			if inside(current):
				if not inside(prev):
					output_list.append(compute_intersection(prev, current))
				output_list.append(current)
			elif inside(prev):
				output_list.append(compute_intersection(prev, current))

		return output_list