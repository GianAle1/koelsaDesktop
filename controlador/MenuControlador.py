# controlador/menu_controlador.py
from controlador.ControladorMarca import ControladorMarca
from controlador.ControladorProveedor import ControladorProveedor
from controlador.ControladorProducto import ControladorProducto
from controlador.ControladorAlmacen import ControladorAlmacen
from controlador.ControladorUso import ControladorUso
from controlador.ControladorUnidadMedida import ControladorUnidadMedida
from controlador.ControladorEquipo import ControladorEquipo
from controlador.ControladorFamilia import ControladorFamilia
class MenuControlador:
    def __init__(self):
        self.controlador_marca = ControladorMarca()
        self.controlador_proveedor = ControladorProveedor()
        self.controlador_producto = ControladorProducto()
        self.controlador_almacen = ControladorAlmacen()
        self.controlador_uso = ControladorUso()
        self.controlador_unidadMedidas = ControladorUnidadMedida()
        self.controlador_equipo = ControladorEquipo()
        self.controlador_familia = ControladorFamilia()

    def registrar_marca(self, nombre_marca):
        return self.controlador_marca.registrar_marca(nombre_marca)

    def eliminar_marca(self, marca_id):
        return self.controlador_marca.eliminar_marca(marca_id)
    
    def listar_marcas(self):
        return self.controlador_marca.listar_marcas() 
    
    def listar_proveedores(self):
        return self.controlador_proveedor.listar_proveedores() 
    
    def registrar_proveedor(self, nombre,direccion,telefono,correo):
        return self.controlador_proveedor.registrar_proveedor(nombre,direccion,telefono,correo)
    
    def listar_proveedores_combo(self):
        """Obtiene los proveedores solo con el id y nombre (para ComboBox)"""
        proveedores = self.controlador_producto.obtener_proveedores()  
        return [(proveedor[0], proveedor[1]) for proveedor in proveedores] 
    
    def listar_almacenes(self):
        return self.controlador_almacen.listar_almacenes() 
    
    def listar_usos(self):
        return self.controlador_uso.listar_usos() 
    
    def listar_unidadMedidas(self):
        return self.controlador_unidadMedidas.listar_unidadMedidas()
    
    def listar_equipos(self):
        return self.controlador_equipo.listar_equipos() 
    def listar_familias(self):
        return self.controlador_familia.listar_familias() 
    

    def registrar_producto(self, nombre, descripcion, cantidad, precio, proveedor_id, marca_id, almacen_id, und_medida, uso, equipo,familia):
        if not nombre or not descripcion or not cantidad or not precio:
            return False  
        exito = self.controlador_producto.registrar_producto(nombre, descripcion, cantidad, precio, proveedor_id, marca_id, almacen_id, und_medida, uso, equipo,familia)
        return exito
    
    