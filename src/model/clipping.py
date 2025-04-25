from src.model.graphic_objects.line import Line
from src.model.graphic_objects.point import Point
from src.model.graphic_objects.wireframe import Wireframe
from src.model.graphic_objects.bezier import Bezier
from src.model.graphic_objects.bspline import BSpline
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

		# define a viewport
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
				self.clip_wireframe(obj)
			if isinstance(obj, Bezier) or isinstance(obj, BSpline):
				for point in obj.points:
					point.convert_coordinates()
					self.clip_bezier(obj)

	def clip_point(self, point):
		x, y = point.scn_x, point.scn_y
		if ((x <= self.x_max) and (x >= self.x_min)) and ((y<= self.y_max) and (y >= self.y_min)):
			point.inside_window = True
		else:
			point.inside_window = False
			 
	def clip_line(self, line, clipping_algorithm):
			x1, y1 = line.points[0].scn_x, line.points[0].scn_y
			x2, y2 = line.points[1].scn_x, line.points[1].scn_y
			result = None
			
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

		def inside(p, edge, clip_edge_type):
			x, y = p
			if clip_edge_type == 'LEFT':
				return x >= edge
			elif clip_edge_type == 'RIGHT':
				return x <= edge
			elif clip_edge_type == 'BOTTOM':
				return y >= edge
			elif clip_edge_type == 'TOP':
				return y <= edge
			
		def compute_intersection(p1, p2, edge, clip_edge_type):
			x1, y1 = p1
			x2, y2 = p2

			if x1 == x2:
				m = None  # Vertical line
			else:
				m = (y2 - y1) / (x2 - x1)

			if clip_edge_type == 'LEFT' or clip_edge_type == 'RIGHT':
				x_edge = edge
				if m is not None:
					y = m * (x_edge - x1) + y1
				else:
					y = y1
				return (x_edge, y)
			else:  # BOTTOM or TOP
				y_edge = edge
				if m is not None:
					x = (y_edge - y1) / m + x1
				else:
					x = x1
				return (x, y_edge)
		
		polygon = [(point.scn_x, point.scn_y) for point in wireframe.points]
		clip_window = (self.x_min, self.y_min, self.x_max, self.y_max)

		edges = [
        ('LEFT', clip_window[0]),
        ('RIGHT', clip_window[2]),
        ('BOTTOM', clip_window[1]),
        ('TOP', clip_window[3])
    ]

		output_polygon = polygon
		for edge_type, edge_val in edges:
			input_polygon = output_polygon
			output_polygon = []
			if not input_polygon:
				break
			prev_point = input_polygon[-1]

			for curr_point in input_polygon:
				if inside(curr_point, edge_val, edge_type):
					if inside(prev_point, edge_val, edge_type):
						output_polygon.append(curr_point)
					else:
						inter_pt = compute_intersection(prev_point, curr_point, edge_val, edge_type)
						output_polygon.append(inter_pt)
						output_polygon.append(curr_point)
				elif inside(prev_point, edge_val, edge_type):
					inter_pt = compute_intersection(prev_point, curr_point, edge_val, edge_type)
					output_polygon.append(inter_pt)
				prev_point = curr_point

		for point in wireframe.points:
			point.inside_window = True
		wireframe.points_draw = []

		for point in output_polygon:
			x, y = point
			p = Point(self.window, x, y)
			p.from_scene_coordinates(x, y)
			p.inside_window = True
			wireframe.points_draw.append(p)
		return output_polygon

	def clip_bezier(self, bezier) -> None:
		"""Clip a Bezier curve"""
		bezier.points_draw = []
		for point in bezier.curve_points:
			point.convert_coordinates()
			self.clip_point(point)
			if point.inside_window:
				bezier.points_draw.append(point)
