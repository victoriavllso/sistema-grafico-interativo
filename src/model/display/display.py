from abc import ABC, abstractmethod

class Display(ABC):
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.list = []
    
    def add(self, object) -> None:
        self.list.append(object)

    def remove(self, name: str) -> None:
        for obj in self.list:
            if obj.name == name:
                self.list.remove(obj)
    
    def get_all(self) -> list:
        return self.list

    def get_object(self, name: str) -> object:
        for obj in self.list:
            if obj.name == name:
                return obj
            
    def clear(self) -> None:
            self.list.clear()
