# controlador/controlador_familia.py
from modelo.Familia import Familia

class ControladorFamilia:
    def __init__(self):
        self.familia_modelo = Familia()

    def listar_familias(self):
        """Obtiene las familias del modelo y las pasa a la vista"""
        return self.familia_modelo.listar_familias()

    def registrar_familia(self, nombre_familia):
        """Registra una nueva familia en la base de datos"""
        return self.familia_modelo.registrar_familia(nombre_familia)

    def eliminar_familia(self, idfamilia):
        """Elimina una familia de la base de datos"""
        return self.familia_modelo.eliminar_familia(idfamilia)
