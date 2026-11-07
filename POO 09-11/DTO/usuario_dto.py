class UsuarioDTO:
    def __init__(self, username, password_hash, rol="Empleado", empleado_id=None, id_usuario=None):
        self.id_usuario = id_usuario
        self.username = username
        self.password_hash = password_hash
        self.rol = rol
        self.empleado_id = empleado_id

    def mostrar_datos(self):
        emp = f"Empleado ID {self.empleado_id}" if self.empleado_id else "Sin empleado asociado"
        return f"ID: {self.id_usuario} | Usuario: {self.username} | Rol: {self.rol} | {emp}"