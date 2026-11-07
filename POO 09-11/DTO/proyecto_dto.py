class ProyectoDTO:
    def __init__(self, nombre, descripcion, fecha_inicio, id_proyecto=None):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

    def mostrar_datos(self):
        return f"ID: {self.id_proyecto} | Proyecto: {self.nombre} | Fecha Inicio: {self.fecha_inicio} | Descripción: {self.descripcion}"
