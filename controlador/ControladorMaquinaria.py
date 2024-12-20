from modelo.Maquinaria import Maquinaria

class ControladorMaquinaria:
    def __init__(self):
        self.maquina_modelo = Maquinaria()

    def listar_maquinarias(self):
        """Obtiene las marcas del modelo y las pasa a la vista"""
        return self.maquina_modelo.obtener_maquinarias()
