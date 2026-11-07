import os
import sys
from datetime import datetime
from DTO.empleado_dto import EmpleadoDTO
from DTO.proyecto_dto import ProyectoDTO
from DTO.registro_tiempo_dto import RegistroTiempoDTO
from DTO.departamento_dto import DepartamentoDTO
from DAO.empleado_dao import EmpleadoDAO
from DAO.proyecto_dao import ProyectoDAO
from DAO.registro_tiempo_dao import RegistroTiempoDAO
from DAO.departamento_dao import DepartamentoDAO
from DAO.proyecto_asignacion_dao import ProyectoAsignacionDAO
from DAO.usuario_dao import UsuarioDAO
from SEGURIDAD.autenticacion import AutenticacionService, hash_password, verificar_password
from SEGURIDAD.validaciones import (
    sanitizar_texto, validar_email, validar_telefono, validar_nombre,
    validar_salario, validar_fecha, validar_ciudad, validar_codigo_moneda,
    validar_no_vacio,
)
from SERVICIOS.clima_service import ClimaService
from SERVICIOS.indicadores_service import IndicadoresService

# Instancias de acceso a datos
empleado_dao = EmpleadoDAO()
proyecto_dao = ProyectoDAO()
registro_dao = RegistroTiempoDAO()
departamento_dao = DepartamentoDAO()
asignacion_dao = ProyectoAsignacionDAO()
usuario_dao = UsuarioDAO()
auth_service = AutenticacionService()
clima_service = ClimaService()
indicadores_service = IndicadoresService()
usuario_actual = None


def resetear_base_datos():
    print("\n=== RESTAURAR BASE DE DATOS A ESTADO BASE ===")
    print("ADVERTENCIA: Se eliminarán TODOS los datos actuales (empleados, proyectos, departamentos, registros, asignaciones).")
    confirm = input("¿Estás seguro de continuar? (s/n): ").strip().lower()
    if confirm != 's':
        print("Operación cancelada.")
        return
    
    try:
        import pymysql
        from DAO.conexion import Conexion
        conexion_obj = Conexion()
        sql_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BASE', 'ecotech.sql')
        
        if not os.path.exists(sql_file):
            print(f"No se encontró el archivo SQL: {sql_file}")
            return
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        config = conexion_obj.config.copy()
        db_name = config.pop('database')
        
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci")
        cursor.execute(f"USE {db_name}")
        
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--') and statement.upper() not in ['CREATE DATABASE', 'USE']:
                try:
                    cursor.execute(statement)
                except Exception:
                    pass
        
        conn.commit()
        cursor.close()
        conn.close()
        print("\n¡Base de datos restaurada a estado base exitosamente!")
        print("Se han cargado los datos de prueba iniciales.")
    except Exception as e:
        print(f"Error al restaurar la base de datos: {e}")
        print("Asegúrate de que MySQL esté corriendo en XAMPP.")

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
    ok, msg = validar_nombre(nombre)
    if not ok:
        print(f"Error: {msg}")
        return
    email = input("Email: ").strip()
    ok, msg = validar_email(email)
    if not ok:
        print(f"Error: {msg}")
        return
    telefono = input("Teléfono: ").strip()
    ok, msg = validar_telefono(telefono)
    if not ok:
        print(f"Error: {msg}")
        return
    salario = leer_float("Salario: ")
    ok, msg = validar_salario(salario)
    if not ok:
        print(f"Error: {msg}")
        return
    rol = input("Rol [Empleado]: ").strip() or "Empleado"
    rol = sanitizar_texto(rol, 50)
    nombre = sanitizar_texto(nombre, 100)
    email = sanitizar_texto(email, 100)
    telefono = sanitizar_texto(telefono, 20)
    
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

def leer_fecha(mensaje):
    while True:
        fecha_str = input(mensaje).strip()
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return fecha_str
        except ValueError:
            print("Error: Ingrese una fecha válida con formato YYYY-MM-DD.")


# --- CRUD PROYECTOS ---

