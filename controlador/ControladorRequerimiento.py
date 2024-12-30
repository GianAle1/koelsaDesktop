from modelo.Requerimiento import Requerimiento

class ControladorRequerimiento:
    def __init__(self):
        self.modelo_requerimiento = Requerimiento()

    
    def guardar_requerimiento(self, fecha, criterio, productos):
        return self.modelo_requerimiento.guardar_requerimiento(fecha, criterio, productos)
        
    def listar_productos(self):
        return self.modelo_requerimiento.listar_productos()

    def listar_proveedores(self):
        return self.modelo_requerimiento.listar_proveedores()

    def listar_usos(self):
        return self.modelo_requerimiento.listar_usos()

    def listar_almacenes(self):
        return self.modelo_requerimiento.listar_almacenes()
