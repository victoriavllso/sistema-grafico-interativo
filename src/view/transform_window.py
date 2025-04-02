from src.view.gui_transform import Ui_Dialog, QtWidgets
from PyQt6.QtWidgets import QListWidget

class TransformData:

class TransformWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.controller = controller
        
        self.display_transform = QListWidget(self)
        self.display_transform.setGeometry(370, 90, 190, 220) # Coordenadas retiradas do gui_transform.ui, na área reservada ao display
        
        self.transform_added = False
        self.transform_list = []

    def initUI(self):
        self.ok_cancel_transform.accepted.connect(self.confirm_transform_and_transform)
        self.ok_cancel_transform.rejected.connect(self.reject)
        self.add_transform_button.clicked.connect(self.add_transform_display)
    
    def add_transform_display(self):
        try:
            transform_data = None
            
            # Translação
            if self.tabWidget.currentIndex() == 0:
                transform_data = {
                    "type": "translate",
                    "tx": self.get_x_translate(),
                    "ty": self.get_y_translate(),
                    "angle": None,
                    "text": f"Translação nos pontos {float(self.get_x_translate())} {float(self.get_y_translate())}"
                }

            # Rotação
            elif self.tabWidget.currentIndex() == 1:
                angle = self.get_angle() * (3.14 / 180)

                if self.rotate_origin_button.isChecked():
                    transform_data = {
                        "type": "rotate_origin",
                        "tx": 0, "ty": 0,
                        "angle": angle,
                        "text": f"Rotação em torno da origem com {float(self.get_angle())} graus"
                    }
                elif self.rotate_center_button.isChecked():
                    transform_data = {
                        "type": "rotate_center",
                        "tx": 0, "ty": 0,
                        "angle": angle,
                        "text": f"Rotação em torno do centro do objeto {float(self.get_angle())} graus"
                    }
                elif self.rotate_point_button.isChecked():
                    transform_data = {
                        "type": "rotate_point",
                        "tx": self.get_x_rotate(),
                        "ty": self.get_y_rotate(),
                        "angle": angle,
                        "text": f"Rotação em torno do ponto: ({float(self.get_x_rotate())}, {float(self.get_y_rotate())}) com {float(self.get_angle())} graus"
                    }
                
            elif self.tabWidget.currentIndex() == 2:  # Escalonamento
                transform_data = {
                    "type": "scale",
                    "tx": self.get_x_scale(),
                    "ty": self.get_y_scale(),
                    "angle": None,
                    "text": f"Escalonamento no ponto: ({float(self.get_x_scale())}, {float(self.get_y_scale())})"
                }
            
            if transform_data:
                self.transform_list.append(transform_data)
                self.transform_added = True
                self.update_display_transform()
            else:
                self.transform_added = False
        
        except ValueError:
            self.controller.show_popup(
                "Erro", "Erro ao adicionar transformação. Verifique os valores informados.",
                QtWidgets.QMessageBox.Icon.Critical
            )
    
    def confirm_transform_and_transform(self):
        try:
            if self.transform_added:
                self.controller.transform_object(self.transform_list)
                self.clear_transform_list()
            else:
                self.controller.show_popup(
                    "Erro", "É necessário adicionar as transformações antes de prosseguir!",
                    QtWidgets.QMessageBox.Icon.Critical
                )
        except Exception as e:
            self.controller.show_popup(
                "Erro", f"Erro ao aplicar a transformação: {str(e)}",
                QtWidgets.QMessageBox.Icon.Critical
            )
    
    def clear_transform_list(self):
        self.transform_list = []
        self.display_transform.clear()
        self.transform_added = False

    def update_display_transform(self):
        self.display_transform.clear()
        for transform in self.transform_list:
            self.display_transform.addItem(transform["text"])
        self.display_transform.show()
    
    def get_x_translate(self):
        return float(self.x_translate.text().strip())

    def get_y_translate(self):
        return float(self.y_translate.text().strip())
    
    def get_x_scale(self):
        return float(self.x_scaling.text().strip())
    
    def get_y_scale(self):
        return float(self.y_scaling.text().strip())

    def get_angle(self):
        return float(self.angulo_input.text().strip())
    
    def get_x_rotate(self):
        return float(self.x_rotate.text().strip())
    
    def get_y_rotate(self):
        return float(self.y_rotate.text().strip())
