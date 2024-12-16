
from modelo.Equipo import Equipo

class ControladorEquipo:
    def __init__(self):
        self.equipo_modelo = Equipo()

    def listar_equipos(self):
        """Obtiene las marcas del modelo y las pasa a la vista"""
        return self.equipo_modelo.listar_equipos()
