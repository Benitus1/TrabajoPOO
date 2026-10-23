class RegistroTiempoDTO:
    def __init__(self, horas, descripcion_tarea, fecha, empleado_id, proyecto_id, id_registro=None):
        self.id_registro = id_registro
        self.horas = horas
        self.descripcion_tarea = descripcion_tarea
        self.fecha = fecha
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.nombre_empleado = None
        self.nombre_proyecto = None

    def mostrar_resumen(self):
        emp = self.nombre_empleado if self.nombre_empleado else f"ID {self.empleado_id}"
        proy = self.nombre_proyecto if self.nombre_proyecto else f"ID {self.proyecto_id}"
        return f"N° Registro: {self.id_registro} | Empleado: {emp} | Proyecto: {proy} | Horas: {self.horas} | Fecha: {self.fecha} | Tarea: {self.descripcion_tarea}"
