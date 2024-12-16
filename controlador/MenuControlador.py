# controlador/menu_controlador.py
from controlador.ControladorMarca import ControladorMarca
from controlador.ControladorProveedor import ControladorProveedor
from controlador.ControladorProducto import ControladorProducto
class MenuControlador:
    def __init__(self):
        self.controlador_marca = ControladorMarca()
        self.controlador_proveedor = ControladorProveedor()
        self.controlador_producto = ControladorProducto()
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
    def listar_proveedores(self):
        """Obtener las marcas a través del controlador de marcas"""
        return self.controlador_proveedor.listar_proveedores()  # Delegar la obtención de marcas al controlador de marcas
    def registrar_proveedor(self, nombre,direccion,telefono,correo):
        """Método para registrar una nueva marca"""
        # Delegamos el registro al ControladorMarca
        return self.controlador_proveedor.registrar_proveedor(nombre,direccion,telefono,correo)
     # Función para obtener solo el id y nombre de los proveedores (para el ComboBox)
    def listar_proveedores_combo(self):
        """Obtiene los proveedores solo con el id y nombre (para ComboBox)"""
        proveedores = self.controlador_producto.obtener_proveedores()  # Devuelve todos los proveedores
        return [(proveedor[0], proveedor[1]) for proveedor in proveedores]  # Solo 