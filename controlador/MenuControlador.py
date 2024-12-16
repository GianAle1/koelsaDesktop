# controlador/menu_controlador.py
from controlador.ControladorMarca import ControladorMarca

class MenuControlador:
    def __init__(self):
        self.controlador_marca = ControladorMarca()

    def registrar_marca(self, nombre_marca):
        """Método para registrar una nueva marca"""
        # Delegamos el registro al ControladorMarca
        return self.controlador_marca.registrar_marca(nombre_marca)

    def eliminar_marca(self, marca_id):
        """Método para eliminar una marca"""
        # Delegamos la eliminación al ControladorMarca
        return self.controlador_marca.eliminar_marca(marca_id)
    def listar_marcas(self):
        """Obtener las marcas a través del controlador de marcas"""
        return self.controlador_marca.listar_marcas()  # Delegar la obtención de marcas al controlador de marcas
