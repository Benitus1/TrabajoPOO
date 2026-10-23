from DAO.conexion import Conexion
from DTO.empleado_dto import EmpleadoDTO

class EmpleadoDAO:
    def __init__(self):
        self.conexion_obj = Conexion()

    def guardar(self, empleado: EmpleadoDTO):
        sql = "INSERT INTO empleados (nombre, email, telefono, salario, rol, departamento_id) VALUES (%s, %s, %s, %s, %s, %s)"
        departamento_id = getattr(empleado, 'departamento_id', None)
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (empleado.nombre, empleado.email, empleado.telefono, empleado.salario, empleado.rol, departamento_id))
                conn.commit()
                empleado.id_empleado = cursor.lastrowid
                return empleado

    def listar(self):
        sql = "SELECT id, nombre, email, telefono, salario, rol, departamento_id FROM empleados ORDER BY id"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                filas = cursor.fetchall()
                lista = []
                for f in filas:
                    dto = EmpleadoDTO(f['nombre'], f['email'], f['telefono'], float(f['salario']), f['rol'], f['id'])
                    dto.departamento_id = f.get('departamento_id')
                    lista.append(dto)
                return lista

    def buscar_por_id(self, id_empleado: int):
        sql = "SELECT id, nombre, email, telefono, salario, rol, departamento_id FROM empleados WHERE id = %s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_empleado,))
                f = cursor.fetchone()
                if f:
                    dto = EmpleadoDTO(f['nombre'], f['email'], f['telefono'], float(f['salario']), f['rol'], f['id'])
                    dto.departamento_id = f.get('departamento_id')
                    return dto
                return None

    def actualizar(self, empleado: EmpleadoDTO):
        sql = "UPDATE empleados SET nombre=%s, email=%s, telefono=%s, salario=%s, rol=%s, departamento_id=%s WHERE id=%s"
        departamento_id = getattr(empleado, 'departamento_id', None)
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (empleado.nombre, empleado.email, empleado.telefono, empleado.salario, empleado.rol, departamento_id, empleado.id_empleado))
                conn.commit()
                return cursor.rowcount > 0

    def eliminar(self, id_empleado: int):
        sql = "DELETE FROM empleados WHERE id = %s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_empleado,))
                conn.commit()
                return cursor.rowcount > 0
