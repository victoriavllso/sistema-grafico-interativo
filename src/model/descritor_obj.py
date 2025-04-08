from src.model.graphic_objects.point import Point
from src.model.graphic_objects.line import Line
from src.model.graphic_objects.wireframe import Wireframe

from PyQt6.QtGui import QColor

class DescritorOBJ:
    @staticmethod
    def from_obj_file(filename) -> list:
        """Lê um arquivo .obj e retorna uma lista de objetos gráficos."""
        with open(filename, 'r') as file:
            lines = file.readlines()
            objects = []

            current_object = None

            current_type = None
            current_name = None
            current_material = None
            current_points = None
            
            points = {}
            materials = {}

            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if line.startswith("mtllib"):
                    # Lê a biblioteca de materiais
                    _, lib_name = line.split()
                    import os
                    mtl_path = os.path.join(os.path.dirname(filename), lib_name)
                    materials = DescritorOBJ.read_material_library(mtl_path)
                elif line.startswith("v"):
                    # Lê os pontos
                    _, x, y, z = line.split()
                    point = (float(x), float(y))
                    points[len(points)+1] = point
                elif line.startswith("o"):
                    # Lê o nome do objeto
                    _, current_name = line.split()
                elif line.startswith("usemtl"):
                    # Lê o material atual
                    _, current_material = line.split()
                    if current_material in materials:
                        current_material = materials[current_material]['color']
                elif line and line[0] in ['w', 'l', 'f', 'p']:
                    tokens = line.split()
                    current_type = tokens[0]
                    indices = list(map(int, tokens[1:]))
                    current_points = [points[i] for i in indices]
                    if len(current_points) == 1:
                        current_points = current_points[0]
                    current_object = {
                        "name": current_name,
                        "type": current_type,
                        "points": current_points,
                        "material": current_material
                    }
                    objects.append(current_object)
                    current_object = None
                    current_type = None
                    current_name = None
                    current_material = None
                    current_points = None
            return objects

    @staticmethod
    def objString_file(objects, filename) -> None:
        """Escreve uma lista de objetos em um arquivo .obj e gera um .mtl associado."""
        import os
        base_name = os.path.splitext(os.path.basename(filename))[0]
        mtl_name = f"{base_name}.mtl"
        mtl_path = os.path.join(os.path.dirname(filename), mtl_name)

        with open(filename, 'w') as file:
            file.write("# Exported .obj file\n")
            file.write(f"mtllib {mtl_name}\n\n")

            materials = {}
            points = {}
            for obj in objects:
                if isinstance(obj, Point):
                    points[(obj.x, obj.y)] = len(points) + 1
                elif isinstance(obj, Line):
                    points[(obj.x1(), obj.y1())] = len(points) + 1
                    points[(obj.x2(), obj.y2())] = len(points) + 1
                elif isinstance(obj, Wireframe):
                    for point in obj.points:
                        points[(point.x, point.y)] = len(points) + 1
                materials[obj.name] = obj.color
            for point, index in points.items():
                file.write(f"v {point[0]} {point[1]} 0\n")
            file.write("\n")
            DescritorOBJ.write_material_library(mtl_path, materials)
            for obj in objects:
                file.write(f"o {obj.name}\n")
                file.write(f"usemtl {obj.name}\n")
                if isinstance(obj, Point):
                    file.write(f"p {points[(obj.x, obj.y)]}\n")
                elif isinstance(obj, Line):
                    file.write(f"l {points[(obj.x1(), obj.y1())]} {points[(obj.x2(), obj.y2())]}\n")
                elif isinstance(obj, Wireframe):
                    file.write(f"l {' '.join(str(points[(point.x, point.y)]) for point in obj.points)}\n")

    @staticmethod
    def read_material_library(lib_name):
        """Lê uma biblioteca de materiais .mtl e retorna um dicionário de materiais."""
        materials = {}
        with open(lib_name, 'r') as file:
            lines = file.readlines()
            current_material = None
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if line.startswith("newmtl"):
                    _, material_name = line.split()
                    current_material = material_name
                    materials[current_material] = {}
                elif current_material is not None:
                    if line.startswith("Kd"):
                        _, r, g, b = line.split()
                        materials[current_material]['color'] = (float(r), float(g), float(b))
        return materials
    
    @staticmethod
    def write_material_library(mtl_path, materials):
        """Escreve uma biblioteca de materiais .mtl a partir de um dicionário de materiais."""
        with open(mtl_path, 'w') as mtl_file:
            for name, color in materials.items():
                qcolor = QColor(color)  # Isso aceita tanto Qt.GlobalColor quanto QColor
                r, g, b = qcolor.redF(), qcolor.greenF(), qcolor.blueF()
                mtl_file.write(f"newmtl {name}\n")
                mtl_file.write(f"Kd {r:.4f} {g:.4f} {b:.4f}\n\n")  # Difuse color
