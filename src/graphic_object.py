from abc import ABC, abstractmethod

class GraphicObject(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def draw(self):
		pass

# ---------- DONE ---------- #
