from DAO.conexion import Conexion
from DTO.proyecto_dto import ProyectoDTO

class ProyectoDAO:
    def __init__(self):
        self.conexion_obj = Conexion()

    def guardar(self, proyecto: ProyectoDTO):
        sql = "INSERT INTO proyectos (nombre, descripcion, fecha_inicio) VALUES (%s, %s, %s)"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio))
                conn.commit()
                proyecto.id_proyecto = cursor.lastrowid
                return proyecto

    def listar(self):
        sql = "SELECT id, nombre, descripcion, fecha_inicio FROM proyectos ORDER BY id"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                filas = cursor.fetchall()
                lista = []
                for f in filas:
                    dto = ProyectoDTO(f['nombre'], f['descripcion'], str(f['fecha_inicio']), f['id'])
                    lista.append(dto)
                return lista

    def buscar_por_id(self, id_proyecto: int):
        sql = "SELECT id, nombre, descripcion, fecha_inicio FROM proyectos WHERE id = %s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_proyecto,))
                f = cursor.fetchone()
                if f:
                    return ProyectoDTO(f['nombre'], f['descripcion'], str(f['fecha_inicio']), f['id'])
                return None

    def actualizar(self, proyecto: ProyectoDTO):
        sql = "UPDATE proyectos SET nombre=%s, descripcion=%s, fecha_inicio=%s WHERE id=%s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, proyecto.id_proyecto))
                conn.commit()
                return cursor.rowcount > 0

    def eliminar(self, id_proyecto: int):
        sql = "DELETE FROM proyectos WHERE id = %s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_proyecto,))
                conn.commit()
                return cursor.rowcount > 0
