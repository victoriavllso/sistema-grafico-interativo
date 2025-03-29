from model.window import Window
from model.window import Window
from model.viewport import Viewport
from model.point import Point
from model.line import Line
from model.wireframe import Wireframe
from model.transform_window import TransformWindow
from model.transform import Transform
from model.display_file import DisplayFile
from model.utils import *

from PyQt6.QtWidgets import QMessageBox

class Controller:
    def __init__(self, ui):
        self.ui = ui
        self.display_file = DisplayFile()
        self.viewport = Viewport()
        self.window = Window()
        self.transform_window = None
        self.transform = Transform()
        self.selected_object = None

  
    def create_object(self):
        
        points_input = self.ui.points_ln.text().strip()
        print(f'pontos input: {points_input}')
    
        # points_input validation
        if not points_input:
            self.show_popup("Erro", "Coordenadas vazias", QMessageBox.Icon.Critical)
            return

        name = self.ui.name_ln.text()

        # name validation
        if name in [obj.name for obj in self.display_file.get_all()]:
            self.show_popup("Erro", "Nome de objeto : Nome ja está em uso", QMessageBox.Icon.Critical)
            return

        points = self.parse_coordinates(points_input)

        # points validation
        if points == []:
            self.show_popup("Erro", "Coordenadas inválidas", QMessageBox.Icon.Critical)
            return
        
        if (len(points) > 2 or len(points) == 2) and all(isinstance(p, tuple) for p in points) and not name:
            self.show_popup("Erro", "Nome de objeto inválido: O objeto que você deseja criar precisa de um nome", QMessageBox.Icon.Critical)
            return
        
        if len(points) == 2 and not name:
            name = f"point_{len(self.display_file.get_all())}"

        # Decide which object to create
        if len(points) == 2 and all(isinstance(p, int) for p in points):
            x, y = points[0], points[1]
            obj = Point(name=name, x=x, y=y)

        elif len(points) == 2 and all(isinstance(p, tuple) for p in points):
            x1, y1, x2, y2 = points[0][0], points[0][1], points[1][0], points[1][1]
            point0, point1 = Point(x=x1, y=y1), Point(x=x2, y=y2)
            obj = Line(name= name, point1=point0, point2=point1)

        elif len(points) > 2:
            points = [Point(x=x, y=y) for x, y in points]
            try:
                obj = Wireframe(name=name, points=points)
            except Exception:
                self.show_popup("Erro", "O Objeto informado não é um polígono válido", QMessageBox.Icon.Critical)
                return
    
        # Add object to display file and update viewport
        self.display_file.add(obj)
        self.ui.update_viewport()

    def open_transform_window(self):
        self.update_selected_object()

        if self.selected_object is None:
            self.show_popup("Erro", "Nenhum objeto selecionado para transformar!", QMessageBox.Icon.Critical)
            return
        if self.transform_window is None:
            self.transform_window = TransformWindow(self)
        self.transform_window.show()
    
    def delete_object(self, obj_name):
        self.display_file.remove(obj_name)
        self.ui.update_viewport()
    
    def move_window(self, direction):
        move_actions = {
            "up": self.window.up,
            "down": self.window.down,
            "left": self.window.left,
            "right": self.window.right
        }
        move_function = move_actions.get(direction)
        if move_function is None:
            print("acao invalida")
            return
        move_function()
        self.ui.update_viewport()

    def zoom(self, action):
        if not self.window:
            print("window nao inicializada")
            return
        zoom_actions = {
            "in": self.window.z_in,
            "out": self.window.z_out
        }
        zoom_function = zoom_actions.get(action)
        if zoom_function is None:
            print("acao invalida")
            return
        zoom_function()
        self.ui.update_viewport()

    def parse_coordinates(self, input_text: str) -> list:
        try:
            pontos = list(eval(input_text))
            return pontos
        except Exception:
            return []
        

    def show_popup(self, title:str = "standart", message:str = "standart", icon:QMessageBox.Icon = QMessageBox.Icon.Information):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
  

    def transform_object(self,tx,ty,type):
        self.update_selected_object()
        print(f'objeto selecionado: {self.selected_object}')
        if not self.selected_object:
            self.show_popup("Erro", "Nenhum objeto selecionado para transformar!", QMessageBox.Icon.Critical)
            return
        #tx, ty , type =self.transform_window.confirm_transform()

        if not tx or not ty:
            self.show_popup("Erro", "Valores de transformação inválidos", QMessageBox.Icon.Critical)
            return

        if type == "translate":
            print(f'tranlação chamada no controller com tx: {tx} e ty: {ty}')
            self.transform.translate_object(self.selected_object,tx,ty)
            print(f'coordenadas depois de transladar o objeto: x1:{self.selected_object.point1.x}, y1: {self.selected_object.point1.y} e x2: {self.selected_object.point2.x}, y2: {self.selected_object.point2.y}')
            print('fim translação')
        if type == "scale":
            print(f'escalonamento chamado no controller com tx: {tx} e ty: {ty}')
            self.transform.scale_object(self.selected_object,tx,ty)

 
        self.ui.update_viewport()
    def update_selected_object(self):
        obj_name = self.ui.name_ln.text().strip()
        self.selected_object = self.display_file.get_selected_object(obj_name)
