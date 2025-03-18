from graphic_object import GraphicObject
from utils import BLACK_RGB

class Point(GraphicObject):
	def __init__(self, x, y, color= BLACK_RGB):
		self.x = x
		self.y = y
		self.color = color
	
	#TODO: Draw with API
	def draw(self):
		print(f"Drawing a point at ({self.x}, {self.y})")
