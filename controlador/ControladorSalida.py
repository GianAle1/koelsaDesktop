from modelo.Salida import Salida

class ControladorSalida:
    def __init__(self):
        self.salida_modelo = Salida() 

    def guardar_salida(self, fecha, responsable, productos_temporales,observaciones):
        """Llama al modelo para registrar la salida."""
        return self.salida_modelo.guardar_salida(fecha, responsable, productos_temporales,observaciones)
    
    def obtener_salidas_por_producto(self, producto_id):
        """Obtiene el historial de salidas para un producto específico."""
        return self.salida_modelo.obtener_salidas_por_producto(producto_id)  # Usamos el atributo correcto