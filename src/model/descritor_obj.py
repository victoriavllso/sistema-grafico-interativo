from src.model.graphic_objects.point import Point
from src.model.graphic_objects.line import Line
from src.model.graphic_objects.wireframe import Wireframe

class DescritorOBJ:
    @staticmethod
    def from_obj_file(filename) -> list:
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
                elif line[0] in ['w', 'l', 'f', 'p']:
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
                    print(f"Object: {current_object}, Type: {current_type}, Points: {current_points}, Material: {current_material}")
                    objects.append(current_object)
                    current_object = None
                    current_type = None
                    current_name = None
                    current_material = None
                    current_points = None
            return objects

    @staticmethod
    def objString_file(objects, filename) -> None:
        """Escreve uma lista de objetos em um arquivo .obj."""
        with open(filename, 'w') as file:
            file.write("# Exported .obj file\n")

            vertex_list = []
            index_map = {}  # Map: object -> index in vertex_list
            current_index = 1  # OBJ indices start at 1

            # Categorizar os objetos por tipo
            pontos = []
            retas = []
            wireframes = []

            for obj in objects:
                if isinstance(obj, Point):
                    pontos.append(obj)
                elif isinstance(obj, Line):
                    retas.append(obj)
                elif isinstance(obj, Wireframe):
                    wireframes.append(obj)

            # Escreve os pontos
            if pontos:
                for p in pontos:
                    file.write(f"v {p.x} {p.y} 0.0\n")
                    index_map[p] = current_index
                    file.write(f"l {current_index}\n")
                    current_index += 1

            # Escreve as retas
            if retas:
                for r in retas:
                    p1, p2 = r.points[0], r.points[1]
                    for p in (p1, p2):
                        if p not in index_map:
                            file.write(f"v {p.x} {p.y} 0.0\n")
                            index_map[p] = current_index
                            current_index += 1
                    i1 = index_map[p1]
                    i2 = index_map[p2]
                    file.write(f"l {i1} {i2}\n")

            # Escreve os wireframes
            if wireframes:
                for wf in wireframes:
                    indices = []
                    for p in wf.points:
                        if p not in index_map:
                            file.write(f"v {p.x} {p.y} 0.0\n")
                            index_map[p] = current_index
                            current_index += 1
                        indices.append(index_map[p])
                    file.write("l " + " ".join(map(str, indices)) + "\n")

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
    
    def write_material_library(lib_name, materials):
        """Escreve uma biblioteca de materiais .mtl."""
        with open(lib_name, 'w') as file:
            for material_name, properties in materials.items():
                file.write(f"newmtl {material_name}\n")
                if 'color' in properties:
                    r, g, b = properties['color']
                    file.write(f"Kd {r} {g} {b}\n")
                if 'texture' in properties:
                    file.write(f"map_Kd {properties['texture']}\n")
        file.write("\n")
        file.write(f"# End of material library {lib_name}\n")

