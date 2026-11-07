from DAO.conexion import Conexion
from DTO.usuario_dto import UsuarioDTO


class UsuarioDAO:
    def __init__(self):
        self.conexion_obj = Conexion()
        self._crear_tabla()

    def _crear_tabla(self):
        sql = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            rol VARCHAR(50) NOT NULL DEFAULT 'Empleado',
            empleado_id INT NULL,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_usuario_empleado FOREIGN KEY (empleado_id)
                REFERENCES empleados(id) ON UPDATE CASCADE ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
        """
        try:
            with self.conexion_obj.conectar() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    conn.commit()
        except Exception:
            # La tabla puede no crearse si la BD no está disponible; se reintenta luego.
            pass

    def guardar(self, usuario: UsuarioDTO):
        sql = "INSERT INTO usuarios (username, password_hash, rol, empleado_id) VALUES (%s, %s, %s, %s)"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (usuario.username, usuario.password_hash, usuario.rol, usuario.empleado_id))
                conn.commit()
                usuario.id_usuario = cursor.lastrowid
                return usuario

    def buscar_por_username(self, username):
        sql = "SELECT id, username, password_hash, rol, empleado_id FROM usuarios WHERE username = %s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (username,))
                f = cursor.fetchone()
                if f:
                    dto = UsuarioDTO(f['username'], f['password_hash'], f['rol'], f['empleado_id'], f['id'])
                    return dto
                return None

    def buscar_por_id(self, id_usuario):
        sql = "SELECT id, username, password_hash, rol, empleado_id FROM usuarios WHERE id = %s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_usuario,))
                f = cursor.fetchone()
                if f:
                    return UsuarioDTO(f['username'], f['password_hash'], f['rol'], f['empleado_id'], f['id'])
                return None

    def listar(self):
        sql = "SELECT id, username, password_hash, rol, empleado_id FROM usuarios ORDER BY id"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                filas = cursor.fetchall()
                lista = []
                for f in filas:
                    lista.append(UsuarioDTO(f['username'], f['password_hash'], f['rol'], f['empleado_id'], f['id']))
                return lista

    def contar(self):
        sql = "SELECT COUNT(*) AS total FROM usuarios"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                f = cursor.fetchone()
                return int(f['total']) if f else 0

    def actualizar_password(self, id_usuario, nuevo_hash):
        sql = "UPDATE usuarios SET password_hash=%s WHERE id=%s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (nuevo_hash, id_usuario))
                conn.commit()
                return cursor.rowcount > 0

    def actualizar_rol(self, id_usuario, nuevo_rol):
        sql = "UPDATE usuarios SET rol=%s WHERE id=%s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (nuevo_rol, id_usuario))
                conn.commit()
                return cursor.rowcount > 0

    def eliminar(self, id_usuario):
        sql = "DELETE FROM usuarios WHERE id = %s"
        with self.conexion_obj.conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (id_usuario,))
                conn.commit()
                return cursor.rowcount > 0
