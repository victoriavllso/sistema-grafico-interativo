from src.view.gui_transform import Ui_Dialog, QtWidgets

class TransformWindow(QtWidgets.QDialog, Ui_Dialog):
	def __init__(self,controller):
		super().__init__()
		self.setupUi(self)
		self.initUI()
		self.controller = controller

		# configuração do display
		font = self.label_transform_2d.font()
		font.setPointSize(9)
		self.label_transform_2d.setFont(font)
		self.label_transform_2d.setStyleSheet("color: black; background-color: white;")

	def initUI(self):
		self.ok_cancel_transform.accepted.connect(self.confirm_transform_and_transform)
		self.ok_cancel_transform.rejected.connect(self.reject)
		self.add_transform_button.clicked.connect(self.add_transform_display) 
	
	def confirm_transform(self):
		if self.tabWidget.currentIndex() == 0:
			dx = self.get_x_translate()
			dy = self.get_y_translate()
			return dx, dy, None,"translate"
		
		if self.tabWidget.currentIndex() == 1:
			angle = self.get_angle()
			angle = angle * (3.14 / 180)

			if self.rotate_origin_button.isChecked():
				x, y = 0 , 0
				if self.x_rotate.text() != "" or self.y_rotate.text() != "":
					self.controller.show_popup("Erro", "Para rotacionar em torno da origem, não é necessário informar as coordenadas x e y", QtWidgets.QMessageBox.Icon.Critical)	
				return x, y, angle, "rotate_origin"

			elif self.rotate_center_button.isChecked():
				if self.x_rotate.text() != "" or self.y_rotate.text() != "":
					self.controller.show_popup("Erro", "Para rotacionar em torno do seu centro, não é necessário informar as coordenadas x e y", QtWidgets.QMessageBox.Icon.Critical)
				return 0,0, angle, "rotate_center"
			
			elif self.rotate_point_button.isChecked():
				x = self.x_rotate.text().strip()
				y = self.y_rotate.text().strip()
				return x, y, angle, "rotate_point"
			
		elif self.tabWidget.currentIndex() == 2:
			sx = self.get_x_scale() 
			sy = self.get_y_scale()
			return sx, sy, None, "scale"
	
	def add_transform_display(self):
		text = None
		if self.tabWidget.currentIndex() == 0:
			text = "Translação"
		elif self.tabWidget.currentIndex() == 1:
			if self.rotate_origin_button.isChecked():
				text = "Rotação em torno da origem"
			elif self.rotate_center_button.isChecked():
				text = "Rotação em torno do centro do objeto"
			
			elif self.rotate_point_button.isChecked():
				text = "Rotação em torno de um ponto qualquer"
		elif self.tabWidget.currentIndex() == 2:
			text = "Escalonamento"
			
		if text is not None:
			self.label_transform_2d.setText(text)
			self.label_transform_2d.repaint()
			return True
		else:
			return False
	
	def confirm_transform_and_transform(self):
		if self.add_transform_display:
			tx,ty,angle, type = self.confirm_transform()
			self.controller.transform_object(tx,ty,angle,type)
		else:
			self.controller.show_popup("Erro", "É necessário adicioanar as transformações antes de prosseguir !", QtWidgets.QMessageBox.Icon.Critical)

	def get_x_translate(self):
		x = float(self.x_translate.text().strip())
		return x

	def get_y_translate(self):
		y = float(self.y_translate.text().strip())
		return y
	
	def get_x_scale(self):
		x = float(self.x_scaling.text().strip())
		return x
	
	def get_y_scale(self):
		y = float(self.y_scaling.text().strip())
		return y

	def get_angle(self):
		angle = float(self.angulo_input.text().strip())
		return angle
