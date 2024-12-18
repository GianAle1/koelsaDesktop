from modelo.marca import Marca

class ControladorMarca:
    def __init__(self):
        self.marca_modelo = Marca()

    def registrar_marca(self, nombre_marca):
        """Método para registrar una nueva marca usando el modelo"""
        exito = self.marca_modelo.registrar_marca(nombre_marca)
        if exito:
            return self.listar_marcas()
        else:
            return None

    def eliminar_marca(self, marca_id):
        """Método para eliminar una marca usando el modelo"""
        exito = self.marca_modelo.eliminar_marca(marca_id)
        if exito:
            return self.listar_marcas()
        else:
            return None  

    def listar_marcas(self):
        """Obtiene las marcas del modelo y las pasa a la vista"""
        return self.marca_modelo.listar_marcas()
