from modelo.Salida import Salida

class ControladorSalida:
    def __init__(self):
        self.salida_modelo = Salida() 

    def guardar_salida(self, fecha, id_responsable, id_proyecto, productos_temporales, observaciones):
        """Llama al modelo para registrar la salida en la base de datos."""
        return self.salida_modelo.guardar_salida(fecha, id_responsable, id_proyecto, productos_temporales, observaciones)

    
    def obtener_salidas_por_producto(self, producto_id):
        """Obtiene el historial de salidas para un producto específico."""
        return self.salida_modelo.obtener_salidas_por_producto(producto_id)  # Usamos el atributo correcto
    
    def obtener_todas_las_salidas(self):
        """Obtiene todas las salidas registradas en la base de datos."""
        return self.salida_modelo.obtener_todas_las_salidas()
    
    def listar_proyectos(self):
        """Retorna la lista de proyectos desde el modelo."""
        return self.salida_modelo.listar_proyectos()
