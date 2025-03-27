from gui.gui_transform import Ui_Dialog, QtWidgets

class TransformWindow(QtWidgets.QDialog, Ui_Dialog):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.initUI()

	def initUI(self):
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
	#	self.rotate_origin_button.clicked.connect(self.show_translate)
	#	self.rotete_point_button.clicked.connect(self.show_rotate)
	#	self.rotate_center_button.clicked.connect(self.show_scale)
		self.angulo_input.text()
		
	#def show_translate(self):
	#	pass
	
	#def show_rotate(self):
	#	pass
	#def show_scale(self):
	#	pass
if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	window = TransformWindow()
	window.show()
	sys.exit(app.exec())