from modelo.Entrada import Entrada

class ControladorEntrada:
    def __init__(self):
        self.modelo_entrada = Entrada()

    def guardar_entrada(self, fecha, productos):
        """Guarda una entrada y sus detalles en la base de datos"""
        return self.modelo_entrada.guardar_entrada(fecha, productos)
