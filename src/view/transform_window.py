from src.view.gui_transform import Ui_Dialog, QtWidgets
from PyQt6.QtWidgets import QListWidget

class TransformWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.controller = controller
        
        self.display_transform = QListWidget()
        self.display_transform.setGeometry(
            self.controller.display_file.x_min, 
            self.controller.display_file.y_min, 
            self.controller.display_file.x_max, 
            self.controller.display_file.y_max
        )
        
        self.transform_added = False
        self.transform_list_display = []
        self.transform_list = []

    def initUI(self):
        self.ok_cancel_transform.accepted.connect(self.confirm_transform_and_transform)
        self.ok_cancel_transform.rejected.connect(self.reject)
        self.add_transform_button.clicked.connect(self.add_transform_display)
    
    def confirm_transform(self):
        if self.tabWidget.currentIndex() == 0:  # Translação
            transform_data = {
                "type": "translate",
                "tx": self.get_x_translate(),
                "ty": self.get_y_translate(),
                "angle": None
            }
            self.transform_list.append(transform_data)
        elif self.tabWidget.currentIndex() == 1:  # Rotação
            angle = self.get_angle() * (3.14 / 180)  # Converte para radianos

            if self.rotate_origin_button.isChecked():
                transform_data = {
                    "type": "rotate_origin",
                    "tx": 0, "ty": 0,
                    "angle": angle
                }
                self.transform_list.append(transform_data)
                if self.x_rotate.text() or self.y_rotate.text():
                    self.controller.show_popup(
                        "Erro", "Para rotacionar em torno da origem, não é necessário informar x e y",
                        QtWidgets.QMessageBox.Icon.Critical
                    )
                    return

            elif self.rotate_center_button.isChecked():
                transform_data = {
                    "type": "rotate_center",
                    "tx": 0, "ty": 0,
                    "angle": angle
                }
                self.transform_list.append(transform_data)
                if self.x_rotate.text() or self.y_rotate.text():
                    self.controller.show_popup(
                        "Erro", "Para rotacionar em torno do centro, não é necessário informar x e y",
                        QtWidgets.QMessageBox.Icon.Critical
                    )
                    return

            elif self.rotate_point_button.isChecked():
                transform_data = {
                    "type": "rotate_point",
                    "tx": self.get_x_rotate(),
                    "ty": self.get_y_rotate(),
                    "angle": angle
                }
                self.transform_list.append(transform_data)
        elif self.tabWidget.currentIndex() == 2:  # Escalonamento
            transform_data = {
                "type": "scale",
                "tx": self.get_x_scale(),
                "ty": self.get_y_scale(),
                "angle": None
            }	
            self.transform_list.append(transform_data)

        else:
            return None  # Caso não haja transformação válida

        return self.transform_list

    def add_transform_display(self):
        text = None
        if self.tabWidget.currentIndex() == 0:
            text = f"Translação nos pontos {int(self.get_x_translate())} {int(self.get_y_translate())}"
            self.transform_list_display.append(text)
            self.confirm_transform()
              
        elif self.tabWidget.currentIndex() == 1:
            if self.rotate_origin_button.isChecked():
                text = f"Rotação em torno da origem com {int(self.get_angle())} graus"
                self.transform_list_display.append(text)
                self.confirm_transform()  # Apenas adiciona na lista
                
            elif self.rotate_center_button.isChecked():
                text = f"Rotação em torno do centro do objeto {int(self.get_angle())} graus"
                self.transform_list_display.append(text)
                self.confirm_transform()  # Apenas adiciona na lista
                
            elif self.rotate_point_button.isChecked():
                text = f"Rotação em torno do ponto: ({int(self.get_x_rotate())}, {int(self.get_y_rotate())}) com {int(self.get_angle())} graus"
                self.transform_list_display.append(text)
                self.confirm_transform()
                
        elif self.tabWidget.currentIndex() == 2:
            text = f"Escalonamento no ponto: ({int(self.get_x_scale())}, {int(self.get_y_scale())})"
            self.transform_list_display.append(text)
            self.confirm_transform()  # Apenas adiciona na lista
            
        if text is not None:
            self.transform_added = True
        else:
            self.transform_added = False
        self.update_display_transform()
    
    def confirm_transform_and_transform(self):
        if self.transform_added:
            self.controller.transform_object(self.transform_list)  # Chama a função sem parâmetros (ela busca na lista)
        else:
            self.controller.show_popup(
                "Erro", "É necessário adicionar as transformações antes de prosseguir!",
                QtWidgets.QMessageBox.Icon.Critical
            )

    def get_x_translate(self):
        return float(self.x_translate.text().strip())

    def get_y_translate(self):
        return float(self.y_translate.text().strip())
    
    def get_x_scale(self):
        return float(self.x_scaling.text().strip())
    
    def get_y_scale(self):
        return float(self.y_scaling.text().strip())

    def get_angle(self):
        angle = float(self.angulo_input.text().strip())
        print(f'angle: {angle}')
        return angle
    
    def get_x_rotate(self):
        return float(self.x_rotate.text().strip())
    
    def get_y_rotate(self):
        return float(self.y_rotate.text().strip())
    
    def update_display_transform(self):
        self.display_transform.clear()
        for transform in self.transform_list_display:
            self.display_transform.addItem(transform)
            print(transform)
        self.display_transform.show()