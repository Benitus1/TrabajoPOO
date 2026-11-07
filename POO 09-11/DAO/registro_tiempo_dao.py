from DAO.conexion import Conexion
from DTO.registro_tiempo_dto import RegistroTiempoDTO

class RegistroTiempoDAO:
    def __init__(self):
        self.conexion_obj = Conexion()

    def guardar(self, registro: RegistroTiempoDTO):
        sql = "INSERT INTO registros_tiempo (horas, descripcion_tarea, fecha, empleado_id, proyecto_id) VALUES (%s, %s, %s, %s, %s)"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (registro.horas, registro.descripcion_tarea, registro.fecha, registro.empleado_id, registro.proyecto_id))
                conn.commit()
                registro.id_registro = cursor.lastrowid
                return registro

    def listar(self):
        # Consulta canónica con INNER JOIN para traer los nombres asociados
        sql = """
        SELECT r.id, r.horas, r.descripcion_tarea, r.fecha, r.empleado_id, r.proyecto_id,
               e.nombre AS nombre_empleado, p.nombre AS nombre_proyecto
        FROM registros_tiempo r
        INNER JOIN empleados e ON r.empleado_id = e.id
        INNER JOIN proyectos p ON r.proyecto_id = p.id
        ORDER BY r.id
        """
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                filas = cursor.fetchall()
                lista = []
                for f in filas:
                    dto = RegistroTiempoDTO(float(f['horas']), f['descripcion_tarea'], str(f['fecha']), f['empleado_id'], f['proyecto_id'], f['id'])
                    dto.nombre_empleado = f['nombre_empleado']
                    dto.nombre_proyecto = f['nombre_proyecto']
                    lista.append(dto)
                return lista

    def buscar_por_id(self, id_registro: int):
        sql = """
        SELECT r.id, r.horas, r.descripcion_tarea, r.fecha, r.empleado_id, r.proyecto_id,
               e.nombre AS nombre_empleado, p.nombre AS nombre_proyecto
        FROM registros_tiempo r
        INNER JOIN empleados e ON r.empleado_id = e.id
        INNER JOIN proyectos p ON r.proyecto_id = p.id
        WHERE r.id = %s
        """
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_registro,))
                f = cursor.fetchone()
                if f:
                    dto = RegistroTiempoDTO(float(f['horas']), f['descripcion_tarea'], str(f['fecha']), f['empleado_id'], f['proyecto_id'], f['id'])
                    dto.nombre_empleado = f['nombre_empleado']
                    dto.nombre_proyecto = f['nombre_proyecto']
                    return dto
                return None

    def actualizar(self, registro: RegistroTiempoDTO):
        sql = "UPDATE registros_tiempo SET horas=%s, descripcion_tarea=%s, fecha=%s, empleado_id=%s, proyecto_id=%s WHERE id=%s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (registro.horas, registro.descripcion_tarea, registro.fecha, registro.empleado_id, registro.proyecto_id, registro.id_registro))
                conn.commit()
                return cursor.rowcount > 0

    def eliminar(self, id_registro: int):
        sql = "DELETE FROM registros_tiempo WHERE id = %s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_registro,))
                conn.commit()
                return cursor.rowcount > 0
