from abc import ABC, abstractmethod
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class GraphicObject(ABC):
	def __init__(self, name: str, color: Qt.GlobalColor = Qt.GlobalColor.black, window=None):
		self.name = name
		self.color = color
		self.window = window

	@abstractmethod
	def draw(self) -> None:
		"""Desenha o objeto gráfico na tela"""
		pass

	@abstractmethod
	def geometric_center(self) -> tuple[float, float]:
		"""Retorna o centro geométrico do objeto gráfico"""
		pass

	@abstractmethod
	def receive_transform(self, matrix) -> None:
		"""Aplica a transformação da matriz de transformação ao objeto gráfico"""
		pass

	@abstractmethod
	def __str__(self):
		pass

	@abstractmethod
	def get_points_obj(self):
		"""Retorna os pontos do objeto gráfico em formato .obj"""
		return
	
	@abstractmethod
	def get_type_obj(self):
		"""Retorna o tipo do objeto gráfico"""
		return

	def get_name_obj(self):
		"""Retorna o nome para .obj"""
		return f'o {self.name}'
	
	def get_color_obj(self):
		"""Retorna a cor para .obj"""
		qcolor = QColor(self.color)
		return (qcolor.red(), qcolor.green(), qcolor.blue())