def agregar_proyecto():
    print("\n--- REGISTRAR PROYECTO ---")
    nombre = input("Nombre: ").strip()
    ok, msg = validar_no_vacio(nombre, "nombre")
    if not ok:
        print(f"Error: {msg}")
        return
    descripcion = input("Descripción: ").strip()
    ok, msg = validar_no_vacio(descripcion, "descripción")
    if not ok:
        print(f"Error: {msg}")
        return
    fecha_inicio = leer_fecha("Fecha inicio (YYYY-MM-DD): ")
    ok, msg = validar_fecha(fecha_inicio)
    if not ok:
        print(f"Error: {msg}")
        return
    nombre = sanitizar_texto(nombre, 100)
    descripcion = sanitizar_texto(descripcion, 255)
    
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
    if fec:
        try:
            datetime.strptime(fec, '%Y-%m-%d')
            proy.fecha_inicio = fec
        except ValueError:
            print("Fecha inválida. Se mantiene la fecha actual.")

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
    if horas <= 0:
        print("Error: Las horas deben ser mayor a 0.")
        return
    tarea = input("Descripción de la tarea: ").strip()
    ok, msg = validar_no_vacio(tarea, "descripción de la tarea")
    if not ok:
        print(f"Error: {msg}")
        return
    fecha = leer_fecha("Fecha (YYYY-MM-DD): ")
    ok, msg = validar_fecha(fecha)
    if not ok:
        print(f"Error: {msg}")
        return
    tarea = sanitizar_texto(tarea, 255)

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
        try:
            h = float(h_str)
            if h <= 0:
                print("Las horas deben ser mayor a 0. Se mantiene el valor actual.")
            else:
                reg.horas = h
        except ValueError:
            print("Valor inválido. Se mantiene el valor actual.")
    tar = input(f"Nueva tarea [{reg.descripcion_tarea}]: ").strip()
    if tar:
        reg.descripcion_tarea = tar
    fec = input(f"Nueva fecha [{reg.fecha}]: ").strip()
    if fec:
        try:
            datetime.strptime(fec, '%Y-%m-%d')
            reg.fecha = fec
        except ValueError:
            print("Fecha inválida. Se mantiene la fecha actual.")

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

# --- CRUD DEPARTAMENTOS ---

def agregar_departamento():
    print("\n--- REGISTRAR DEPARTAMENTO ---")
    nombre = input("Nombre: ").strip()
    ok, msg = validar_no_vacio(nombre, "nombre")
    if not ok:
        print(f"Error: {msg}")
        return
    descripcion = input("Descripción: ").strip()
    nombre = sanitizar_texto(nombre, 100)
    descripcion = sanitizar_texto(descripcion, 255)
    print("\nEmpleados disponibles para asignar como gerente:")
    listar_empleados()
    ger_str = input("\nID del gerente (enter para omitir): ").strip()
    gerente_id = None
    if ger_str:
        try:
            gerente_id_cand = int(ger_str)
            if empleado_dao.buscar_por_id(gerente_id_cand):
                gerente_id = gerente_id_cand
            else:
                print("Gerente no encontrado. Se dejará sin asignar.")
        except ValueError:
            print("ID inválido. Se dejará sin asignar.")
    
    dto = DepartamentoDTO(nombre, descripcion, None, gerente_id)
    try:
        nuevo = departamento_dao.guardar(dto)
        print("\n¡Departamento registrado!")
        print(nuevo.mostrar_datos())
    except Exception as e:
        print(f"Error al registrar: {e}")


def listar_departamentos():
    print("\n--- LISTA DE DEPARTAMENTOS ---")
    lista = departamento_dao.listar()
    if not lista:
        print("No hay departamentos registrados.")
    else:
        for d in lista:
            print(d.mostrar_datos())


def buscar_departamento():
    print("\n--- BUSCAR DEPARTAMENTO POR ID ---")
    id_dep = leer_entero("Ingrese ID: ")
    dep = departamento_dao.buscar_por_id(id_dep)
    if dep:
        print(dep.mostrar_datos())
    else:
        print("Departamento no encontrado.")


def actualizar_departamento():
    print("\n--- ACTUALIZAR DEPARTAMENTO ---")
    id_dep = leer_entero("Ingrese ID a modificar: ")
    dep = departamento_dao.buscar_por_id(id_dep)
    if not dep:
        print("Departamento no encontrado.")
        return

    print(f"Datos actuales: {dep.mostrar_datos()}")
    nom = input(f"Nuevo nombre [{dep.nombre}]: ").strip()
    if nom:
        dep.nombre = nom
    desc = input(f"Nueva descripción [{dep.descripcion}]: ").strip()
    if desc:
        dep.descripcion = desc
    print("\nEmpleados disponibles:")
    listar_empleados()
    ger_str = input(f"Nuevo ID de gerente [{dep.gerente_id or 'Sin asignar'}]: ").strip()
    if ger_str:
        try:
            ger_id = int(ger_str)
            if empleado_dao.buscar_por_id(ger_id):
                dep.gerente_id = ger_id
            else:
                print("Gerente no encontrado. Se mantiene el valor anterior.")
        except ValueError:
            print("ID inválido. Se mantiene el valor anterior.")
    
    if departamento_dao.actualizar(dep):
        print("Departamento actualizado correctamente.")
    else:
        print("No se realizaron cambios.")


