from DAO.conexion import Conexion
from DTO.empleado_dto import EmpleadoDTO


class ProyectoAsignacionDAO:
    def __init__(self):
        self.conexion_obj = Conexion()

    def asignar_empleado(self, proyecto_id: int, empleado_id: int, fecha_asignacion: str = None):
        from datetime import date
        if fecha_asignacion is None:
            fecha_asignacion = date.today().strftime('%Y-%m-%d')
        sql = "INSERT IGNORE INTO proyecto_empleados (proyecto_id, empleado_id, fecha_asignacion) VALUES (%s, %s, %s)"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (proyecto_id, empleado_id, fecha_asignacion))
                conn.commit()
                return cursor.rowcount > 0

    def desasignar_empleado(self, proyecto_id: int, empleado_id: int):
        sql = "DELETE FROM proyecto_empleados WHERE proyecto_id=%s AND empleado_id=%s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (proyecto_id, empleado_id))
                conn.commit()
                return cursor.rowcount > 0

    def listar_empleados_por_proyecto(self, proyecto_id: int):
        sql = """
        SELECT e.id, e.nombre, e.email, e.telefono, e.salario, e.rol, pe.fecha_asignacion
        FROM proyecto_empleados pe
        INNER JOIN empleados e ON pe.empleado_id = e.id
        WHERE pe.proyecto_id = %s
        ORDER BY e.id
        """
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (proyecto_id,))
                filas = cursor.fetchall()
                lista = []
                for f in filas:
                    dto = EmpleadoDTO(f['nombre'], f['email'], f['telefono'], float(f['salario']), f['rol'], f['id'])
                    lista.append((dto, str(f['fecha_asignacion'])))
                return lista

    def listar_proyectos_por_empleado(self, empleado_id: int):
        sql = """
        SELECT p.id, p.nombre, p.descripcion, p.fecha_inicio, pe.fecha_asignacion
        FROM proyecto_empleados pe
        INNER JOIN proyectos p ON pe.proyecto_id = p.id
        WHERE pe.empleado_id = %s
        ORDER BY p.id
        """
        from DTO.proyecto_dto import ProyectoDTO
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (empleado_id,))
                filas = cursor.fetchall()
                lista = []
                for f in filas:
                    dto = ProyectoDTO(f['nombre'], f['descripcion'], str(f['fecha_inicio']), f['id'])
                    lista.append((dto, str(f['fecha_asignacion'])))
                return lista
