import hashlib
from datetime import date

class Empleado:
    def __init__(self, id_empleado: str, nombre: str, direccion: str, telefono: str, email: str, fecha_inicio: date, salario: float):
        self.__id_empleado = id_empleado
        self.__nombre = nombre
        self.__direccion = direccion
        self.__telefono = telefono
        self.__email = email
        self.__fecha_inicio = fecha_inicio
        self.__salario = salario

    @property
    def salario(self) -> float:
        return self.__salario

    @salario.setter
    def salario(self, nuevo_salario: float):
        if nuevo_salario > 0:
            self.__salario = nuevo_salario

    def obtener_perfil(self) -> dict:
        return {"id": self.__id_empleado, "nombre": self.__nombre, "email": self.__email}

    def actualizar_contacto(self, direccion: str, telefono: str, email: str) -> bool:
        self.__direccion = direccion
        self.__telefono = telefono
        self.__email = email
        return True


class Gerente(Empleado):
    def __init__(self, id_empleado: str, nombre: str, direccion: str, telefono: str, email: str, fecha_inicio: date, salario: float, bono_gestion: float):
        super().__init__(id_empleado, nombre, direccion, telefono, email, fecha_inicio, salario)
        self.__bono_gestion = bono_gestion

    def autorizar_horas(self, registro) -> bool:
        return True

    def asignar_presupuesto(self, monto: float) -> None:
        pass


class Departamento:
    def __init__(self, id_depto: str, nombre: str, gerente: Gerente = None):
        self.__id_depto = id_depto
        self.__nombre = nombre
        self.__gerente = gerente
        self.__empleados: list[Empleado] = []

    def agregar_empleado(self, emp: Empleado) -> bool:
        self.__empleados.append(emp)
        return True

    def remover_empleado(self, id_empleado: str) -> bool:
        return True

    def asignar_gerente(self, nuevo_gerente: Gerente) -> None:
        self.__gerente = nuevo_gerente

    def listar_empleados(self) -> list[Empleado]:
        return self.__empleados


class Proyecto:
    def __init__(self, id_proyecto: str, nombre: str, descripcion: str, fecha_inicio: date):
        self.__id_proyecto = id_proyecto
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fecha_inicio = fecha_inicio
        self.__equipo: list[Empleado] = []

    def asignar_empleado(self, emp: Empleado) -> bool:
        self.__equipo.append(emp)
        return True

    def desasignar_empleado(self, id_empleado: str) -> bool:
        return True

    def obtener_resumen_proyecto(self) -> dict:
        return {"id": self.__id_proyecto, "nombre": self.__nombre, "integrantes": len(self.__equipo)}


class RegistroTiempo:
    def __init__(self, id_registro: str, fecha: date, horas: float, descripcion_tarea: str, empleado: Empleado, proyecto: Proyecto):
        self.__id_registro = id_registro
        self.__fecha = fecha
        self.__horas = horas
        self.__descripcion_tarea = descripcion_tarea
        self.__empleado = empleado
        self.__proyecto = proyecto

    def validar_horas(self) -> bool:
        return self.__horas > 0

    def obtener_detalle(self) -> str:
        return f"registro {self.__id_registro}: {self.__horas}h en tarea {self.__descripcion_tarea}"


class Usuario:
    def __init__(self, id_usuario: str, username: str, password_plana: str, rol: str, empleado_asociado: Empleado):
        self.__id_usuario = id_usuario
        self.__username = username
        self.__password_hash = hashlib.sha256(password_plana.encode()).hexdigest()
        self.__rol = rol
        self.__empleado_asociado = empleado_asociado

    def autenticar(self, password_plana: str) -> bool:
        hash_ingresado = hashlib.sha256(password_plana.encode()).hexdigest()
        return self.__password_hash == hash_ingresado

    def verificar_permiso(self, modulo: str) -> bool:
        return True

    def cambiar_password(self, antiguo_pass: str, nuevo_pass: str) -> bool:
        if self.autenticar(antiguo_pass):
            self.__password_hash = hashlib.sha256(nuevo_pass.encode()).hexdigest()
            return True
        return False


class GeneradorInformes:
    def __init__(self, formato_salida: str = "PDF"):
        self.__formato_salida = formato_salida

    def exportar_informe_empleados(self, dept: Departamento, formato: str):
        return f"informe del departamento en formato {formato}"

    def exportar_informe_horas_proyecto(self, proy: Proyecto, formato: str):
        return f"informe de horas del proyecto en formato {formato}"

    def generar_consolidado_horas(self, registros: list[RegistroTiempo]):
        return "consolidado generado"
