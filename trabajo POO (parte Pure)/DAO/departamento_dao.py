from DAO.conexion import Conexion
from DTO.departamento_dto import DepartamentoDTO


class DepartamentoDAO:
    def __init__(self):
        self.conexion_obj = Conexion()

    def guardar(self, departamento: DepartamentoDTO):
        sql = "INSERT INTO departamentos (nombre, descripcion, gerente_id) VALUES (%s, %s, %s)"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (departamento.nombre, departamento.descripcion, departamento.gerente_id))
                conn.commit()
                departamento.id_departamento = cursor.lastrowid
                return departamento

    def listar(self):
        sql = """
        SELECT d.id, d.nombre, d.descripcion, d.gerente_id, e.nombre AS nombre_gerente
        FROM departamentos d
        LEFT JOIN empleados e ON d.gerente_id = e.id
        ORDER BY d.id
        """
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                filas = cursor.fetchall()
                lista = []
                for f in filas:
                    dto = DepartamentoDTO(f['nombre'], f['descripcion'] or "", f['id'], f['gerente_id'])
                    dto.nombre_gerente = f['nombre_gerente']
                    lista.append(dto)
                return lista

    def buscar_por_id(self, id_departamento: int):
        sql = """
        SELECT d.id, d.nombre, d.descripcion, d.gerente_id, e.nombre AS nombre_gerente
        FROM departamentos d
        LEFT JOIN empleados e ON d.gerente_id = e.id
        WHERE d.id = %s
        """
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_departamento,))
                f = cursor.fetchone()
                if f:
                    dto = DepartamentoDTO(f['nombre'], f['descripcion'] or "", f['id'], f['gerente_id'])
                    dto.nombre_gerente = f['nombre_gerente']
                    return dto
                return None

    def actualizar(self, departamento: DepartamentoDTO):
        sql = "UPDATE departamentos SET nombre=%s, descripcion=%s, gerente_id=%s WHERE id=%s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (departamento.nombre, departamento.descripcion, departamento.gerente_id, departamento.id_departamento))
                conn.commit()
                return cursor.rowcount > 0

    def eliminar(self, id_departamento: int):
        sql = "DELETE FROM departamentos WHERE id = %s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_departamento,))
                conn.commit()
                return cursor.rowcount > 0

    def asignar_empleado(self, empleado_id: int, departamento_id: int):
        sql = "UPDATE empleados SET departamento_id=%s WHERE id=%s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (departamento_id, empleado_id))
                conn.commit()
                return cursor.rowcount > 0

    def quitar_empleado(self, empleado_id: int):
        sql = "UPDATE empleados SET departamento_id=NULL WHERE id=%s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (empleado_id,))
                conn.commit()
                return cursor.rowcount > 0

    def listar_empleados_por_departamento(self, departamento_id: int):
        sql = """
        SELECT id, nombre, email, telefono, salario, rol, departamento_id
        FROM empleados
        WHERE departamento_id = %s
        ORDER BY id
        """
        from DTO.empleado_dto import EmpleadoDTO
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (departamento_id,))
                filas = cursor.fetchall()
                lista = []
                for f in filas:
                    dto = EmpleadoDTO(f['nombre'], f['email'], f['telefono'], float(f['salario']), f['rol'], f['id'])
                    lista.append(dto)
                return lista