def eliminar_departamento():
    print("\n--- ELIMINAR DEPARTAMENTO ---")
    id_dep = leer_entero("Ingrese ID a eliminar: ")
    dep = departamento_dao.buscar_por_id(id_dep)
    if not dep:
        print("Departamento no encontrado.")
        return

    print(f"Seleccionado: {dep.mostrar_datos()}")
    confirm = input("¿Confirmar eliminación? (s/n): ").strip().lower()
    if confirm == 's':
        try:
            if departamento_dao.eliminar(id_dep):
                print("Departamento eliminado.")
            else:
                print("No se pudo eliminar.")
        except Exception as e:
            print(f"Error: No se puede eliminar por dependencia ({e}).")


def asignar_empleado_a_departamento():
    print("\n--- ASIGNAR EMPLEADO A DEPARTAMENTO ---")
    print("\nEmpleados:")
    listar_empleados()
    id_emp = leer_entero("\nID del empleado: ")
    emp = empleado_dao.buscar_por_id(id_emp)
    if not emp:
        print("Empleado no encontrado.")
        return
    
    print("\nDepartamentos:")
    listar_departamentos()
    id_dep = leer_entero("\nID del departamento: ")
    dep = departamento_dao.buscar_por_id(id_dep)
    if not dep:
        print("Departamento no encontrado.")
        return
    
    if departamento_dao.asignar_empleado(id_emp, id_dep):
        print(f"Empleado {emp.nombre} asignado a {dep.nombre} correctamente.")
    else:
        print("No se pudo asignar el empleado.")


def quitar_empleado_de_departamento():
    print("\n--- QUITAR EMPLEADO DE DEPARTAMENTO ---")
    print("\nEmpleados:")
    listar_empleados()
    id_emp = leer_entero("\nID del empleado: ")
    emp = empleado_dao.buscar_por_id(id_emp)
    if not emp:
        print("Empleado no encontrado.")
        return
    
    if departamento_dao.quitar_empleado(id_emp):
        print(f"Empleado {emp.nombre} removido del departamento correctamente.")
    else:
        print("No se pudo quitar el empleado del departamento.")


def listar_empleados_de_departamento():
    print("\n--- EMPLEADOS POR DEPARTAMENTO ---")
    listar_departamentos()
    id_dep = leer_entero("\nID del departamento: ")
    dep = departamento_dao.buscar_por_id(id_dep)
    if not dep:
        print("Departamento no encontrado.")
        return
    
    lista = departamento_dao.listar_empleados_por_departamento(id_dep)
    if not lista:
        print("No hay empleados asignados a este departamento.")
    else:
        print(f"\nEmpleados de {dep.nombre}:")
        for e in lista:
            print(e.mostrar_datos())


# --- ASIGNACIÓN EMPLEADO-PROYECTO ---

def asignar_empleado_a_proyecto():
    print("\n--- ASIGNAR EMPLEADO A PROYECTO ---")
    print("\nEmpleados:")
    listar_empleados()
    id_emp = leer_entero("\nID del empleado: ")
    emp = empleado_dao.buscar_por_id(id_emp)
    if not emp:
        print("Empleado no encontrado.")
        return
    
    print("\nProyectos:")
    listar_proyectos()
    id_proy = leer_entero("\nID del proyecto: ")
    proy = proyecto_dao.buscar_por_id(id_proy)
    if not proy:
        print("Proyecto no encontrado.")
        return
    
    fec = leer_fecha("Fecha de asignación (YYYY-MM-DD): ")
    if asignacion_dao.asignar_empleado(id_proy, id_emp, fec):
        print(f"Empleado {emp.nombre} asignado a {proy.nombre} correctamente.")
    else:
        print("El empleado ya se encuentra asignado a este proyecto o no se pudo asignar.")


