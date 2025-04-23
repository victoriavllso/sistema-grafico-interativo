from src.model.descritor_obj import DescritorOBJ
from src.model.transform import Transform
from src.model.clipping import Cliper

from src.model.display.display_transform import DisplayTransform
from src.model.display.display_file import DisplayFile

from src.model.viewport import Viewport
from src.model.window import Window

from src.model.graphic_objects.point import Point
from src.model.graphic_objects.line import Line
from src.model.graphic_objects.wireframe import Wireframe
from src.model.graphic_objects.bezier import Bezier
from src.model.graphic_objects.bspline import BSpline

from src.utils.utils import *
from src.utils.gui_utils import GUIUtils

from src.view.transform_view.transform_window import TransformWindow
from src.view.main_view.main_window import MainWindow
from src.view.obj_view.obj_window import OBJDialog
from src.view.create_object_view.create_object_window import CreateObjectWindow

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QColor


class Controller:
    def __init__(self):
        self.display_file = DisplayFile()
        self.display_transform = DisplayTransform()
        self.viewport = Viewport()
        self.window = Window()
        self.transform_window = None
        self.obj_window = None
        self.bezier_window = None
        self.create_object_window = None
        self.transform = Transform()
        self.cliper = Cliper(self.window, self.viewport)
        self.descritor_obj = DescritorOBJ()
        self.main_window = MainWindow(self)
        self.main_window.show()

    #---------- Graphic Objects ----------#

    def open_create_window(self):
        """Abre a janela de criação de objetos gráficos."""
        self.create_object_window = CreateObjectWindow(self)
        self.create_object_window.show()

    def create_object(self, points_input, color, type, filled, name) -> None:
        """Cria um objeto gráfico"""
        name = Controller.assign_default_name({"name": name}, self.display_file)
        name = name["name"]
        obj = None # objeto unico
        objects = [] # lista de objetos (bezier, por exemplo)
        if type == "point":
            try:
                obj = Point(window=self.window, name=name, x=points_input[0], y=points_input[1], color=color)
            except Exception:
                GUIUtils.show_popup("Erro", "Ponto inválido!", QMessageBox.Icon.Critical)
                return
            
        elif type == "line":
            try:
                point0, point1 = Point(window=self.window, x=points_input[0][0], y=points_input[0][1]), Point(window=self.window, x=points_input[1][0], y=points_input[1][1])
                obj = Line(window=self.window, name=name, point1=point0, point2=point1, color=color)
            except Exception:
                GUIUtils.show_popup("Erro", "Linha inválida!", QMessageBox.Icon.Critical)
                return

        elif type == "wireframe":
            try:
                points = [Point(window=self.window, x=x, y=y) for x, y in points_input]
                obj = Wireframe(window=self.window, name=name, points=points, color=color, filled=filled)
            except Exception:
                GUIUtils.show_popup("Erro", "Wireframe inválido!", QMessageBox.Icon.Critical)
                return
        
        elif type == "bezier":
            try:
                if len(points_input) >= 4:
                    for i in range(0, len(points_input) - 3,3):
                        bezier_points = points_input[i:i+4]
                        points = [Point(window=self.window, x=x, y=y) for x, y in bezier_points]
                        bezier_obj = Bezier(window=self.window, name=f"{name}_{i//3}", points=points, color=color)
                        objects.append(bezier_obj)
                   
            except Exception as e:
                GUIUtils.show_popup("Erro", "Bezier inválido!", QMessageBox.Icon.Critical)
                return
        
        elif type == "spline":
            try:
                if len(points_input) >= 4:
                    for i in range(0, len(points_input) - 3,3):
                        spline_points = points_input[i:i+4]
                        points = [Point(window=self.window, x=x, y=y) for x, y in spline_points]
                        spline_obj = BSpline(window=self.window, name=f"{name}_{i//3}", points=points, color=color)
                        objects.append(spline_obj)
         
            except Exception:
                GUIUtils.show_popup("Erro", "Spline inválido!", QMessageBox.Icon.Critical)
                return
        else:
            GUIUtils.show_popup("Erro", "Tipo de objeto inválido!", QMessageBox.Icon.Critical)
            return
        
        if obj:
            self.display_file.add(obj)
        elif objects:
            for obj in objects:
                self.display_file.add(obj)
        self.main_window.update_viewport()

    def draw_objects(self, painter: QPainter) -> None:
        """Desenha os objetos na área de visualização."""
        graphic_objects = self.display_file.get_all()
        clipping_algorithm = self.main_window.get_clipping_algorithm()
        self.cliper.clip_object(graphic_objects, clipping_algorithm)

        for obj in graphic_objects:
            if all(getattr(p, "inside_window", False) for p in getattr(obj, "points", [])) or isinstance(obj, Bezier):
                obj.draw(painter, self.viewport)
            for p in getattr(obj, "points", []):
                p.inside_window = False

    def delete_object(self, obj_name) -> None:
        """Remove o objeto selecionado do arquivo de exibição."""
        self.display_file.remove(obj_name)
        self.main_window.update_viewport()

    def get_object_from_display(self) -> object:
        """Retorna o objeto selecionado pelo nome."""
        return self.display_file.get_object(self.main_window.get_selected_name_in_display())

    #---------- Métodos de Transformação ----------#

    def open_transform_window(self) -> None:
        """Abre a janela de transformação para o objeto selecionado."""
        selected_object = self.get_object_from_display()

        if selected_object is None:
            GUIUtils.show_popup("Erro", "Nenhum objeto selecionado!", QMessageBox.Icon.Critical)
            return

        self.transform_window = TransformWindow(self, selected_object)
        self.transform_window.show()

    def append_transform(self, transform: dict) -> None:
        """Adiciona uma transformação à lista de transformações a serem aplicadas."""
        if not transform:
            GUIUtils.show_popup("Erro", "Nenhuma transformação selecionada!", QMessageBox.Icon.Critical)
            return

        self.display_transform.add(transform)
        self.transform_window.update_display()
        self.main_window.update_viewport()

    def delete_transform(self):
        """Remove a transformada selecionada no display"""
        self.display_transform.remove(self.transform_window.get_selected_in_display())
        self.transform_window.update_display()
  
    def transform_object(self, selected_object) -> None:
        """Aplica a transformação ao objeto selecionado."""
        if not selected_object:
            GUIUtils.show_popup("Erro", "Nenhum objeto selecionado para transformar!", QMessageBox.Icon.Critical)
            return

        transform_types = {0: "translate", 1: "rotate", 2: "scale"}
        
        for transform in self.display_transform.get_all():
            tr_type = transform_types.get(transform.get("type"))

            if tr_type == "translate":
                dx = transform.get("x_translate")
                dy = transform.get("y_translate")
                self.transform.translate_object(selected_object, dx, dy)
            elif tr_type == "scale":
                sx = transform.get("x_scale")
                sy = transform.get("y_scale")
                self.transform.scale_object(selected_object, sx, sy)
            elif tr_type == "rotate":
                angle = transform.get("angle")

                if transform.get("type_rotate") == "rotate_origin":
                    self.transform.rotate_object(selected_object, angle)
                elif transform.get("type_rotate") == "rotate_point":
                    x = transform.get("x_rotate")
                    y = transform.get("y_rotate")
                    self.transform.rotate_object(selected_object, angle, x, y)
                elif transform.get("type_rotate") == "rotate_center":
                    x = selected_object.geometric_center()[0]
                    y = selected_object.geometric_center()[1]
                    self.transform.rotate_object(selected_object, angle, x, y)

        self.display_transform.clear()
        self.transform_window.update_display()
        self.main_window.update_viewport()

    #---------- Métodos de Janela de Visualização ----------#

    def move_window(self, direction) -> None:
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

    def zoom(self, action) -> None:
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
    
    def rotate_window(self, direction) -> None:
        """Rotaciona a janela de visualização na direção especificada."""
        direction_actions = {
            "left": self.window.rotate_window_left,
            "right": self.window.rotate_window_right
        }
        rotate_function = direction_actions.get(direction)
        if rotate_function is None:
            return
        angle = self.main_window.get_angle_rotation()

        if angle is None:
            GUIUtils.show_popup("Erro", "Ângulo inválido!", QMessageBox.Icon.Critical)
            return

        rotate_function(angle)
        self.main_window.update_viewport()

    def get_margin(self) -> None:
        """Calcula a margem da janela de visualização."""
        margin_x = int(VP_X_MAX * MARGIN_FACTOR)
        margin_y = int(VP_Y_MAX * MARGIN_FACTOR)
        return margin_x, margin_y

    #---------- Métodos de Importação/Exportação ----------#

    def open_obj_window(self) -> None:
        """Abre a janela de importação/exportação de arquivos OBJ."""
        self.obj_window = OBJDialog(self)
        self.obj_window.show()

    def import_obj(self) -> None:
        """Importa um arquivo OBJ e adiciona os objetos à exibição."""
        file_name = self.obj_window.select_file()
        if not file_name:
            return
        objs = self.descritor_obj.from_obj_file(file_name)
        for obj in objs:
            obj = Controller.assign_material_color(obj)
            obj = Controller.assign_default_name(obj, self.display_file)
            obj = Controller.assign_type(obj)
            self.create_object(points_input=obj["points"], color=obj["material"], name=obj["name"], filled=obj["filled"], type=obj["type"])

    def export_obj(self) -> None:
        """Exporta os objetos do mundo para um arquivo OBJ."""
        file_name = self.obj_window.select_file()
        if not file_name:
            return
        try:
            selected_objects = self.display_file.get_all()
            if selected_objects == []:
                GUIUtils.show_popup("Erro", "Nenhum objeto selecionado para exportar!", QMessageBox.Icon.Critical)
                return
            self.descritor_obj.objString_file(selected_objects, file_name)
            GUIUtils.show_popup("Sucesso", "Arquivo exportado com sucesso!", QMessageBox.Icon.Information)
        except Exception as e:
            GUIUtils.show_popup("Erro", str(e), QMessageBox.Icon.Critical)
            return

    #---------- Métodos Estáticos ----------#

    @staticmethod
    def assign_material_color(obj) -> dict:
        """Atribui uma cor de material ao objeto."""
        if obj["material"] is not None:
            r, g, b = obj["material"]
            obj["material"] = QColor(int(r * 255), int(g * 255), int(b * 255))
        else:
            obj["material"] = QColor(255, 0, 0)
        return obj

    @staticmethod
    def assign_default_name(obj, display_file) -> dict:
        """Atribui um nome padrão ao objeto, se não houver nome fornecido."""
        if obj["name"] is None or obj["name"] == "" or obj["name"] in display_file.get_all_names():
            obj["name"] = display_file.get_next_possible_name()
        return obj
    
    @staticmethod
    def assign_type(obj) -> dict:
        """Atribui o tipo de objeto ao objeto."""
        if obj["type"] == "p":
            obj["type"] = "point"
        elif obj["type"] == "l":
            if len(obj["points"]) == 2:
                obj["type"] = "line"
            else:
                obj["type"] = "wireframe"
        elif obj["type"] == "w":
            obj["type"] = "wireframe"
        elif obj["type"] == "curve":
            obj["type"] = "bezier"
        return obj

    @staticmethod
    def parse_coordinates(input_text: str) -> list:
        """Converte uma string de coordenadas em uma lista de pontos."""
        try:
            pontos = list(eval(input_text))
            return pontos
        except Exception:
            return []
