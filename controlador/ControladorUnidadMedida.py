# controlador/controlador_marca.py
from modelo.UnidadMedida import UnidadMedida

class ControladorUnidadMedida:
    def __init__(self):
        self.unidadMedida_modelo= UnidadMedida()

    def listar_unidadMedidas(self):
        return self.unidadMedida_modelo.listar_unidadMedidas()
