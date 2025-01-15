# controlador/controlador_marca.py
from modelo.almacen import Almacen

class ControladorAlmacen:
    def __init__(self):
        self.almacen_modelo = Almacen()

    def registrar_Almacen(self, nombre_almacen,direccion,capacidad):
        exito = self.almacen_modelo.registrar_almacen(nombre_almacen,direccion,capacidad)
        if exito:
            return self.listar_almacenes()  # Solo retornamos las marcas si la inserción fue exitosa
        else:
            return None  # En caso de error, retornamos None

    def eliminar_almacen(self, almacen_id):
        """Método para eliminar una alamacen usando el modelo"""
        exito = self.almacen_modelo.eliminar_almacen(almacen_id)
        if exito:
            return self.listar_almacenes()  # Solo retornamos las marcas si la eliminación fue exitosa
        else:
            return None  # En caso de error, retornamos None

    def listar_almacenes(self):
        """Obtiene las marcas del modelo y las pasa a la vista"""
        return self.almacen_modelo.listar_almacenes()
    
    def listar_subalmacenes(self, almacen_id):
        """Consulta los subalmacenes de un almacén desde el modelo."""
        return self.almacen_modelo.obtener_subalmacenes(almacen_id)

