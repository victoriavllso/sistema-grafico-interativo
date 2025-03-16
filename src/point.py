from graphic_object import GraphicObject

class Point(GraphicObject):
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def draw(self):
		print(f"Drawing a point at ({self.x}, {self.y})") #precisamos implementar a viewport e winndow