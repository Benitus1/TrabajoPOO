import os
from DTO.empleado_dto import EmpleadoDTO
from DTO.proyecto_dto import ProyectoDTO
from DTO.registro_tiempo_dto import RegistroTiempoDTO
from DAO.empleado_dao import EmpleadoDAO
from DAO.proyecto_dao import ProyectoDAO
from DAO.registro_tiempo_dao import RegistroTiempoDAO

# Instancias de acceso a datos
empleado_dao = EmpleadoDAO()
proyecto_dao = ProyectoDAO()
registro_dao = RegistroTiempoDAO()

# --- HELPER CONSOLA ---

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pausa():
    input("\nPresione ENTER para continuar...")

def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número entero válido.")

def leer_float(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingrese un valor numérico válido.")

# --- CRUD EMPLEADOS ---

def agregar_empleado():
    print("\n--- REGISTRAR EMPLEADO ---")
    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()
    salario = leer_float("Salario: ")
    rol = input("Rol [Empleado]: ").strip() or "Empleado"
    
    dto = EmpleadoDTO(nombre, email, telefono, salario, rol)
    try:
        nuevo = empleado_dao.guardar(dto)
        print("\n¡Empleado registrado!")
        print(nuevo.mostrar_datos())
    except Exception as e:
        print(f"Error al registrar: {e}")

def listar_empleados():
    print("\n--- LISTA DE EMPLEADOS ---")
    lista = empleado_dao.listar()
    if not lista:
        print("No hay empleados registrados.")
    else:
        for emp in lista:
            print(emp.mostrar_datos())

def buscar_empleado():
    print("\n--- BUSCAR EMPLEADO POR ID ---")
    id_emp = leer_entero("Ingrese ID: ")
    emp = empleado_dao.buscar_por_id(id_emp)
    if emp:
        print(emp.mostrar_datos())
    else:
        print("Empleado no encontrado.")

def actualizar_empleado():
    print("\n--- ACTUALIZAR EMPLEADO ---")
    id_emp = leer_entero("Ingrese ID a modificar: ")
    emp = empleado_dao.buscar_por_id(id_emp)
    if not emp:
        print("Empleado no encontrado.")
        return

    print(f"Datos actuales: {emp.mostrar_datos()}")
    nom = input(f"Nuevo nombre [{emp.nombre}]: ").strip()
    if nom: emp.nombre = nom
    em = input(f"Nuevo email [{emp.email}]: ").strip()
    if em: emp.email = em
    tel = input(f"Nuevo teléfono [{emp.telefono}]: ").strip()
    if tel: emp.telefono = tel
    sal_str = input(f"Nuevo salario [{emp.salario}]: ").strip()
    if sal_str:
        try: emp.salario = float(sal_str)
        except ValueError: pass
    rol = input(f"Nuevo rol [{emp.rol}]: ").strip()
    if rol: emp.rol = rol

    if empleado_dao.actualizar(emp):
        print("Empleado actualizado correctamente.")
    else:
        print("No se realizaron cambios.")

def eliminar_empleado():
    print("\n--- ELIMINAR EMPLEADO ---")
    id_emp = leer_entero("Ingrese ID a eliminar: ")
    emp = empleado_dao.buscar_por_id(id_emp)
    if not emp:
        print("Empleado no encontrado.")
        return

    print(f"Seleccionado: {emp.mostrar_datos()}")
    confirm = input("¿Confirmar eliminación? (s/n): ").strip().lower()
    if confirm == 's':
        try:
            if empleado_dao.eliminar(id_emp):
                print("Empleado eliminado.")
            else:
                print("No se pudo eliminar.")
        except Exception as e:
            print(f"Error: No se puede eliminar por dependencia con registros de horas ({e}).")

# --- CRUD PROYECTOS ---

def agregar_proyecto():
    print("\n--- REGISTRAR PROYECTO ---")
    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()
    fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ").strip()
    
    dto = ProyectoDTO(nombre, descripcion, fecha_inicio)
    try:
        nuevo = proyecto_dao.guardar(dto)
        print("\n¡Proyecto registrado!")
        print(nuevo.mostrar_datos())
    except Exception as e:
        print(f"Error al registrar: {e}")

def listar_proyectos():
    print("\n--- LISTA DE PROYECTOS ---")
    lista = proyecto_dao.listar()
    if not lista:
        print("No hay proyectos registrados.")
    else:
        for p in lista:
            print(p.mostrar_datos())

def buscar_proyecto():
    print("\n--- BUSCAR PROYECTO POR ID ---")
    id_proy = leer_entero("Ingrese ID: ")
    proy = proyecto_dao.buscar_por_id(id_proy)
    if proy:
        print(proy.mostrar_datos())
    else:
        print("Proyecto no encontrado.")

def actualizar_proyecto():
    print("\n--- ACTUALIZAR PROYECTO ---")
    id_proy = leer_entero("Ingrese ID a modificar: ")
    proy = proyecto_dao.buscar_por_id(id_proy)
    if not proy:
        print("Proyecto no encontrado.")
        return

    print(f"Datos actuales: {proy.mostrar_datos()}")
    nom = input(f"Nuevo nombre [{proy.nombre}]: ").strip()
    if nom: proy.nombre = nom
    desc = input(f"Nueva descripción [{proy.descripcion}]: ").strip()
    if desc: proy.descripcion = desc
    fec = input(f"Nueva fecha inicio [{proy.fecha_inicio}]: ").strip()
    if fec: proy.fecha_inicio = fec

    if proyecto_dao.actualizar(proy):
        print("Proyecto actualizado correctamente.")
    else:
        print("No se realizaron cambios.")

def eliminar_proyecto():
    print("\n--- ELIMINAR PROYECTO ---")
    id_proy = leer_entero("Ingrese ID a eliminar: ")
    proy = proyecto_dao.buscar_por_id(id_proy)
    if not proy:
        print("Proyecto no encontrado.")
        return

    print(f"Seleccionado: {proy.mostrar_datos()}")
    confirm = input("¿Confirmar eliminación? (s/n): ").strip().lower()
    if confirm == 's':
        try:
            if proyecto_dao.eliminar(id_proy):
                print("Proyecto eliminado.")
            else:
                print("No se pudo eliminar.")
        except Exception as e:
            print(f"Error: No se puede eliminar por dependencia con registros de horas ({e}).")

# --- CRUD REGISTRO DE TIEMPO (TRANSACCIONAL) ---

def agregar_registro_tiempo():
    print("\n--- IMPUTAR HORAS A PROYECTO ---")
    print("\nEmpleados existentes:")
    listar_empleados()
    id_emp = leer_entero("\nID del empleado: ")
    if not empleado_dao.buscar_por_id(id_emp):
        print("El empleado seleccionado no existe.")
        return

    print("\nProyectos existentes:")
    listar_proyectos()
    id_proy = leer_entero("\nID del proyecto: ")
    if not proyecto_dao.buscar_por_id(id_proy):
        print("El proyecto seleccionado no existe.")
        return

    horas = leer_float("Horas dedicadas: ")
    tarea = input("Descripción de la tarea: ").strip()
    fecha = input("Fecha (YYYY-MM-DD): ").strip()

    dto = RegistroTiempoDTO(horas, tarea, fecha, id_emp, id_proy)
    try:
        nuevo = registro_dao.guardar(dto)
        print("\n¡Horas registradas exitosamente!")
        print(nuevo.mostrar_resumen())
    except Exception as e:
        print(f"Error al registrar: {e}")

def listar_registros_tiempo():
    print("\n--- BITÁCORA DE HORAS REGISTRADAS (INNER JOIN) ---")
    lista = registro_dao.listar()
    if not lista:
        print("No hay registros de tiempo.")
    else:
        for r in lista:
            print(r.mostrar_resumen())

def buscar_registro_tiempo():
    print("\n--- BUSCAR REGISTRO DE HORAS ---")
    id_reg = leer_entero("Ingrese N° Registro: ")
    reg = registro_dao.buscar_por_id(id_reg)
    if reg:
        print(reg.mostrar_resumen())
    else:
        print("Registro no encontrado.")

def actualizar_registro_tiempo():
    print("\n--- ACTUALIZAR REGISTRO DE HORAS ---")
    id_reg = leer_entero("Ingrese N° Registro a modificar: ")
    reg = registro_dao.buscar_por_id(id_reg)
    if not reg:
        print("Registro no encontrado.")
        return

    print(f"Datos actuales: {reg.mostrar_resumen()}")
    h_str = input(f"Nuevas horas [{reg.horas}]: ").strip()
    if h_str:
        try: reg.horas = float(h_str)
        except ValueError: pass
    tar = input(f"Nueva tarea [{reg.descripcion_tarea}]: ").strip()
    if tar: reg.descripcion_tarea = tar
    fec = input(f"Nueva fecha [{reg.fecha}]: ").strip()
    if fec: reg.fecha = fec

    if registro_dao.actualizar(reg):
        print("Registro actualizado correctamente.")
    else:
        print("No se realizaron cambios.")

def eliminar_registro_tiempo():
    print("\n--- ELIMINAR REGISTRO DE HORAS ---")
    id_reg = leer_entero("Ingrese N° Registro a eliminar: ")
    reg = registro_dao.buscar_por_id(id_reg)
    if not reg:
        print("Registro no encontrado.")
        return

    print(f"Seleccionado: {reg.mostrar_resumen()}")
    confirm = input("¿Confirmar eliminación? (s/n): ").strip().lower()
    if confirm == 's':
        if registro_dao.eliminar(id_reg):
            print("Registro eliminado exitosamente.")
        else:
            print("No se pudo eliminar.")

# --- MENU ---

def submenu_empleados():
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE EMPLEADOS ===")
        print("1. Agregar")
        print("2. Listar")
        print("3. Buscar por ID")
        print("4. Actualizar")
        print("5. Eliminar")
        print("6. Volver")
        op = input("\nOpción: ").strip()
        if op == "1": agregar_empleado(); pausa()
        elif op == "2": listar_empleados(); pausa()
        elif op == "3": buscar_empleado(); pausa()
        elif op == "4": actualizar_empleado(); pausa()
        elif op == "5": eliminar_empleado(); pausa()
        elif op == "6": break
        else: print("Opción inválida."); pausa()

def submenu_proyectos():
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE PROYECTOS ===")
        print("1. Agregar")
        print("2. Listar")
        print("3. Buscar por ID")
        print("4. Actualizar")
        print("5. Eliminar")
        print("6. Volver")
        op = input("\nOpción: ").strip()
        if op == "1": agregar_proyecto(); pausa()
        elif op == "2": listar_proyectos(); pausa()
        elif op == "3": buscar_proyecto(); pausa()
        elif op == "4": actualizar_proyecto(); pausa()
        elif op == "5": eliminar_proyecto(); pausa()
        elif op == "6": break
        else: print("Opción inválida."); pausa()

def submenu_registros():
    while True:
        limpiar_pantalla()
        print("=== REGISTRO DE TIEMPO ===")
        print("1. Imputar Horas")
        print("2. Listar Bitácora")
        print("3. Buscar por ID")
        print("4. Actualizar")
        print("5. Eliminar")
        print("6. Volver")
        op = input("\nOpción: ").strip()
        if op == "1": agregar_registro_tiempo(); pausa()
        elif op == "2": listar_registros_tiempo(); pausa()
        elif op == "3": buscar_registro_tiempo(); pausa()
        elif op == "4": actualizar_registro_tiempo(); pausa()
        elif op == "5": eliminar_registro_tiempo(); pausa()
        elif op == "6": break
        else: print("Opción inválida."); pausa()

def menu_principal():
    while True:
        limpiar_pantalla()
        print("==========================================")
        print("   SISTEMA DE GESTION ECOTECH SOLUTIONS   ")
        print("==========================================")
        print("1. Gestión de Empleados")
        print("2. Gestión de Proyectos")
        print("3. Registro de Tiempo")
        print("4. Salir")
        op = input("\nOpción: ").strip()
        if op == "1": submenu_empleados()
        elif op == "2": submenu_proyectos()
        elif op == "3": submenu_registros()
        elif op == "4":
            print("\nCerrando aplicación EcoTech Solutions...")
            break
        else: print("Opción inválida."); pausa()

if __name__ == "__main__":
    menu_principal()
