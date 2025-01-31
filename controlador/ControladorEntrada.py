from modelo.Entrada import Entrada

class ControladorEntrada:
    def __init__(self):
        self.modelo_entrada = Entrada()

    def guardar_entrada(self, fecha, docu_ingreso, productos):
        """Guarda una entrada y sus detalles en la base de datos"""
        return self.modelo_entrada.guardar_entrada(fecha, docu_ingreso, productos)

    
    def obtener_entradas_por_producto(self, producto_id):
        """Obtiene el historial de entradas para un producto específico."""
        return self.modelo_entrada.obtener_entradas_por_producto(producto_id)
    
    def obtener_todas_las_entradas(self):
        """Obtiene todas las entradas registradas en la base de datos."""
        return self.modelo_entrada.obtener_todas_las_entradas()