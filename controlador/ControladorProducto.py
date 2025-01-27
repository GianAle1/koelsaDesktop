# controlador/ControladorProducto.py
from modelo.Producto import Producto

class ControladorProducto:
    def __init__(self):
        self.modelo_producto = Producto()

    def registrar_producto(self, nombre, descripcion, cantidad, precio, codigoInterno, sap, marca_id, almacen_id, und_medida, familia):
        return self.modelo_producto.registrar_producto(
            nombre, descripcion, cantidad, precio, codigoInterno, sap, marca_id, almacen_id, und_medida, familia
        )

    def listar_productos(self):
        return self.modelo_producto.listar_productos()
    
    def listar_productos_por_familia(self, familia):
        return self.modelo_producto.listar_productos_por_familia(familia)