def desasignar_empleado_de_proyecto():
    print("\n--- DESASIGNAR EMPLEADO DE PROYECTO ---")
    print("\nProyectos:")
    listar_proyectos()
    id_proy = leer_entero("\nID del proyecto: ")
    proy = proyecto_dao.buscar_por_id(id_proy)
    if not proy:
        print("Proyecto no encontrado.")
        return
    
    print(f"\nEmpleados asignados a {proy.nombre}:")
    lista = asignacion_dao.listar_empleados_por_proyecto(id_proy)
    if not lista:
        print("No hay empleados asignados a este proyecto.")
        return
    for emp_dto, fec_asig in lista:
        print(f"{emp_dto.mostrar_datos()} | Asignado: {fec_asig}")
    
    id_emp = leer_entero("\nID del empleado a desasignar: ")
    emp = empleado_dao.buscar_por_id(id_emp)
    if not emp:
        print("Empleado no encontrado.")
        return
    
    confirm = input("¿Confirmar desasignación? (s/n): ").strip().lower()
    if confirm == 's':
        if asignacion_dao.desasignar_empleado(id_proy, id_emp):
            print("Empleado desasignado correctamente.")
        else:
            print("No se pudo desasignar el empleado.")


def listar_equipo_proyecto():
    print("\n--- EQUIPO POR PROYECTO ---")
    listar_proyectos()
    id_proy = leer_entero("\nID del proyecto: ")
    proy = proyecto_dao.buscar_por_id(id_proy)
    if not proy:
        print("Proyecto no encontrado.")
        return
    
    lista = asignacion_dao.listar_empleados_por_proyecto(id_proy)
    if not lista:
        print("No hay empleados asignados a este proyecto.")
    else:
        print(f"\nEquipo de {proy.nombre}:")
        for emp_dto, fec_asig in lista:
            print(f"{emp_dto.mostrar_datos()} | Fecha asignación: {fec_asig}")


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


def submenu_departamentos():
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE DEPARTAMENTOS ===")
        print("1. Agregar departamento")
        print("2. Listar departamentos")
        print("3. Buscar por ID")
        print("4. Actualizar departamento")
        print("5. Eliminar departamento")
        print("6. Asignar empleado a departamento")
        print("7. Quitar empleado de departamento")
        print("8. Listar empleados por departamento")
        print("9. Volver")
        op = input("\nOpción: ").strip()
        if op == "1": agregar_departamento(); pausa()
        elif op == "2": listar_departamentos(); pausa()
        elif op == "3": buscar_departamento(); pausa()
        elif op == "4": actualizar_departamento(); pausa()
        elif op == "5": eliminar_departamento(); pausa()
        elif op == "6": asignar_empleado_a_departamento(); pausa()
        elif op == "7": quitar_empleado_de_departamento(); pausa()
        elif op == "8": listar_empleados_de_departamento(); pausa()
        elif op == "9": break
        else: print("Opción inválida."); pausa()


def submenu_asignaciones():
    while True:
        limpiar_pantalla()
        print("=== ASIGNACIÓN EMPLEADO - PROYECTO ===")
        print("1. Asignar empleado a proyecto")
        print("2. Desasignar empleado de proyecto")
        print("3. Ver equipo por proyecto")
        print("4. Volver")
        op = input("\nOpción: ").strip()
        if op == "1": asignar_empleado_a_proyecto(); pausa()
        elif op == "2": desasignar_empleado_de_proyecto(); pausa()
        elif op == "3": listar_equipo_proyecto(); pausa()
        elif op == "4": break
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

def extra():
    limpiar_pantalla()
    print("""⠀⣠⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠙⠻⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠀⠀⠀⠉⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠀⠀⠀⠀⠀⠈⠹⢶⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⡅⠀⠀⠀⠀⠀⠀⠀⠙⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠟⠛⠛⠛⠛⠿⠷⠶⠶⢶⣦⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠷⢶⣤⣀⡀⠀⠀⠀⠀⣀⣤⡶⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⢶⣤⣾⠛⠁⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢿⡄⠀⠀⠀⢀⣠⣴⣶⣶⣦⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢶⣤⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣸⡷⠀⠀⠀⣾⡟⠁⣶⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢷⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣰⠟⠀⠀⠀⠀⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢰⡟⠀⠀⠀⠀⠀⠹⣷⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡟⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⡿⠿⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⡿⠿⠛⠁⠀⠀⢻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⡆⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠿⠿⠷⢶⣶⣶⠶⠿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣷⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠈⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣄⠀⣼⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣶⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⡤⠶⠶⠶⠶⠶⠶⠤⠦⠀⠀
⠀⠀⠀⠀⠀⠶⠚⠛⠛⠛⠛⠛⠛⠛⠛⠛⠓⠛⠚⠓⠶⠶⠶⠦⢦⣤⣄⣀⠀⠀⠀⠀⠀⠈⠻⣶⣦⣦⡀⠀⠀⠀⠀⠀⣠⣾⢿⡅⡀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⠉⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣧⣤⣤⡶⠾⠛⠋⠁⣼⡟⠉⠉⠉⠛⠛⠶⢦⣤⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⠀⠀⠀⢠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀⠀⠀⣠⡿⠛⠷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⣦⣤⣤⡶⠾⠋⠁⠀⠀⠀⠙⠻⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠳⢦⣤⣀⡀⠀⠀⠀⠀⠀⠀⢀⣀⣤⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠛⠛⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣆""")
    pausa()


