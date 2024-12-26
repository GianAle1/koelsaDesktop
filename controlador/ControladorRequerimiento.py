from modelo.Requerimiento import Requerimiento

class ControladorRequerimiento:
    def __init__(self):
        self.modelo_requerimiento = Requerimiento()

    def guardar_requerimiento(self, fecha, criterio, productos):
        try:
            id_requerimiento = self.modelo_requerimiento.registrar_requerimiento(fecha, criterio)
            if not id_requerimiento:
                print("Error: No se pudo registrar el requerimiento principal.")
                return False

            print(f"Requerimiento registrado con ID: {id_requerimiento}")  # Log adicional

            for producto in productos:
                id_producto = producto["id_producto"]
                cantidad = producto["cantidad"]
                id_proveedor = producto["id_proveedor"]
                id_uso = producto["id_uso"]
                id_almacen = producto["id_almacen"]
                precio_unitario = producto["precio_unitario"]
                precio_total = producto["precio_total"]

                detalle_registrado = self.modelo_requerimiento.registrar_requerimiento_detalle(
                    id_requerimiento, id_producto, cantidad, id_proveedor, id_uso, id_almacen, precio_unitario, precio_total
                )
                if not detalle_registrado:
                    print(f"Error al registrar el detalle del producto ID: {id_producto}")
                    return False
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
