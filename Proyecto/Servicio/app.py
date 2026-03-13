import requests
from Clases.lista_materias import Materia
from Clases.lista_profesores import Docente
from Datos.Profesores import datos_crudos
from Datos.Materias import lista_materia
class App:
    def __init__(self):
        self.materia = []
        self.profesor = []
    
    def run(self):
        self.profesor = [
            Docente(
                cedula=item["Cedula"],
                email=item["Email"],
                apellido=item["Apellido"],
                nombre=item["Nombre"],
                max_carga=item["Max Carga"],
                materias=item["Materias"]
            ) for item in datos_crudos
        ]
        self.materia = [
            Materia(
                codigo=item["Código"],
                nombre=item["Nombre"],
                secciones=item["Secciones"]
            ) for item in lista_materia
        ]
        
        while True:
            print("""
1. Profesores
2. Materias
3. Generación de horarios
4. Modificación de horarios
0. Salir
""")
            menu = int(input("Ingrese un numero para escoger entre las siguientes opciones: "))
            if menu == 0:
                break
            elif menu == 1:
                self.profesores()
            elif menu == 2:
                self.materia()
            elif menu == 3:
                self.crear_horario()
    
    def profesores(self):
        while True:
            print("""
1. Lista de profesores
2. Ver un profesor especifico
3. Agregar un profesor a la lista
4. Eliminar un profesor de la lista
5. Modificar la lista de materias de un profesor 
0. Regresar
""")
            menu_profesores = int(input("Ingrese un numero para escoger entre las siguientes opciones: "))
            if menu_profesores == 0:
                break
            elif menu_profesores == 1:
                for item in self.profesor:
                    print(item.datos_profesor())
            elif menu_profesores == 2:
                pass
            elif menu_profesores == 3:
                pass
            elif menu_profesores == 4:
                pass
            elif menu_profesores == 5:
                pass

    def modificar_lista_materias(self):
        x = int(input("Ingrese la ci del profesor: "))
        tmp = None
        for i in self.profesor:
            if x == i:
                tmp = i
                break
        while True:
            z = input("Que desea hacer 1. agregar materia, 2 quitar materia")
            if z == 1:
            
                y = int(input("Ingrese codigo materia: "))
                for j in self.materias:
                    if j == y:
                        tmp.materias.append(j)
                        break

    def materia(self):
        while True:
            print("""
1. Lista de materias
2. Detalles de las materias
3. Profesores asociados con las materias
4. Agregar o eliminar materias
5. Modificar las secciones de las materias
0. Regresar
""")
            menu_materias = int(input("Ingrese un numero para escoger entre las siguientes opciones: "))
            if menu_materias == 0:
                break
            elif menu_materias == 1:
                for item in self.materia:
                    print(item.datos_materia())
            elif menu_materias == 2:
                pass
            elif menu_materias == 3:
                target = input("Que materia desea buscar: ")
                for item in self.materia:
                    if target == item.nombre:
                        for i in self.profesor:
                            if target in i.materias:
                                print(i.datos_profesor())
    
    def modificacion(self):
        while True:
            print("""

""")
            

    def crear_materia():
        salones = input()
        listaerrores = []
        [
            [
            
            ], []
        ]
        for i in self.materia():
            for j in self.profesor()
