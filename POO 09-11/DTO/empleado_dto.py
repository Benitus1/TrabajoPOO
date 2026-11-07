class EmpleadoDTO:
    def __init__(self, nombre, email, telefono, salario, rol="Empleado", id_empleado=None):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.salario = salario
        self.rol = rol

    def mostrar_datos(self):
        return f"ID: {self.id_empleado} | Nombre: {self.nombre} | Email: {self.email} | Teléfono: {self.telefono} | Salario: ${self.salario:,.0f} | Rol: {self.rol}"
