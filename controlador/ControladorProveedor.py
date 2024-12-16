# controlador/ControladorProveedor.py
from modelo.Proveedor import Proveedor

class ControladorProveedor:
    def __init__(self, conexion_db):
        self.modelo_proveedor = Proveedor(conexion_db)

    def registrar_proveedor(self, nombre, direccion, telefono, correo):
        """Registra un nuevo proveedor a través del modelo."""
        return self.modelo_proveedor.registrar_proveedor(nombre, direccion, telefono, correo)

    def eliminar_proveedor(self, id_proveedor):
        """Elimina un proveedor a través del modelo."""
        return self.modelo_proveedor.eliminar_proveedor(id_proveedor)

    def obtener_proveedores(self):
        """Obtiene la lista de proveedores a través del modelo."""
        return self.modelo_proveedor.obtener_proveedores()
