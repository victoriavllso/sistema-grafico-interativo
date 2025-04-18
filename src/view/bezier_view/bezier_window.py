from src.view.bezier_view.gui_bezier import Ui_Dialog, QtWidgets
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import Qt

class BezierWindow(QtWidgets.QDialog, Ui_Dialog):
	def __init__(self, controller):
		super().__init__()
		self.setupUi(self)
		self.initUI()
		self.controller = controller



	def initUI(self):

		# chama a função que cria a curva bezier (função do model, acionada pelo controller)
		self.create_bezier_button.clicked.connect(lambda: self.controller(self.create_bezier_curve()))

	def get_points_input(self):

		#pega os pontos de entrada
		points = self.input_bezier.toPlainText().strip()
		points - list(eval(points))
		return points
	
	def get_name(self):

		name = self.name_curve_bezier.text().strip()
		return name