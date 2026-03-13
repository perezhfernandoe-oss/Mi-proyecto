
from dataclasses import dataclass
from typing import List

@dataclass
class Docente:
    cedula: int
    email: str
    apellido: str
    nombre: str
    max_carga: int
    materias: List

    def datos_profesor(self):
        return f"{self.cedula} - {self.nombre} {self.apellido}"
       
