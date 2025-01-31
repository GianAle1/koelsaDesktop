from controlador.ControladorMarca import ControladorMarca
from controlador.ControladorProveedor import ControladorProveedor
from controlador.ControladorProducto import ControladorProducto
from controlador.ControladorAlmacen import ControladorAlmacen
from controlador.ControladorUso import ControladorUso
from controlador.ControladorUnidadMedida import ControladorUnidadMedida
from controlador.ControladorEquipo import ControladorEquipo
from controlador.ControladorFamilia import ControladorFamilia
from controlador.ControladorEntrada import ControladorEntrada
from controlador.ControladorMaquinaria import ControladorMaquinaria
from controlador.ControladorSalida import ControladorSalida
from controlador.ControladorRequerimiento import ControladorRequerimiento
from controlador.ControladorBacklog import ControladorBacklog
from controlador.ControladorResponsable import ControladorResponsable
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
        self.controlador_entrada = ControladorEntrada()
        self.controlador_maquinaria = ControladorMaquinaria()
        self.controlador_salida = ControladorSalida()
        self.controlador_requerimiento = ControladorRequerimiento()
        self.controlador_backlog = ControladorBacklog()
        self.controlador_responsable = ControladorResponsable()
    def registrar_marca(self, nombre_marca):
        return self.controlador_marca.registrar_marca(nombre_marca)

    def eliminar_marca(self, marca_id):
        return self.controlador_marca.eliminar_marca(marca_id)
    
    def listar_marcas(self):
        return self.controlador_marca.listar_marcas() 
    
    def listar_proveedores(self):
        return self.controlador_proveedor.listar_proveedores() 
    
    def registrar_proveedor(self, nombre,direccion,telefono,correo,ruc):
        return self.controlador_proveedor.registrar_proveedor(nombre,direccion,telefono,correo,ruc)
    
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

    def registrar_producto(self, nombre, descripcion, cantidad, precio, smcs, sap, marca_id, almacen_id, und_medida, familia):
        if not nombre or not descripcion or not cantidad or not precio:
            return False
        exito = self.controlador_producto.registrar_producto(
            nombre, descripcion, cantidad, precio, smcs, sap, marca_id, almacen_id, und_medida, familia
        )
        return exito
    
    def listar_productos(self):
        return self.controlador_producto.listar_productos() 
    
    def listar_productos_por_familia(self, familia):
        return self.controlador_producto.listar_productos_por_familia(familia)
    
    def guardar_entrada(self, fecha, docu_ingreso, productos):
        return self.controlador_entrada.guardar_entrada(fecha, docu_ingreso, productos)

    
    def listar_maquinarias(self):
        """Obtiene la lista de maquinarias del modelo."""
        return self.controlador_maquinaria.listar_maquinarias()
    
    def guardar_salida(self, fecha, id_responsable, id_proyecto, productos, observaciones):
        """Llama al controlador de salida para registrar la salida."""
        return self.controlador_salida.guardar_salida(fecha, id_responsable, id_proyecto, productos, observaciones)


    
    def obtener_historial_producto(self, producto_id):
        """Obtiene el historial de entradas y salidas para un producto específico."""
        entradas = self.controlador_entrada.obtener_entradas_por_producto(producto_id)
        salidas = self.controlador_salida.obtener_salidas_por_producto(producto_id)
        return {"entradas": entradas, "salidas": salidas}
    
    def listar_subalmacenes(self, almacen_id):
        """Obtiene los subalmacenes asociados a un almacén específico."""
        return self.controlador_almacen.listar_subalmacenes(almacen_id)
    
    def guardar_requerimiento(self, fecha, criterio, productos):
        return self.controlador_requerimiento.guardar_requerimiento(fecha, criterio, productos)
    
    def listar_requerimientos(self):
        return self.controlador_requerimiento.listar_requerimientos()
    
    def obtener_detalle_requerimiento(self, id_requerimiento):
        """Llama al modelo para obtener los detalles del requerimiento."""
        return self.controlador_requerimiento.obtener_detalle_requerimiento(id_requerimiento)
    
    def listar_backlogs(self):
        return self.controlador_backlog.listar_backlogs()

    def guardar_backlog(self, backlog_data, detalles_temporales):
        return self.controlador_backlog.guardar_backlog(backlog_data, detalles_temporales)
    

    def obtener_historial_general(self):
        """
        Devuelve un diccionario con todas las entradas y salidas de todos los productos.
        """
        try:
            entradas = self.controlador_entrada.obtener_todas_las_entradas()
            salidas = self.controlador_salida.obtener_todas_las_salidas()
            return {"entradas": entradas, "salidas": salidas}
        except Exception as e:
            print(f"Error al obtener el historial general: {e}")
            return {"entradas": [], "salidas": []}

    def registrar_familia(self, nombre_familia):
        """Registra una nueva familia en la base de datos"""
        return self.controlador_familia.registrar_familia(nombre_familia)

    def eliminar_familia(self, idfamilia):
        """Elimina una familia de la base de datos"""
        return self.controlador_familia.eliminar_familia(idfamilia)

    def listar_responsables(self):
        return self.controlador_responsable.listar_responsables()

    def listar_proyectos(self):
        return self.controlador_salida.listar_proyectos()
    
    def eliminar_proveedor(self, id_proveedor):
        return self.controlador_proveedor.eliminar_proveedor(id_proveedor)
