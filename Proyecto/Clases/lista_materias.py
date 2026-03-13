from dataclasses import dataclass
from typing import List

@dataclass
class Materia:
    def __init__(self, codigo, nombre, secciones):
        self.codigo = codigo
        self.nombre = nombre
        self.secciones = secciones

    def datos_materia(self):
        return f"[{self.codigo}] {self.nombre} ({self.secciones} secciones)"


