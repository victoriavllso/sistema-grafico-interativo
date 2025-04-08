from abc import ABC, abstractmethod

class Display(ABC):
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.list = []
    
    def add(self, object:object) -> None:
        """Add an object to the display list"""
        self.list.append(object)

    def remove(self, name: str) -> None:
        """Remove an object from the display list by name"""
        for obj in self.list:
            if obj.name == name:
                self.list.remove(obj)
    
    def get_all(self) -> list:
        """Get all objects in the display list"""
        return self.list

    def get_object(self, name: str) -> object:
        """Get an object from the display list by name"""
        for obj in self.list:
            if obj.name == name:
                return obj
            
    def clear(self) -> None:
        """Clear the display list"""
        self.list.clear()
