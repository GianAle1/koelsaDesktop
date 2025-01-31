# controlador/ControladorProveedor.py
from modelo.Proveedor import Proveedor

class ControladorProveedor:
    def __init__(self):
        self.modelo_proveedor = Proveedor()

    def registrar_proveedor(self, nombre, direccion, telefono, correo,ruc):
        """Método para registrar una nueva proveedor usando el modelo"""
        exito = self.modelo_proveedor.registrar_proveedor(nombre,direccion,telefono,correo,ruc)
        if exito:
            return self.listar_proveedores()  # Solo retornamos las marcas si la inserción fue exitosa
        else:
            return None  # En caso de error, retornamos None

    def eliminar_proveedor(self, id_proveedor):
        """Elimina un proveedor por su ID"""
        return self.modelo_proveedor.eliminar_proveedor(id_proveedor)

    def listar_proveedores(self):
        """Obtiene las marcas del modelo y las pasa a la vista"""
        return self.modelo_proveedor.listar_proveedores()
    
