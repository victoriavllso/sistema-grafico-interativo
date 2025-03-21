from abc import ABC, abstractmethod

class GraphicObject(ABC):
	def __init__(self, name: str):
		self.name = name

	@abstractmethod
	def draw(self):
		pass

# ---------- DONE ---------- #
