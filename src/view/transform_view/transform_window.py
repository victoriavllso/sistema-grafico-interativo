from src.view.transform_view.gui_transform import Ui_Dialog, QtWidgets
from PyQt6.QtWidgets import QListWidget
from src.utils.utils import DT_X_MAX, DT_X_MIN, DT_Y_MAX, DT_Y_MIN
from PyQt6.QtCore import Qt


class TransformWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, controller, object):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.controller = controller
        self.object = object

        self.display = QListWidget(self)
        self.display.setGeometry(DT_X_MIN, DT_Y_MIN, DT_X_MAX, DT_Y_MAX)

    def initUI(self):
        self.ok_cancel_transform.accepted.connect(self.confirm_transform)
        self.ok_cancel_transform.rejected.connect(self.reject)
        self.add_transform_button.clicked.connect(self.get_transform)
        self.add_transform_button_2.clicked.connect(lambda: self.controller.delete_transform())
    
    def get_transform(self):
        """Envia um dicionário com os dados da transformação."""
        text = self.generate_text()
        self.controller.append_transform( {
            "type": self.tabWidget.currentIndex(),
            "type_rotate": (
                "rotate_origin" if self.rotate_origin_button.isChecked() else
                "rotate_center" if self.rotate_center_button.isChecked() else
                "rotate_point" if self.rotate_point_button.isChecked() else None
            ),
            "name": self.get_name(),
            "x_translate": self.get_x_translate(),
            "y_translate": self.get_y_translate(),
            "x_scale": self.get_x_scale(),
            "y_scale": self.get_y_scale(),
            "angle": self.get_angle(),
            "x_rotate": self.get_x_rotate(),
            "y_rotate": self.get_y_rotate(),
            "text": text
        } )
    
    def confirm_transform(self):
        """Aplica as transformações."""
        self.controller.transform_object(self.object)

    def update_display(self):
        """Atualiza o display de transformações."""
        self.display.clear()
        self.display.addItem("Transformações: \n")
        for transform in self.controller.display_transform.get_all():
            self.display.addItem(transform["text"])
        self.display.show()

    def generate_text(self) -> str:
        """Gera o texto da transformação."""
        transform_text = ""
        if self.tabWidget.currentIndex() == 0:
            transform_text += f"Translação: ({self.get_x_translate()}, {self.get_y_translate()})"
        elif self.tabWidget.currentIndex() == 1:
            if self.rotate_origin_button.isChecked():
                transform_text += f"Rotação em torno da origem em {self.get_angle()} graus"
            elif self.rotate_center_button.isChecked():
                transform_text += f"Rotação em torno do ponto ({self.get_x_rotate()}, {self.get_y_rotate()}) em {self.get_angle()} graus"
            elif self.rotate_point_button.isChecked():
                transform_text += f"Rotação em torno do centro do objeto em {self.get_angle()} graus"
        elif self.tabWidget.currentIndex() == 2:
            transform_text += f"Escalonamento: ({self.get_x_scale()},{self.get_y_scale()})"
        return transform_text

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
        return self.controller.main_window.name_ln.text().strip()
    
    def get_selected_in_display(self) -> str:
        "Retorna a transformada selecionada no display"
        selected_items = self.display.selectedItems()
        if selected_items:
            return selected_items[0].text()
        return None

    @staticmethod
    def _parse_float(value: str) -> float:
        """Tenta converter uma string para float, retorna 0.0 se inválido."""
        try:
            return float(value.strip())
        except ValueError:
            return 0.0  # Ou None, dependendo da lógica
