from src.view.bezier_view.gui_bezier import Ui_Dialog, QtWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QColorDialog

class BezierWindow(QtWidgets.QDialog, Ui_Dialog):
	def __init__(self, controller):
		super().__init__()
		self.setupUi(self)
		self.initUI()
		self.controller = controller
		self.color = QColor("black")


	def initUI(self):

		self.create_bezier_button.accepted.connect(lambda: self.handle_create_bezier())
		self.create_bezier_button.rejected.connect(self.reject)
		self.set_color_bezier.clicked.connect(lambda: self.open_color_dialog())
	
	def get_points_input(self):

		#pega os pontos de entrada
		points = self.input_bezier.toPlainText().strip()
		points = list(eval(points))
		return points
	
	def get_name(self):

		name = self.name_curve_bezier.text().strip()
		return name
	
	def handle_create_bezier(self):
		""" lidamos com a criação de objecto para que a janela não fique com os dados do objeto criado anteriormente"""
		self.controller.create_bezier_curve(name=self.get_name(), points_input=self.get_points_input(), color=self.color)
		self.reset_fields()

	def reset_fields(self):
		self.name_curve_bezier.clear()
		self.input_bezier.clear()
		self.color = QColor("black")

	def open_color_dialog(self):
		"""Abre o dialogo de cores"""
		self.color = QColorDialog.getColor()