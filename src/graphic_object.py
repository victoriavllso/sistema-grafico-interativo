from abc import ABC, abstractmethod
from utils import BLACK_RGB

class GraphicObject(ABC):
	def __init__(self, name: str, color: tuple[int, int, int] = BLACK_RGB):
		self.name = name
		self.color = color

	@abstractmethod
	def draw(self):
		pass

# ---------- DONE ---------- #
