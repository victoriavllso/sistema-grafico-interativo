from src.view.transform_view.gui_transform import Ui_Dialog, QtWidgets
from PyQt6.QtWidgets import QListWidget
from src.utils.utils import DT_X_MAX, DT_X_MIN, DT_Y_MAX, DT_Y_MIN
from PyQt6.QtCore import Qt


class TransformWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, controller):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.controller = controller
        
        self.display = QListWidget(self)
        self.display.setGeometry(DT_X_MIN, DT_Y_MIN, DT_X_MAX, DT_Y_MAX)

    def initUI(self):
        self.ok_cancel_transform.accepted.connect(self.confirm_transform_and_transform)
        self.ok_cancel_transform.rejected.connect(self.reject)
        self.add_transform_button.clicked.connect(self.add_transform_display)
    
    def add_transform_display(self) -> dict:
        """Retorna um dicionário com os dados da transformação."""
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


        if transform_data is None:
            self.controller.show_popup(
                "Erro", "Selecione uma transformação válida.",
                QtWidgets.QMessageBox.Icon.Critical
            )
            return None
        else:
            self.controller.display_transform.add(transform_data)
            self.update_display()
            return transform_data
    
    def confirm_transform_and_transform(self):
        """Aplica as transformações."""
        self.controller.transform_object()

    def update_display(self):
        """Atualiza o display de transformações."""
        self.display.clear()
        self.display.addItem("Transformações: \n")
        for transform in self.controller.display_transform.get_all():
            self.display.addItem(transform["text"])
        self.display.show()
    
    def get_x_translate(self) -> float:
        return self._parse_float(self.x_translate.text())

    def get_y_translate(self) -> float:
        return self._parse_float(self.y_translate.text())

    def get_x_scale(self) -> float:
        return self._parse_float(self.x_scaling.text())

    def get_y_scale(self) -> float:
        return self._parse_float(self.y_scaling.text())

    def get_angle(self) -> float:
        return self._parse_float(self.angulo_input.text())

    def get_x_rotate(self) -> float:
        return self._parse_float(self.x_rotate.text())

    def get_y_rotate(self) -> float:
        return self._parse_float(self.y_rotate.text())

    def get_name(self) -> str:
        return self.name_ln.text().strip()

    @staticmethod
    def _parse_float(value: str) -> float:
        """Tenta converter uma string para float, retorna 0.0 se inválido."""
        try:
            return float(value.strip())
        except ValueError:
            return 0.0  # Ou None, dependendo da lógica

