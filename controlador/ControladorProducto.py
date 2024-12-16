# controlador/ControladorProducto.py
from modelo.Producto import Producto

class ControladorProducto:
    def __init__(self):
        self.modelo_producto = Producto()

    def registrar_producto(self, partname, descripcion, idmarca, undMedida, cantidad, idproveedor, idalmacen, uso, equipo, precio):
        """Método para registrar un nuevo producto usando el modelo"""
        exito = self.modelo_producto.registrar_producto(partname, descripcion, idmarca, undMedida, cantidad, idproveedor, idalmacen, uso, equipo, precio)
        return exito
