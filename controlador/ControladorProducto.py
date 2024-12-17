# controlador/ControladorProducto.py
from modelo.Producto import Producto

class ControladorProducto:
    def __init__(self):
        self.modelo_producto = Producto()

    def registrar_producto(self, nombre, descripcion, cantidad, precio, proveedor_id, marca_id, almacen_id, und_medida, uso, equipo,familia):
        # Llamar al modelo para registrar el producto
        return self.modelo_producto.registrar_producto(nombre, descripcion, cantidad, precio, proveedor_id, marca_id, almacen_id, und_medida, uso, equipo,familia)

    def listar_productos(self):
        return self.modelo_producto.listar_productos()
    
