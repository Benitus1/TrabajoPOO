import os
from DTO.empleado_dto import EmpleadoDTO
from DTO.proyecto_dto import ProyectoDTO
from DTO.registro_tiempo_dto import RegistroTiempoDTO
from DAO.empleado_dao import EmpleadoDAO
from DAO.proyecto_dao import ProyectoDAO
from DAO.registro_tiempo_dao import RegistroTiempoDAO

empleado_dao = EmpleadoDAO()
proyecto_dao = ProyectoDAO()
registro_dao = RegistroTiempoDAO()

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pausa():
    input("\npresione enter para continuar")

def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("ingrese un numero entero valido")

def leer_float(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("ingrese un numero valido")

def agregar_empleado():
    print("\n--- agregar empleado ---")
    nombre = input("nombre: ").strip()
    email = input("email: ").strip()
    telefono = input("telefono: ").strip()
    salario = leer_float("salario: ")
    rol = input("rol [Empleado]: ").strip() or "Empleado"
    
    dto = EmpleadoDTO(nombre, email, telefono, salario, rol)
    try:
        nuevo = empleado_dao.guardar(dto)
        print("guardado")
        print(nuevo.mostrar_datos())
    except Exception as e:
        print(f"error al guardar: {e}")

def listar_empleados():
    print("\n--- empleados ---")
    lista = empleado_dao.listar()
    if not lista:
        print("no hay registros")
    else:
        for emp in lista:
            print(emp.mostrar_datos())

def buscar_empleado():
    print("\n--- buscar empleado ---")
    id_emp = leer_entero("id: ")
    emp = empleado_dao.buscar_por_id(id_emp)
    if emp:
        print(emp.mostrar_datos())
    else:
        print("no existe")

def actualizar_empleado():
    print("\n--- editar empleado ---")
    id_emp = leer_entero("id a editar: ")
    emp = empleado_dao.buscar_por_id(id_emp)
    if not emp:
        print("no existe")
        return

    print(f"actual: {emp.mostrar_datos()}")
    nom = input(f"nombre [{emp.nombre}]: ").strip()
    if nom: emp.nombre = nom
    em = input(f"email [{emp.email}]: ").strip()
    if em: emp.email = em
    tel = input(f"telefono [{emp.telefono}]: ").strip()
    if tel: emp.telefono = tel
    sal_str = input(f"salario [{emp.salario}]: ").strip()
    if sal_str:
        try: emp.salario = float(sal_str)
        except ValueError: pass
    rol = input(f"rol [{emp.rol}]: ").strip()
    if rol: emp.rol = rol

    if empleado_dao.actualizar(emp):
        print("actualizado")
    else:
        print("sin cambios")

def eliminar_empleado():
    print("\n--- borrar empleado ---")
    id_emp = leer_entero("id a borrar: ")
    emp = empleado_dao.buscar_por_id(id_emp)
    if not emp:
        print("no existe")
        return

    print(f"seleccionado: {emp.mostrar_datos()}")
    confirm = input("confirmar borrado (s/n): ").strip().lower()
    if confirm == 's':
        try:
            if empleado_dao.eliminar(id_emp):
                print("borrado")
            else:
                print("no se pudo borrar")
        except Exception as e:
            print(f"error: tiene horas asociadas ({e})")

def agregar_proyecto():
    print("\n--- agregar proyecto ---")
    nombre = input("nombre: ").strip()
    descripcion = input("descripcion: ").strip()
    fecha_inicio = input("fecha inicio (YYYY-MM-DD): ").strip()
    
    dto = ProyectoDTO(nombre, descripcion, fecha_inicio)
    try:
        nuevo = proyecto_dao.guardar(dto)
        print("guardado")
        print(nuevo.mostrar_datos())
    except Exception as e:
        print(f"error al guardar: {e}")

def listar_proyectos():
    print("\n--- proyectos ---")
    lista = proyecto_dao.listar()
    if not lista:
        print("no hay registros")
    else:
        for p in lista:
            print(p.mostrar_datos())

def buscar_proyecto():
    print("\n--- buscar proyecto ---")
    id_proy = leer_entero("id: ")
    proy = proyecto_dao.buscar_por_id(id_proy)
    if proy:
        print(proy.mostrar_datos())
    else:
        print("no existe")

def actualizar_proyecto():
    print("\n--- editar proyecto ---")
    id_proy = leer_entero("id a editar: ")
    proy = proyecto_dao.buscar_por_id(id_proy)
    if not proy:
        print("no existe")
        return

    print(f"actual: {proy.mostrar_datos()}")
    nom = input(f"nombre [{proy.nombre}]: ").strip()
    if nom: proy.nombre = nom
    desc = input(f"descripcion [{proy.descripcion}]: ").strip()
    if desc: proy.descripcion = desc
    fec = input(f"fecha inicio [{proy.fecha_inicio}]: ").strip()
    if fec: proy.fecha_inicio = fec

    if proyecto_dao.actualizar(proy):
        print("actualizado")
    else:
        print("sin cambios")

def eliminar_proyecto():
    print("\n--- borrar proyecto ---")
    id_proy = leer_entero("id a borrar: ")
    proy = proyecto_dao.buscar_por_id(id_proy)
    if not proy:
        print("no existe")
        return

    print(f"seleccionado: {proy.mostrar_datos()}")
    confirm = input("confirmar borrado (s/n): ").strip().lower()
    if confirm == 's':
        try:
            if proyecto_dao.eliminar(id_proy):
                print("borrado")
            else:
                print("no se pudo borrar")
        except Exception as e:
            print(f"error: tiene horas asociadas ({e})")

def agregar_registro_tiempo():
    print("\n--- registrar horas ---")
    print("\nempleados:")
    listar_empleados()
    id_emp = leer_entero("\nid empleado: ")
    if not empleado_dao.buscar_por_id(id_emp):
        print("empleado no existe")
        return

    print("\nproyectos:")
    listar_proyectos()
    id_proy = leer_entero("\nid proyecto: ")
    if not proyecto_dao.buscar_por_id(id_proy):
        print("proyecto no existe")
        return

    horas = leer_float("horas: ")
    tarea = input("tarea: ").strip()
    fecha = input("fecha (YYYY-MM-DD): ").strip()

    dto = RegistroTiempoDTO(horas, tarea, fecha, id_emp, id_proy)
    try:
        nuevo = registro_dao.guardar(dto)
        print("guardado")
        print(nuevo.mostrar_resumen())
    except Exception as e:
        print(f"error al guardar: {e}")

def listar_registros_tiempo():
    print("\n--- horas registradas ---")
    lista = registro_dao.listar()
    if not lista:
        print("no hay registros")
    else:
        for r in lista:
            print(r.mostrar_resumen())

def buscar_registro_tiempo():
    print("\n--- buscar registro ---")
    id_reg = leer_entero("id registro: ")
    reg = registro_dao.buscar_por_id(id_reg)
    if reg:
        print(reg.mostrar_resumen())
    else:
        print("no existe")

def actualizar_registro_tiempo():
    print("\n--- editar registro ---")
    id_reg = leer_entero("id registro a editar: ")
    reg = registro_dao.buscar_por_id(id_reg)
    if not reg:
        print("no existe")
        return

    print(f"actual: {reg.mostrar_resumen()}")
    h_str = input(f"horas [{reg.horas}]: ").strip()
    if h_str:
        try: reg.horas = float(h_str)
        except ValueError: pass
    tar = input(f"tarea [{reg.descripcion_tarea}]: ").strip()
    if tar: reg.descripcion_tarea = tar
    fec = input(f"fecha [{reg.fecha}]: ").strip()
    if fec: reg.fecha = fec

    if registro_dao.actualizar(reg):
        print("actualizado")
    else:
        print("sin cambios")

def eliminar_registro_tiempo():
    print("\n--- borrar registro ---")
    id_reg = leer_entero("id registro a borrar: ")
    reg = registro_dao.buscar_por_id(id_reg)
    if not reg:
        print("no existe")
        return

    print(f"seleccionado: {reg.mostrar_resumen()}")
    confirm = input("confirmar borrado (s/n): ").strip().lower()
    if confirm == 's':
        if registro_dao.eliminar(id_reg):
            print("borrado")
        else:
            print("no se pudo borrar")

def submenu_empleados():
    while True:
        limpiar_pantalla()
        print("--- empleados ---")
        print("1. agregar")
        print("2. listar")
        print("3. buscar")
        print("4. editar")
        print("5. borrar")
        print("6. volver")
        op = input("\nopcion: ").strip()
        if op == "1": agregar_empleado(); pausa()
        elif op == "2": listar_empleados(); pausa()
        elif op == "3": buscar_empleado(); pausa()
        elif op == "4": actualizar_empleado(); pausa()
        elif op == "5": eliminar_empleado(); pausa()
        elif op == "6": break
        else: print("opcion no valida"); pausa()

def submenu_proyectos():
    while True:
        limpiar_pantalla()
        print("--- proyectos ---")
        print("1. agregar")
        print("2. listar")
        print("3. buscar")
        print("4. editar")
        print("5. borrar")
        print("6. volver")
        op = input("\nopcion: ").strip()
        if op == "1": agregar_proyecto(); pausa()
        elif op == "2": listar_proyectos(); pausa()
        elif op == "3": buscar_proyecto(); pausa()
        elif op == "4": actualizar_proyecto(); pausa()
        elif op == "5": eliminar_proyecto(); pausa()
        elif op == "6": break
        else: print("opcion no valida"); pausa()

def submenu_registros():
    while True:
        limpiar_pantalla()
        print("--- registro de tiempo ---")
        print("1. registrar horas")
        print("2. listar horas")
        print("3. buscar")
        print("4. editar")
        print("5. borrar")
        print("6. volver")
        op = input("\nopcion: ").strip()
        if op == "1": agregar_registro_tiempo(); pausa()
        elif op == "2": listar_registros_tiempo(); pausa()
        elif op == "3": buscar_registro_tiempo(); pausa()
        elif op == "4": actualizar_registro_tiempo(); pausa()
        elif op == "5": eliminar_registro_tiempo(); pausa()
        elif op == "6": break
        else: print("opcion no valida"); pausa()

def menu_principal():
    while True:
        limpiar_pantalla()
        print("--- ecotech solutions ---")
        print("1. empleados")
        print("2. proyectos")
        print("3. registro de tiempo")
        print("4. salir")
        op = input("\nopcion: ").strip()
        if op == "1": submenu_empleados()
        elif op == "2": submenu_proyectos()
        elif op == "3": submenu_registros()
        elif op == "4":
            print("saliendo del sistema")
            break
        else: print("opcion no valida"); pausa()

if __name__ == "__main__":
    menu_principal()