# --- SERVICIOS EXTERNOS (API) ---

def menu_servicios_externos():
    global usuario_actual
    if usuario_actual is not None and not auth_service.tiene_permiso(usuario_actual, "api"):
        print("No tiene permisos para acceder a los servicios externos.")
        pausa()
        return
    while True:
        limpiar_pantalla()
        print("=== SERVICIOS EXTERNOS (API) ===")
        print("1. Consultar clima por ciudad")
        print("2. Consultar indicadores económicos")
        print("3. Convertir moneda (CLP <-> USD/EUR)")
        print("4. Volver")
        op = input("\nOpción: ").strip()
        if op == "1":
            consultar_clima()
            pausa()
        elif op == "2":
            consultar_indicadores()
            pausa()
        elif op == "3":
            convertir_moneda()
            pausa()
        elif op == "4":
            break
        else:
            print("Opción inválida."); pausa()


def consultar_clima():
    ciudad = input("Ingrese ciudad: ").strip()
    ok, msg = validar_ciudad(ciudad)
    if not ok:
        print(f"Error: {msg}")
        return
    try:
        datos = clima_service.obtener_clima(ciudad)
        print("\n--- CLIMA ACTUAL ---")
        print(f"Fuente: {datos['fuente']}")
        print(f"Ciudad: {datos['ciudad']} ({datos['pais']})")
        print(f"Temperatura: {datos['temperatura']} °C")
        if datos.get('sensacion') is not None:
            print(f"Sensación térmica: {datos['sensacion']} °C")
        if datos.get('humedad') is not None:
            print(f"Humedad: {datos['humedad']}%")
        print(f"Descripción: {datos['descripcion']}")
        print(f"Viento: {datos['viento']} m/s")
    except Exception as e:
        print(f"Error al consultar clima: {e}")


def consultar_indicadores():
    try:
        datos = indicadores_service.listar_indicadores()
        print("\n--- INDICADORES ECONÓMICOS (mindicador.cl) ---")
        for codigo, info in datos.items():
            print(f"{info['nombre']} ({codigo}): {info['valor']} - {info['fecha']}")
        codigo = input("\nIngrese código para ver detalle (enter para volver): ").strip().lower()
        if codigo:
            # Los indicadores usan códigos propios, no ISO necesariamente.
            try:
                detalle = indicadores_service.obtener_indicador(codigo)
                print(f"\n{detalle['nombre']}: {detalle['valor']} ({detalle['fecha']})")
            except Exception as e:
                print(f"Error: {e}")
    except Exception as e:
        print(f"Error al consultar indicadores: {e}")


def convertir_moneda():
    try:
        monto = float(input("Monto: ").strip())
    except ValueError:
        print("Monto inválido.")
        return
    origen = input("Moneda origen (CLP/USD/EUR): ").strip().upper()
    destino = input("Moneda destino (CLP/USD/EUR): ").strip().upper()
    try:
        resultado, info = indicadores_service.convertir(monto, origen, destino)
        if resultado is None:
            print("No se pudo realizar la conversión.")
        else:
            print(f"\n{monto} {origen} = {resultado:.2f} {destino}")
            print(f"Indicador usado: {info['nombre']} = {info['valor']} ({info['fecha']})")
    except Exception as e:
        print(f"Error: {e}")


# --- SEGURIDAD / USUARIOS ---

def submenu_usuarios():
    global usuario_actual
    if usuario_actual is None or getattr(usuario_actual, "rol", "") != "Administrador":
        print("Solo el administrador puede gestionar usuarios.")
        pausa()
        return
    while True:
        limpiar_pantalla()
        print("=== GESTIÓN DE USUARIOS Y SEGURIDAD ===")
        print("1. Listar usuarios")
        print("2. Crear usuario")
        print("3. Cambiar contraseña")
        print("4. Eliminar usuario")
        print("5. Volver")
        op = input("\nOpción: ").strip()
        if op == "1":
            listar_usuarios()
            pausa()
        elif op == "2":
            crear_usuario()
            pausa()
        elif op == "3":
            cambiar_password_usuario()
            pausa()
        elif op == "4":
            eliminar_usuario()
            pausa()
        elif op == "5":
            break
        else:
            print("Opción inválida."); pausa()


