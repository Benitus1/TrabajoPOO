class DepartamentoDTO:
    def __init__(self, nombre, descripcion="", id_departamento=None, gerente_id=None):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.descripcion = descripcion
        self.gerente_id = gerente_id
        self.nombre_gerente = None

    def mostrar_datos(self):
        gerente = self.nombre_gerente if self.nombre_gerente else (f"ID {self.gerente_id}" if self.gerente_id else "Sin asignar")
        return f"ID: {self.id_departamento} | Nombre: {self.nombre} | Gerente: {gerente} | Descripción: {self.descripcion}"