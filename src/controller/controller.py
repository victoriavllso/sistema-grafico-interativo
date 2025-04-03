from src.model.window import Window
from src.model.window import Window
from src.model.viewport import Viewport
from src.model.graphic_objects.point import Point
from src.model.graphic_objects.line import Line
from src.model.graphic_objects.wireframe import Wireframe
from src.view.transform_view.transform_window import TransformWindow
from src.model.transform import Transform
from src.model.display.display_file import DisplayFile
from src.utils.utils import *
from src.view.main_view.main_window import MainWindow
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPainter
from src.model.display.display_transform import DisplayTransform
from src.utils.gui_utils import GUIUtils

class Controller:
    def __init__(self):
        self.display_file = DisplayFile()
        self.display_transform = DisplayTransform()

        self.viewport = Viewport()
        self.window = Window()
        self.transform_window = None
        self.transform = Transform()
        self.main_window = MainWindow(self)
        self.main_window.show()

    @staticmethod
    def parse_coordinates(input_text: str) -> list:
        """Converte uma string de coordenadas em uma lista de pontos."""
        try:
            pontos = list(eval(input_text))
            return pontos
        except Exception:
            return []

    def create_object(self):
        """Cria um objeto gráfico com base nas informações fornecidas pelo usuário."""
        try:
            points_input = self.main_window.points_ln.text().strip()
            color = self.main_window.color

            if not points_input:
                GUIUtils.show_popup("Erro", "Coordenadas inválidas", QMessageBox.Icon.Critical)
                return

            name = self.main_window.name_ln.text()

            if name in [obj.name for obj in self.display_file.get_all()]:
                GUIUtils.show_popup("Erro", "Nome de objeto inválido: O nome do objeto já existe", QMessageBox.Icon.Critical)
                return

            points = self.parse_coordinates(points_input)

            if points == []:
                GUIUtils.show_popup("Erro", "Coordenadas inválidas", QMessageBox.Icon.Critical)
                return
            
            if (len(points) > 2 or len(points) == 2) and all(isinstance(p, tuple) for p in points) and not name:
                GUIUtils.show_popup("Erro", "Nome inválido: O nome do objeto não pode ser vazio", QMessageBox.Icon.Critical)
                return

            if len(points) == 2 and not name:
                name = f"point_{self.display_file.get_num_points() + 1}"

            if len(points) == 2 and all(isinstance(p, int) for p in points):
                x, y = points[0], points[1]
                obj = Point(name=name, x=x, y=y, color=color)
            elif len(points) == 2 and all(isinstance(p, tuple) for p in points):
                x1, y1, x2, y2 = points[0][0], points[0][1], points[1][0], points[1][1]
                point0, point1 = Point(x=x1, y=y1), Point(x=x2, y=y2)
                obj = Line(name=name, point1=point0, point2=point1, color=color)
            elif len(points) > 2:
                points = [Point(x=x, y=y) for x, y in points]
                try:
                    obj = Wireframe(name=name, points=points, color=color)
                except Exception:
                    GUIUtils.show_popup("Erro", "Wireframe inválido!", QMessageBox.Icon.Critical)
                    return

            self.display_file.add(obj)
            self.main_window.update_viewport()

        except ValueError as e:
            GUIUtils.show_popup("Erro", str(e), QMessageBox.Icon.Critical)

    def delete_object(self, obj_name):
        """Remove o objeto selecionado do arquivo de exibição."""
        self.display_file.remove(obj_name)
        self.main_window.update_viewport()

    def open_transform_window(self):
        """Abre a janela de transformação para o objeto selecionado."""
        selected_object = self.get_object_from_display()

        if selected_object is None:
            GUIUtils.show_popup("Erro", "Nenhum objeto selecionado!", QMessageBox.Icon.Critical)
            return
        if self.transform_window is None:
            self.transform_window = TransformWindow(self)

        self.transform_window.show()
    
    def move_window(self, direction):
        """Move a janela de visualização na direção especificada."""
        move_actions = {
            "up": self.window.up,
            "down": self.window.down,
            "left": self.window.left,
            "right": self.window.right
        }
        move_function = move_actions.get(direction)
        if move_function is None:
            return
        move_function()
        self.main_window.update_viewport()

    def zoom(self, action):
        """Aplica zoom na janela de visualização."""
        if not self.window:
            return
        zoom_actions = {
            "in": self.window.z_in,
            "out": self.window.z_out
        }
        zoom_function = zoom_actions.get(action)
        if zoom_function is None:
            return
        zoom_function()
        self.main_window.update_viewport()
  
    def transform_object(self):
        """Aplica a transformação ao objeto selecionado."""
        selected_object = self.get_object_from_display()

        if not selected_object:
            GUIUtils.show_popup("Erro", "Nenhum objeto selecionado para transformar!", QMessageBox.Icon.Critical)
            return

        for transform in self.display_transform.get_all():
            tr_type = transform.get("type")
            tx = transform.get("tx")
            ty = transform.get("ty")
            angle = transform.get("angle")

            if tr_type not in {"translate", "scale", "rotate_origin", "rotate_point", "rotate_center"}:
                GUIUtils.show_popup("Erro", "Tipo de transformação inválido", QMessageBox.Icon.Critical)

            if (tx is None or ty is None) and tr_type != "rotate_point":
                GUIUtils.show_popup("Erro", "Valores de transformação inválidos", QMessageBox.Icon.Critical)
                return

            if tr_type == "translate":
                self.transform.translate_object(selected_object, tx, ty)
            
            elif tr_type == "scale":
                self.transform.scale_object(selected_object, tx, ty)

            elif tr_type == "rotate_origin":
                self.transform.rotate_object(selected_object, angle, True)

            elif tr_type == "rotate_point":
                self.transform.rotate_object(selected_object, angle, True, int(tx), int(ty))

            elif tr_type == "rotate_center":
                self.transform.rotate_object(selected_object, angle, False)

        self.display_transform.clear()
        self.transform_window.update_display()
        self.main_window.update_viewport()

    def get_object_from_display(self) -> object:
        """Retorna o objeto selecionado na lista de exibição."""
        return self.display_file.get_object(self.main_window.get_name())

    def draw_objects(self, painter: QPainter) -> None:
        """Desenha os objetos na área de visualização."""
        for obj in self.display_file.get_all(): 
            obj.draw(painter, self.viewport, self.window)