def listar_usuarios():
    try:
        lista = usuario_dao.listar()
        if not lista:
            print("No hay usuarios registrados.")
        else:
            for u in lista:
                print(u.mostrar_datos())
    except Exception as e:
        print(f"Error al listar usuarios: {e}")


def crear_usuario():
    username = input("Nombre de usuario: ").strip()
    password = input("Contraseña: ")
    print("Roles disponibles: Administrador, Gerente, Empleado, Lector")
    rol = input("Rol [Empleado]: ").strip() or "Empleado"
    emp_str = input("ID empleado asociado (enter para omitir): ").strip()
    empleado_id = None
    if emp_str:
        try:
            empleado_id = int(emp_str)
        except ValueError:
            print("ID de empleado inválido. Se omite.")
            empleado_id = None
    try:
        nuevo = auth_service.registrar_usuario(username, password, rol, empleado_id)
        print("\n¡Usuario creado!")
        print(nuevo.mostrar_datos())
    except Exception as e:
        print(f"Error al crear usuario: {e}")


def cambiar_password_usuario():
    username = input("Usuario: ").strip()
    actual = input("Contraseña actual: ")
    nuevo = input("Nueva contraseña: ")
    ok, msg = auth_service.cambiar_password(username, actual, nuevo)
    print(msg)


def eliminar_usuario():
    try:
        lista = usuario_dao.listar()
        for u in lista:
            print(u.mostrar_datos())
    except Exception as e:
        print(f"Error: {e}")
        return
    try:
        id_usr = int(input("\nID de usuario a eliminar: ").strip())
    except ValueError:
        print("ID inválido.")
        return
    if usuario_actual is not None and id_usr == usuario_actual.id_usuario:
        print("No puede eliminar su propio usuario.")
        return
    confirm = input("¿Confirmar eliminación? (s/n): ").strip().lower()
    if confirm == "s":
        try:
            if usuario_dao.eliminar(id_usr):
                print("Usuario eliminado.")
            else:
                print("No se pudo eliminar.")
        except Exception as e:
            print(f"Error: {e}")


def menu_principal():
    while True:
        limpiar_pantalla()
        print("==========================================")
        print("   SISTEMA DE GESTION ECOTECH SOLUTIONS   ")
        print("==========================================")
        print("1. Gestión de Empleados")
        print("2. Gestión de Departamentos")
        print("3. Gestión de Proyectos")
        print("4. Asignación Empleado-Proyecto")
        print("5. Registro de Tiempo")
        print("6. Servicios Externos (API)")
        print("7. Usuarios y Seguridad")
        print("8. Restaurar base de datos a estado base")
        print("9. Extra")
        print("10. Salir")
        op = input("\nOpción: ").strip()
        if op == "1": submenu_empleados()
        elif op == "2": submenu_departamentos()
        elif op == "3": submenu_proyectos()
        elif op == "4": submenu_asignaciones()
        elif op == "5": submenu_registros()
        elif op == "6": menu_servicios_externos()
        elif op == "7": submenu_usuarios()
        elif op == "8":
            resetear_base_datos()
            pausa()
        elif op == "9": extra()
        elif op == "10":
            print("\nCerrando aplicación EcoTech Solutions...")
            break
        else: print("Opción inválida."); pausa()

def iniciar_sesion():
    global usuario_actual
    limpiar_pantalla()
    print("==========================================")
    print("   ACCESO SEGURO - ECOTECH SOLUTIONS      ")
    print("==========================================")
    print("Ingrese sus credenciales para continuar.\n")
    intentos = 3
    while intentos > 0:
        username = input("Usuario: ").strip()
        password = input("Contraseña: ")
        usuario = auth_service.login(username, password)
        if usuario is not None:
            usuario_actual = usuario
            print(f"\nBienvenido/a, {usuario.username} ({usuario.rol}).")
            pausa()
            return True
        intentos -= 1
        print(f"Credenciales inválidas. Intentos restantes: {intentos}")
    print("\nDemasiados intentos fallidos. Cerrando aplicación.")
    return False


if __name__ == "__main__":
    if iniciar_sesion():
        menu_principal()
