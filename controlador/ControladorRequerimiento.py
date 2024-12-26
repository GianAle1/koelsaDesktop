from modelo.Requerimiento import Requerimiento

class ControladorRequerimiento:
    def __init__(self):
        self.modelo_requerimiento = Requerimiento()

    def guardar_requerimiento(self, fecha, criterio, productos):
        try:
            id_requerimiento = self.modelo_requerimiento.registrar_requerimiento(fecha, criterio, productos)
            if not id_requerimiento:
                print("Error: No se pudo registrar el requerimiento principal.")
                return False

            print(f"Requerimiento registrado con ID: {id_requerimiento}")
            return True
        except Exception as e:
            print(f"Error en guardar_requerimiento: {e}")
            return False


        
    def listar_productos(self):
        return self.modelo_requerimiento.listar_productos()

    def listar_proveedores(self):
        return self.modelo_requerimiento.listar_proveedores()

    def listar_usos(self):
        return self.modelo_requerimiento.listar_usos()

    def listar_almacenes(self):
        return self.modelo_requerimiento.listar_almacenes()
