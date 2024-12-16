# controlador/controlador_marca.py
from modelo.uso import Uso

class ControladorUso:
    def __init__(self):
        self.uso_modelo = Uso()

    def listar_usos(self):
        """Obtiene las marcas del modelo y las pasa a la vista"""
        return self.uso_modelo.listar_usos()
