from modelo.Salida import Salida

class ControladorSalida:
    def __init__(self):
        self.salida_modelo = Salida() 

    def guardar_salida(self, fecha, responsable, productos_temporales):
        """Llama al modelo para registrar la salida."""
        return self.salida_modelo.guardar_salida(fecha, responsable, productos_temporales)