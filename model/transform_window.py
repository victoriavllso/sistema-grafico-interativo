from view.gui_transform import Ui_Dialog, QtWidgets

class TransformWindow(QtWidgets.QDialog, Ui_Dialog):
	def __init__(self,controller):
		super().__init__()
		self.setupUi(self)
		self.initUI()
		self.controller = controller

	def initUI(self):

		self.ok_cancel_transform.accepted.connect(self.confirm_transform_and_transform) # conecta o botão de ok com o método de confirmação
		self.ok_cancel_transform.rejected.connect(self.reject) # fecha a janela de transformação
	def confirm_transform(self):
		print(f'método chamado ao clicar em ok')
		if self.tabWidget.currentIndex() == 0: # pega os dados de translação e evnvia para o controller
			dx = self.get_x_translate()
			dy = self.get_y_translate()
			print(f'translação chamada com dx: {dx} e dy: {dy}')
			return dx, dy, "translate"
		
		if self.tabWidget.currentIndex() == 1: # pega os dados de rotação e envia para o controller
			angle = self.get_angle()
			angle = angle * (3.14 / 180) # converte para radianos

			#if self.rotate_origin_button.isChecked():
			#	x= 0
			#	y= 0
			#	return x, y, angle, "rotate_origin"

			#elif self.rotate_center_button.isChecked():
			#	return angle, "rotate_center"
			
			#elif self.rotate_point_button.isChecked():
			#	x = self.x_rotate.text().strip()
			#	y = self.y_rotate.text().strip()
			#	return x, y, angle, "rotate_point"
			
		elif self.tabWidget.currentIndex() == 2: # pega os dados de escalonamento e envia para o controller
			sx = self.get_x_scale() 
			sy = self.get_y_scale()
			print(f'escalonamento chamado com sx: {sx} e sy: {sy}')
			return sx, sy, "scale"
	def confirm_transform_and_transform(self):
		tx,ty,type = self.confirm_transform()
		self.controller.transform_object(tx,ty,type)
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
		angle = self.angulo_input.text().strip()
		return angle
