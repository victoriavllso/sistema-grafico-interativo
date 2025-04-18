from src.view.create_object_view.gui_create_object import Ui_Dialog, QtWidgets
from PyQt6.QtWidgets import QColorDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class CreateObjectWindow(QtWidgets.QDialog, Ui_Dialog):
	def __init__(self, controller):
		super().__init__()
		self.setupUi(self)
		self.initUI()
		self.controller = controller
		self.color = None
		self.color = QColor("black")


	def initUI(self):
		self.confirm_create_object.clicked.connect(lambda: self.controller.create_object(name=self.get_name_object(), color=self.color, points_input=self.get_points_input(), filled=self.get_filled()))
		self.color_button.clicked.connect(lambda: self.open_color_dialog())

	def get_name_object(self):
		name = self.name_lbl.text().strip()
		return name
	
	def get_filled(self):
		"""Retorna se o objeto é preenchido ou não"""
		if self.radioButton.isChecked():
			return True
		return False
	
	def open_color_dialog(self):
		"""Abre o dialogo de cores"""
		self.color = QColorDialog.getColor()
	def get_points_input(self):
		points = self.points_ln.toPlainText().strip()
		print(f'pontos captados: {points}')
		points = list(eval(points))
		return points