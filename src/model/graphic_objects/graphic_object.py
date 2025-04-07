from abc import ABC, abstractmethod
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

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

	@abstractmethod
	def get_points_obj(self):
		return
	
	@abstractmethod
	def get_type_obj(self):
		return

	def get_name_obj(self):
		return f'o {self.name}'
	
	def get_color_obj(self):
		qcolor = QColor(self.color)
		return (qcolor.red(), qcolor.green(), qcolor.blue())