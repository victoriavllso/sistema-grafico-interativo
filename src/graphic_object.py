from abc import ABC, abstractmethod
from utils import LINE_COLOR

class GraphicObject(ABC):
	def __init__(self, name: str = "default", color: tuple[int, int, int] = LINE_COLOR):
		self.name = name
		self.color = color

	@abstractmethod
	def draw(self):
		pass

# ---------- DONE ---------- #
