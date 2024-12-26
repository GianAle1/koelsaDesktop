from modelo.conexion import ConexionDB

class Requerimiento:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def registrar_requerimiento(self, fecha, criterio):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Usa OUTPUT para obtener el ID insertado
                query = """
                    INSERT INTO Requerimiento (fechaRequerimiento, critero, total)
                    OUTPUT INSERTED.idrequerimiento
                    VALUES (?, ?, ?)
                """
                cursor.execute(query, (fecha, criterio, 0.0))
                id_requerimiento = cursor.fetchone()[0]  # Recupera el ID directamente

                print(f"Requerimiento registrado con ID: {id_requerimiento}")  # Debug adicional

                connection.commit()
                return id_requerimiento
            except Exception as e:
                print(f"Error al registrar el requerimiento: {e}")
                connection.rollback()
                return None
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return None



    def registrar_requerimiento_detalle(self, id_requerimiento, id_producto, cantidad, id_proveedor, id_uso, id_almacen, precio_unitario, precio_total):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = """
                    INSERT INTO requerimientoDetalle (
                        idrequerimiento, idproducto, cantidad, idproveedor, iduso, idalmacen, precioUnitario, precioTotal
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query, (id_requerimiento, id_producto, cantidad, id_proveedor, id_uso, id_almacen, precio_unitario, precio_total))
                print(f"Detalle registrado para ID Requerimiento: {id_requerimiento}, Producto: {id_producto}")  # Debug adicional
                connection.commit()
                return True
            except Exception as e:
                print(f"Error al registrar el detalle del requerimiento: {e}")  # Log de error
                connection.rollback()
                return False
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False
    def listar_productos(self):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT idproducto, descripcion FROM producto"
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar productos: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []

    def listar_proveedores(self):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT idproveedor, nombre FROM proveedor"
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar proveedores: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []

    def listar_usos(self):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT iduso, descripcion FROM uso"
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar usos: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []

    def listar_almacenes(self):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT idalmacen, nombre FROM almacen"
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar almacenes: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []
