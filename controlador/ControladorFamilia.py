# controlador/controlador_marca.py
from modelo.familia import Familia

class ControladorFamilia:
    def __init__(self):
        self.familia_modelo = Familia()

    def listar_familias(self):
        """Obtiene las marcas del modelo y las pasa a la vista"""
        return self.familia_modelo.listar_familias()
