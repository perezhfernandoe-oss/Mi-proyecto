import requests
from Clases.materia import Materia
from Clases.lista_profesores import Docente
from Datos.Profesores import datos_crudos
from Datos.Materias import lista_materia
class App:
    def __init__(self):
        self.materia = []
        self.profesor = []
    
    def cargar_datos(self):
        materia_dict = {}
        for item in lista_materia:
            cod = item["Código"]
            if cod in materia_dict:
                materia_dict[cod].secciones += item["Secciones"]
            else:
                materia_dict[cod] = Materia(
                    codigo=cod,
                    nombre=item["Nombre"],
                    secciones=item["Secciones"]
                )
        self.materia = list(materia_dict.values())
        
        # 2. Asignar objetos de materia a los profesores
        self.profesor = []
        for item in datos_crudos:
            materias_obj = [materia_dict[cod] for cod in item["Materias"] if cod in materia_dict]
            self.profesor.append(
                Docente(
                    cedula=item["Cedula"],
                    email=item["Email"],
                    apellido=item["Apellido"],
                    nombre=item["Nombre"],
                    max_carga=item["Max Carga"],
                    materias=materias_obj
                )
            )

    
    def run(self):
        while True:
            print("""
--- INICIO DEL SISTEMA ---
1. Cargar datos e ir al menú principal
2. Inicializar sistema sin cargar datos e ir al menú principal
3. Cargar datos y generar horario directamente
0. Salir
""")
            try:
                opc_inicio = int(input("Seleccione una opción: "))
            except ValueError:
                continue
                
            if opc_inicio == 0:
                return
            elif opc_inicio == 1:
                self.cargar_datos()
                break
            elif opc_inicio == 2:
                # Ya están inicializados vacíos en __init__
                break
            elif opc_inicio == 3:
                self.cargar_datos()
                self.crear_horario()
                break
                
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
                self.menu_materia()
            elif menu == 3:
                self.crear_horario()
            elif menu == 4:
                self.modificacion()
    
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
                termino = input("\nIngrese la cédula, nombre o apellido del profesor a buscar: ").strip().lower()
                encontrados = []
                for p in self.profesor:
                    if termino in str(p.cedula) or termino in p.nombre.lower() or termino in p.apellido.lower():
                        encontrados.append(p)
                
                if encontrados:
                    print("\n--- Resultados de la búsqueda ---")
                    for p in encontrados:
                        print(p.datos_profesor())
                        print(f"Email: {p.email}")
                        print(f"Carga Máxima: {p.max_carga}")
                        if p.materias:
                            print("Materias asignadas:")
                            for m in p.materias:
                                print(f"  - {m.codigo} {m.nombre}")
                        else:
                            print("Materias asignadas: Ninguna")
                        print("-" * 33)
                else:
                    print("\nNo se encontró ningún profesor que coincida con la búsqueda.")
            elif menu_profesores == 3:
                print("\n--- Agregar nuevo profesor ---")
                try:
                    cedula = int(input("Ingrese la cédula del profesor: "))
                    # Verificar si ya existe
                    if any(p.cedula == cedula for p in self.profesor):
                        print("Ya existe un profesor con esta cédula.")
                        continue
                        
                    nombre = input("Ingrese el nombre: ").strip()
                    apellido = input("Ingrese el apellido: ").strip()
                    email = input("Ingrese el email: ").strip()
                    max_carga = int(input("Ingrese la carga máxima de materias (ej. 3): "))
                    
                    nuevo_profesor = Docente(
                        cedula=cedula,
                        email=email,
                        apellido=apellido,
                        nombre=nombre,
                        max_carga=max_carga,
                        materias=[]
                    )
                    self.profesor.append(nuevo_profesor)
                    print(f"Profesor {nombre} {apellido} agregado exitosamente.")
                    mod_mat = input("¿Desea asignarle materias ahora? (s/n): ").strip().lower()
                    if mod_mat == 's':
                        print("Por favor, utilice la opción 5 del menú de profesores para modificar sus materias.")
                except ValueError:
                    print("Error: Entrada inválida. Asegúrese de ingresar números para cédula y carga máxima.")
            elif menu_profesores == 4:
                try:
                    cedula = int(input("\nIngrese la cédula del profesor a eliminar: "))
                    profesor_a_eliminar = next((p for p in self.profesor if p.cedula == cedula), None)
                    
                    if profesor_a_eliminar:
                        print(f"Profesor encontrado: {profesor_a_eliminar.nombre} {profesor_a_eliminar.apellido}")
                        confirmacion = input("¿Está seguro que desea eliminar este profesor? (s/n): ").strip().lower()
                        if confirmacion == 's':
                            self.profesor.remove(profesor_a_eliminar)
                            print("Profesor eliminado exitosamente.")
                        else:
                            print("Operación cancelada.")
                    else:
                        print("No se encontró ningún profesor con esa cédula.")
                except ValueError:
                    print("Error: La cédula debe ser un valor numérico.")
            elif menu_profesores == 5:
                self.modificar_lista_materias()

    def modificar_lista_materias(self):
        try:
            x = int(input("Ingrese la CI del profesor: "))
        except ValueError:
            print("CI inválida.")
            return
            
        tmp = None
        for i in self.profesor:
            if x == i.cedula:
                tmp = i
                break
                
        if not tmp:
            print("Profesor no encontrado.")
            return
            
        while True:
            z = input("¿Qué desea hacer? (1. Agregar materia, 2. Quitar materia, 0. Regresar): ")
            if z == "0":
                break
            elif z == "1":
                y = input("Ingrese el código de la materia a agregar: ").strip().upper()
                materia_obj = next((m for m in self.materia if m.codigo == y), None)
                if materia_obj:
                    if materia_obj not in tmp.materias:
                        tmp.materias.append(materia_obj)
                        print(f"Materia {materia_obj.nombre} agregada al profesor.")
                    else:
                        print("El profesor ya tiene asignada esta materia.")
                else:
                    print("Materia no encontrada en el sistema.")
            elif z == "2":
                y = input("Ingrese el código de la materia a quitar: ").strip().upper()
                materia_obj = next((m for m in tmp.materias if m.codigo == y), None)
                if materia_obj:
                    tmp.materias.remove(materia_obj)
                    print(f"Materia {materia_obj.nombre} removida del profesor.")
                else:
                    print("El profesor no tiene asignada esa materia.")

    def menu_materia(self):
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
                termino = input("\nIngrese el código o nombre de la materia a buscar: ").strip().lower()
                encontradas = []
                for m in self.materia:
                    if termino in m.codigo.lower() or termino in m.nombre.lower():
                        encontradas.append(m)
                
                if encontradas:
                    print("\n--- Resultados de la búsqueda ---")
                    for m in encontradas:
                        print(m.datos_materia())
                        print("-" * 33)
                else:
                    print("\nNo se encontró ninguna materia que coincida con la búsqueda.")
            elif menu_materias == 3:
                target = input("Qué materia desea buscar (nombre o fragmento): ").strip().lower()
                for item in self.materia:
                    if target in item.nombre.lower():
                        print(f"\nProfesores para {item.nombre}:")
                        for i in self.profesor:
                            if item in i.materias:
                                print(" - " + i.datos_profesor())
            elif menu_materias == 4:
                print("\n--- Agregar/Eliminar materia ---")
                opcion = input("1. Agregar materia\n2. Eliminar materia\nSeleccione una opción: ").strip()
                if opcion == "1":
                    codigo = input("Ingrese el código de la nueva materia: ").strip().upper()
                    if any(m.codigo == codigo for m in self.materia):
                        print("Ya existe una materia con ese código.")
                    else:
                        nombre = input("Ingrese el nombre de la materia: ").strip()
                        try:
                            secciones = int(input("Ingrese la cantidad de secciones: "))
                            nueva_materia = Materia(codigo=codigo, nombre=nombre, secciones=secciones)
                            self.materia.append(nueva_materia)
                            print(f"Materia {nombre} agregada exitosamente.")
                        except ValueError:
                            print("Error: La cantidad de secciones debe ser un número entero.")
                elif opcion == "2":
                    codigo = input("Ingrese el código de la materia a eliminar: ").strip().upper()
                    materia_eliminar = next((m for m in self.materia if m.codigo == codigo), None)
                    if materia_eliminar:
                        confirmacion = input(f"¿Está seguro que desea eliminar la materia {materia_eliminar.nombre}? (s/n): ").strip().lower()
                        if confirmacion == 's':
                            self.materia.remove(materia_eliminar)
                            for p in self.profesor:
                                if materia_eliminar in p.materias:
                                    p.materias.remove(materia_eliminar)
                            print("Materia eliminada exitosamente.")
                        else:
                            print("Operación cancelada.")
                    else:
                        print("No se encontró ninguna materia con ese código.")
                else:
                    print("Opción inválida.")
            elif menu_materias == 5:
                codigo = input("\nIngrese el código de la materia a modificar: ").strip().upper()
                materia_modificar = next((m for m in self.materia if m.codigo == codigo), None)
                
                if materia_modificar:
                    print(f"Materia encontrada: {materia_modificar.nombre} - Secciones actuales: {materia_modificar.secciones}")
                    try:
                        nuevas_secciones = int(input("Ingrese la nueva cantidad de secciones: "))
                        if nuevas_secciones > 0:
                            materia_modificar.secciones = nuevas_secciones
                            print("Cantidad de secciones actualizada exitosamente.")
                        else:
                            print("Error: La cantidad de secciones debe ser mayor a cero.")
                    except ValueError:
                        print("Error: Debe ingresar un número entero válido.")
                else:
                    print("No se encontró ninguna materia con ese código.")
    
    def modificacion(self):
        if not hasattr(self, 'bloques_horarios') or not self.bloques_horarios:
            print("\nNo se ha generado ningún horario todavía.")
            return

        while True:
            # 1. Seleccionar materia
            codigo_materia = input("\nIngrese el código o nombre de la materia (o '0' para salir): ").strip().lower()
            if codigo_materia == '0' or codigo_materia == "":
                break
                
            clases_materia = []
            for idx_b, b in enumerate(self.bloques_horarios):
                for idx_a, a in enumerate(b["asignaciones"]):
                    if codigo_materia in a["materia"].codigo.lower() or codigo_materia in a["materia"].nombre.lower():
                        clases_materia.append({"b_idx": idx_b, "a_idx": idx_a, "bloque": b, "asig": a})
                        
            if not clases_materia:
                print("No se encontró esa materia en el horario actual.")
                continue

            # 2. Seleccionar sección
            print("\n--- Secciones encontradas ---")
            for i, clase in enumerate(clases_materia):
                a = clase["asig"]
                b = clase["bloque"]
                print(f"{i + 1}. Sec {a['seccion']} - {b['dia']} {b['hora']} - Prof: {a['docente'].nombre} {a['docente'].apellido}")
                
            try:
                opc_sec = int(input("\nSeleccione la sección a modificar (0 para cancelar): "))
                if opc_sec <= 0 or opc_sec > len(clases_materia):
                    continue
                    
                clase_elegida = clases_materia[opc_sec - 1]
                b_actual = clase_elegida["bloque"]
                a_actual = clase_elegida["asig"]
                
                # 3. Seleccionar acción
                print("\n1. Cambiar el profesor de esta sección")
                print("2. Cambiar el horario de esta sección")
                opc_mod = input("Seleccione una opción: ").strip()
                
                if opc_mod == "1":
                    # a. Cambiar el profesor
                    print(f"\nProfesores disponibles para {a_actual['materia'].nombre} en el horario {b_actual['dia']} {b_actual['hora']}:")
                    
                    carga_actual = {p.cedula: 0 for p in self.profesor}
                    for b_iter in self.bloques_horarios:
                        for a_iter in b_iter["asignaciones"]:
                            carga_actual[a_iter["docente"].cedula] += 1
                            
                    profesores_disp = []
                    carga_efectiva = carga_actual.copy()
                    carga_efectiva[a_actual["docente"].cedula] -= 1 # Libera la clase para el profesor actual
                    
                    for p in self.profesor:
                        if a_actual["materia"] in p.materias and carga_efectiva[p.cedula] < p.max_carga:
                            ocupado_ahora = any(a_iter["docente"].cedula == p.cedula for a_iter in b_actual["asignaciones"] if a_iter != a_actual)
                            if not ocupado_ahora:
                                profesores_disp.append(p)
                                
                    if not profesores_disp:
                        print("No hay profesores disponibles.")
                    else:
                        for i_p, p in enumerate(profesores_disp):
                            print(f"{i_p + 1}. {p.nombre} {p.apellido}")
                        
                        opc_p = int(input("\nSeleccione el nuevo profesor (0 para cancelar): "))
                        if 0 < opc_p <= len(profesores_disp):
                            p_nuevo = profesores_disp[opc_p - 1]
                            a_actual["docente"] = p_nuevo
                            print("Profesor cambiado exitosamente.")
                            self.menu_horario()
                            return
                            
                elif opc_mod == "2":
                    # b. Cambiar horario
                    print("\nHoras con salones disponibles:")
                    bloques_disp = []
                    for b_iter in self.bloques_horarios:
                        if b_iter["salones_disp"] > 0 and b_iter != b_actual:
                            bloques_disp.append(b_iter)
                            
                    for i_b, b_iter in enumerate(bloques_disp):
                        print(f"{i_b + 1}. {b_iter['dia']} {b_iter['hora']} (Salones libres: {b_iter['salones_disp']})")
                        
                    carga_actual = {p.cedula: 0 for p in self.profesor}
                    for b_tmp in self.bloques_horarios:
                        for a_tmp in b_tmp["asignaciones"]:
                            carga_actual[a_tmp["docente"].cedula] += 1
                            
                    print("\nProfesores disponibles para esta materia:")
                    profesores_gral = []
                    carga_efectiva = carga_actual.copy()
                    carga_efectiva[a_actual["docente"].cedula] -= 1
                    for p in self.profesor:
                        if a_actual["materia"] in p.materias and carga_efectiva[p.cedula] < p.max_carga:
                            profesores_gral.append(p)
                            print(f"- {p.nombre} {p.apellido}")
                            
                    opc_h = int(input("\nSeleccione el nuevo bloque horario (0 para cancelar): "))
                    if 0 < opc_h <= len(bloques_disp):
                        b_nuevo = bloques_disp[opc_h - 1]
                        
                        print("\nSeleccione el profesor para este nuevo horario:")
                        profesores_validos = []
                        for p in profesores_gral:
                            ocupado_en_b_nuevo = any(a_tmp["docente"].cedula == p.cedula for a_tmp in b_nuevo["asignaciones"])
                            if not ocupado_en_b_nuevo:
                                profesores_validos.append(p)
                                
                        if not profesores_validos:
                            print("Ninguno de los profesores está libre en ese horario.")
                        else:
                            for i_p, p in enumerate(profesores_validos):
                                print(f"{i_p + 1}. {p.nombre} {p.apellido}")
                            opc_p = int(input("Seleccione el profesor (0 para cancelar): "))
                            if 0 < opc_p <= len(profesores_validos):
                                p_nuevo = profesores_validos[opc_p - 1]
                                
                                # Aplicar cambios:
                                b_actual["asignaciones"].pop(clase_elegida["a_idx"])
                                b_actual["salones_disp"] += 1
                                
                                a_actual["docente"] = p_nuevo
                                b_nuevo["asignaciones"].append(a_actual)
                                b_nuevo["salones_disp"] -= 1
                                
                                print("Horario modificado exitosamente.")
                                self.menu_horario()
                                return
                                
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Entrada inválida.")
    def crear_horario(self):
        try:
            salones_str = input("Ingrese el número de salones disponibles (presione Enter para 30 por defecto): ")
            salones = int(salones_str) if salones_str.strip() else 30
        except ValueError:
            print("Valor inválido. Se usarán 30 salones por defecto.")
            salones = 30
            
        print(f"\nGenerando horario con {salones} salones...")
        
        # 1. Asignar profesores a las secciones de las materias
        profesor_carga = {p.cedula: 0 for p in self.profesor}
        asignaciones = [] # lista de dicts
        materias_cerradas = [] # faltan profesores
        
        for mat in self.materia:
            secciones_cerradas_count = 0
            for sec in range(1, mat.secciones + 1):
                asignado = False
                
                # Buscar profesor disponible (directamente)
                for prof in self.profesor:
                    if mat in prof.materias and profesor_carga[prof.cedula] < prof.max_carga:
                        asignaciones.append({"materia": mat, "seccion": sec, "docente": prof})
                        profesor_carga[prof.cedula] += 1
                        asignado = True
                        break
                
                if asignado:
                    continue
                    
                # Si no, buscar reasignación
                reasignado = False
                for prof in self.profesor:
                    if mat in prof.materias and profesor_carga[prof.cedula] >= prof.max_carga:
                        # Buscar si alguna materia que tiene asignada este prof puede ser reasignada
                        # Buscamos en las asignaciones actuales de este profesor
                        for i, asig in enumerate(asignaciones):
                            if asig["docente"].cedula == prof.cedula:
                                materia_actual = asig["materia"]
                                
                                # Buscar otro profesor que pueda dar materia_actual y tenga disponibilidad
                                flag_encontrado_otro = False
                                for otro_prof in self.profesor:
                                    if otro_prof.cedula != prof.cedula and materia_actual in otro_prof.materias and profesor_carga[otro_prof.cedula] < otro_prof.max_carga:
                                        # Reasignamos
                                        asignaciones[i]["docente"] = otro_prof
                                        profesor_carga[otro_prof.cedula] += 1
                                        profesor_carga[prof.cedula] -= 1
                                        flag_encontrado_otro = True
                                        break
                                
                                if flag_encontrado_otro:
                                    # Ahora el prof original tiene disponibilidad
                                    asignaciones.append({"materia": mat, "seccion": sec, "docente": prof})
                                    profesor_carga[prof.cedula] += 1
                                    reasignado = True
                                    break
                    if reasignado:
                        break
                        
                if not reasignado:
                    secciones_cerradas_count += 1
                    
            if secciones_cerradas_count > 0:
                materias_cerradas.append({"materia": mat, "cantidad": secciones_cerradas_count})
                
        # 2. Asignar secciones a bloques horarios
        dias = ["Lunes y Miércoles", "Martes y Jueves"]
        horas = [
            "7:00 – 8:30", "8:45 – 10:15", "10:30 – 12:00",
            "12:15 – 1:45", "2:00 – 3:30", "3:45 – 5:15", "5:30 – 7:00"
        ]
        
        self.bloques_horarios = []
        for d in dias:
            for h in horas:
                self.bloques_horarios.append({
                    "dia": d,
                    "hora": h,
                    "asignaciones": [],
                    "salones_disp": salones
                })
                
        materias_sin_salon = {} # codigo -> count
        
        for asig in asignaciones:
            ubicado = False
            for b in self.bloques_horarios:
                if b["salones_disp"] > 0:
                    docente_ocupado = any(a["docente"].cedula == asig["docente"].cedula for a in b["asignaciones"])
                    materia_repetida = any(a["materia"].codigo == asig["materia"].codigo for a in b["asignaciones"])
                    
                    if not docente_ocupado and not materia_repetida:
                        b["asignaciones"].append(asig)
                        b["salones_disp"] -= 1
                        ubicado = True
                        break
            
            if not ubicado:
                for b in self.bloques_horarios:
                    if b["salones_disp"] > 0:
                        docente_ocupado = any(a["docente"].cedula == asig["docente"].cedula for a in b["asignaciones"])
                        if not docente_ocupado:
                            b["asignaciones"].append(asig)
                            b["salones_disp"] -= 1
                            ubicado = True
                            break
                            
            if not ubicado:
                c = asig["materia"].codigo
                if c not in materias_sin_salon:
                    materias_sin_salon[c] = {"materia": asig["materia"], "cantidad": 0}
                materias_sin_salon[c]["cantidad"] += 1
                
        # Reporte Final
        print("\n--- REPORTE DE HORARIOS ---")
        if materias_cerradas:
            print("\n1. Materias con secciones cerradas por falta de profesores:")
            for mc in materias_cerradas:
                print(f"   - {mc['materia'].nombre} ({mc['materia'].codigo}): {mc['cantidad']} sección(es) cerrada(s).")
        else:
            print("\n1. No hubo secciones cerradas por falta de profesores.")
            
        if materias_sin_salon:
            print("\n2. Materias con secciones no asignadas por falta de salones:")
            for ms in materias_sin_salon.values():
                print(f"   - {ms['materia'].nombre} ({ms['materia'].codigo}): {ms['cantidad']} sección(es) sin asignar.")
        else:
            print("\n2. No hubo secciones sin asignar por falta de salones.")
            
        print("\n3. Bloques horarios y salones disponibles:")
        for idx, b in enumerate(self.bloques_horarios):
            print(f"   [{idx}] {b['dia']} {b['hora']} - Salones disp: {b['salones_disp']}")
            
        self.menu_horario()

    def menu_horario(self):
        while True:
            print("""
--- SUBMENÚ HORARIOS ---
1. Ver el horario de una materia
2. Ver el horario de un profesor
3. Ver salones asignados a una hora
4. Guardar asignación de horarios en CSV
5. Modificar asignación de horarios
0. Volver al menú principal
""")
            try:
                opc = int(input("Seleccione una opción: "))
            except ValueError:
                continue
                
            if opc == 0:
                break
            elif opc == 1:
                target = input("Ingrese el código o nombre de la materia: ").strip().lower()
                encontrado = False
                for b in self.bloques_horarios:
                    for a in b["asignaciones"]:
                        if target in a["materia"].codigo.lower() or target in a["materia"].nombre.lower():
                            print(f"{b['dia']} {b['hora']} - Sec {a['seccion']} - Prof: {a['docente'].nombre} {a['docente'].apellido}")
                            encontrado = True
                if not encontrado:
                    print("No se encontraron horarios para esa materia.")
            elif opc == 2:
                target = input("Ingrese la cédula, nombre o apellido del profesor: ").strip().lower()
                encontrado = False
                for b in self.bloques_horarios:
                    for a in b["asignaciones"]:
                        d = a["docente"]
                        if target in str(d.cedula) or target in d.nombre.lower() or target in d.apellido.lower():
                            print(f"{b['dia']} {b['hora']} - {a['materia'].nombre} (Sec {a['seccion']})")
                            encontrado = True
                if not encontrado:
                    print("No se encontraron horarios para ese profesor.")
            elif opc == 3:
                try:
                    idx = int(input("Ingrese el índice numérico del bloque horario (ver listado arriba): "))
                    if 0 <= idx < len(self.bloques_horarios):
                        b = self.bloques_horarios[idx]
                        print(f"\nHorarios para {b['dia']} {b['hora']}:")
                        if not b["asignaciones"]:
                            print("No hay clases asignadas a esta hora.")
                        else:
                            for a in b["asignaciones"]:
                                print(f" - {a['materia'].nombre} (Sec {a['seccion']}) - Prof: {a['docente'].nombre} {a['docente'].apellido}")
                    else:
                        print("Índice fuera de rango.")
                except ValueError:
                    print("Índice numérico inválido.")
            elif opc == 4:
                try:
                    import csv
                    with open("horarios.csv", "w", encoding="utf-8", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(["Día", "Hora", "Código Materia", "Materia", "Sección", "Cédula Prof", "Profesor"])
                        for b in self.bloques_horarios:
                            for a in b["asignaciones"]:
                                writer.writerow([
                                    b["dia"], b["hora"],
                                    a["materia"].codigo, a["materia"].nombre, a["seccion"],
                                    a["docente"].cedula, f"{a['docente'].nombre} {a['docente'].apellido}"
                                ])
                    print("Horario guardado exitosamente en 'horarios.csv'.")
                except Exception as e:
                    print(f"Error al guardar CSV: {e}")
            elif opc == 5:
                print("\n--- Modificar asignación ---")
                try:
                    idx_origen = int(input("Índice del bloque horario de origen: "))
                    if not (0 <= idx_origen < len(self.bloques_horarios)):
                        print("Índice de bloque origen inválido.")
                        continue
                        
                    b_origen = self.bloques_horarios[idx_origen]
                    if not b_origen["asignaciones"]:
                        print("No hay clases en este bloque horario.")
                        continue
                        
                    for idx, a in enumerate(b_origen["asignaciones"]):
                        print(f"[{idx}] {a['materia'].nombre} (Sec {a['seccion']}) - Prof: {a['docente'].nombre} {a['docente'].apellido}")
                        
                    idx_asig = int(input("Índice de la clase a mover: "))
                    if not (0 <= idx_asig < len(b_origen["asignaciones"])):
                        print("Índice de clase inválido.")
                        continue
                        
                    clase_mov = b_origen["asignaciones"][idx_asig]
                    
                    idx_dest = int(input("Índice del bloque horario de destino: "))
                    if not (0 <= idx_dest < len(self.bloques_horarios)):
                        print("Índice de bloque destino inválido.")
                        continue
                        
                    b_dest = self.bloques_horarios[idx_dest]
                    if b_dest["salones_disp"] <= 0:
                        print("El bloque destino no tiene salones disponibles.")
                        continue
                        
                    docente_ocupado = any(a["docente"].cedula == clase_mov["docente"].cedula for a in b_dest["asignaciones"])
                    if docente_ocupado:
                        print("Error: El profesor ya está ocupado en el bloque destino.")
                        continue
                        
                    b_origen["asignaciones"].pop(idx_asig)
                    b_origen["salones_disp"] += 1
                    b_dest["asignaciones"].append(clase_mov)
                    b_dest["salones_disp"] -= 1
                    print("Clase movida exitosamente.")
                except ValueError:
                    print("Entrada inválida. Debe ser un número.")
