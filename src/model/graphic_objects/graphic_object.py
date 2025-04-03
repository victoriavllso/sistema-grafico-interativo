from abc import ABC, abstractmethod
from PyQt6.QtCore import Qt
class GraphicObject(ABC):
	def __init__(self, name: str, color: Qt.GlobalColor = Qt.GlobalColor.black):
		self.name = name
		self.color = color

	@abstractmethod
	def draw(self):
		pass

	@abstractmethod
	def geometric_center(self):
		pass

	@abstractmethod
	def receive_transform(self, matrix) -> None:
		pass

	@abstractmethod
	def __str__(self):
		pass
