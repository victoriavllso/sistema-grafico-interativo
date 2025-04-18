from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtGui import QPixmap
from src.utils.utils import *
from src.view.main_view.gui_main import Ui_main, QtWidgets
from PyQt6.QtWidgets import QListWidget, QColorDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPen

class MainWindow(QtWidgets.QMainWindow, Ui_main):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setupUi(self)
        self.initUI()

        self.canvas = QPixmap(self.controller.viewport.x_max - self.controller.viewport.x_min, self.controller.viewport.y_max - self.controller.viewport.y_min)
        self.canvas.fill(QColor("white"))
        self.painter = QPainter(self.canvas)
        self.vp.setPixmap(self.canvas)
        self.color = QColor("black")

        # Display
        self.display = QListWidget()
        self.display.setGeometry(self.controller.display_file.x_min, self.controller.display_file.y_min, self.controller.display_file.x_max, self.controller.display_file.y_max)
    
        # Display properties
        self.display.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.display.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.display.setMinimumHeight(50)
        self.display.setMinimumWidth(200)
        self.layout().addWidget(self.display)

        # desenha o subcanvas (borda)
        QTimer.singleShot(0, self.update_viewport)

    # Connect signals to slots
    def initUI(self):
        # colocando botões com desenho
        self.up.setText("\u2191")
        self.left.setText("\u2190")
        self.down.setText("\u2193")
        self.right.setText("\u2192")
        self.z_in.setText("\u2795")
        self.z_out.setText("\u2796")
        self.button_turn_window_left.setText("\u21b6")
        self.button_turn_window_right.setText("\u21b7")

        #botao de criação e deletar
        self.create_but.clicked.connect(lambda: self.controller.create_object(name=self.get_name(), color=self.color, points_input=self.get_points_input(), filled=self.get_filled()))
        self.delete_but.clicked.connect(lambda: self.controller.delete_object(self.get_selected_name_in_display()))
        
        # botoes de navegação
        self.up.clicked.connect(lambda: self.controller.move_window("up"))
        self.down.clicked.connect(lambda: self.controller.move_window("down"))
        self.left.clicked.connect(lambda: self.controller.move_window("left"))
        self.right.clicked.connect(lambda: self.controller.move_window("right"))
        self.z_in.clicked.connect(lambda: self.controller.zoom("in"))
        self.z_out.clicked.connect(lambda: self.controller.zoom("out"))
        
        # botao para abrir a janela de transformação
        self.transform_button.clicked.connect(lambda: self.controller.open_transform_window())
        self.color_button.clicked.connect(self.open_color_dialog)
        

        # rotação da windo3
        self.button_turn_window_left.clicked.connect(lambda: self.controller.rotate_window("left"))
        self.button_turn_window_right.clicked.connect(lambda: self.controller.rotate_window("right"))
        
        # botao para abrir a janela de obj
        self.actionObject_Files.triggered.connect(lambda: self.controller.open_obj_window())

        # botão para abrir a janela de bezier
        self.open_window_bezier_button.clicked.connect(lambda: self.controller.open_bezier_window())
        
    def update_viewport(self) -> None:
        """Atualiza a área de visualização."""
        self.canvas.fill(QColor("white"))
        if self.painter.isActive():
            self.painter.end()
        self.painter.begin(self.canvas)
        self.draw_subcanvas()
        self.controller.draw_objects(self.painter)
        self.painter.end()
        self.vp.setPixmap(self.canvas)
        self.update_display()

    def update_display(self) -> None:
        """Atualiza a lista de exibição com os objetos atuais."""
        self.display.clear()
        self.display.addItem("Objetos: \n")
        for obj in self.controller.display_file.get_all():
            self.display.addItem(f"{obj.name} - {obj.__class__.__name__}")
        self.display.show()

    def open_color_dialog(self) -> None:
        """Abre o diálogo de seleção de cor."""
        self.color = QColorDialog.getColor()

    def get_name(self) -> str:
        """Retorna o nome que o usuário deu de entrada."""
        return self.name_ln.text().strip()

    def draw_subcanvas(self) -> None:
        """Desenha o subcanvas (borda do retângulo de clipping) na área de visualização."""
        pen = QPen(QColor("red"))
        pen.setWidth(LINE_THICKNESS)
        self.painter.setPen(pen)
        margin_x, margin_y = self.controller.get_margin()
        aux = self.vp.rect().adjusted(margin_x, margin_y, -margin_x, -margin_y)
        self.painter.drawRect(aux)

    def get_angle_rotation(self) -> float:
        """Retorna o ângulo de rotação do campo de entrada."""
        try:
            angle = float(self.input_angle_window.text())
        except ValueError:
            return None
        return angle
    
    def get_selected_name_in_display(self) -> str:
        """Retorna o nome do objeto selecionado na lista de exibição."""
        selected_items = self.display.selectedItems()
        if selected_items:
            full_text = selected_items[0].text()
            name_part = full_text.split(' - ')[0]
            return name_part
        return None
    
    def get_points_input(self) -> list:
        """Retorna os pontos de entrada do usuário."""
        return self.parse_coordinates(self.points_ln.text().strip())

    @staticmethod
    def parse_coordinates(input_text: str) -> list:
        """Converte uma string de coordenadas em uma lista de pontos."""
        try:
            pontos = list(eval(input_text))
            return pontos
        except Exception:
            return []
        
    def get_clipping_algorithm(self) -> str:
        """Retorna o algoritmo de recorte selecionado pelo usuário."""
        if self.radioButton_barsky.isChecked():
            return "liang-barsky"
        return "cohen-sutherland"
        
    def get_filled(self) -> bool:
        """Retorna se o objeto deve ser preenchido ou não."""
        if self.radioButton.isChecked():
            return True
        return False
