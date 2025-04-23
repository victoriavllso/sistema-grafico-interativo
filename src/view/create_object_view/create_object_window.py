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
		self.color = QColor("black")

	def initUI(self):
		self.confirm_create_object.accepted.connect(lambda: self.handle_create_object())
		self.confirm_create_object.rejected.connect(self.reject)
		self.color_button.clicked.connect(lambda: self.open_color_dialog())
		self.set_object_types()

	def get_name_object(self) -> str:
		"""Retorna o nome do objeto"""
		name = self.name_ln.text().strip()
		return name
	
	def get_filled(self) -> bool:
		"""Retorna se o objeto é preenchido ou não"""
		if self.radioButton.isChecked():
			return True
		return False
	
	def open_color_dialog(self) -> None:
		"""Abre o dialogo de cores"""
		self.color = QColorDialog.getColor()
	def get_points_input(self):
		points = self.points_ln.toPlainText().strip()
		points = list(eval(points))
		return points
	
	def reset_fields(self) -> None:
		"""Reseta os campos de entrada"""
		self.name_lbl.clear()
		self.points_ln.clear()
		self.color = QColor("black")
		self.radioButton.setChecked(False)

	def handle_create_object(self) -> None:
		""" lida com a criação do objeto"""
		self.controller.create_object(name=self.get_name_object(), color=self.color, points_input=self.get_points_input(), filled=self.get_filled(), type=self.get_selected_object_type())	
		self.reset_fields()

	def set_object_types(self, types: list[str]=["point", "line", "wireframe", "bezier", "spline"]) -> None:
		"""Define os tipos de objeto disponíveis na combo box"""
		self.obj_type_comboBox.clear()
		self.obj_type_comboBox.addItems(types)

	def get_selected_object_type(self) -> str:
		"""Retorna o tipo de objeto selecionado na combo box"""
		return self.obj_type_comboBox.currentText()
