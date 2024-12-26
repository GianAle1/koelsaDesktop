from modelo.conexion import ConexionDB

class Requerimiento:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def registrar_requerimiento(self, fecha, criterio, productos):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Insertar en la tabla Requerimiento
                query_requerimiento = "INSERT INTO Requerimiento (fechaRequerimiento, critero, total) VALUES (?, ?, ?)"
                cursor.execute(query_requerimiento, (fecha, criterio, 0.0))
                connection.commit()

                # Obtener el último ID generado
                id_requerimiento = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
                print(f"Requerimiento registrado con ID: {id_requerimiento}")

                # Insertar los detalles
                query_detalle = """
                    INSERT INTO requerimientoDetalle (
                        idrequerimiento, idproducto, cantidad, idproveedor, iduso, idalmacen, precioUnitario, precioTotal
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                for producto in productos:
                    cursor.execute(query_detalle, (
                        id_requerimiento,
                        producto["id_producto"],
                        producto["cantidad"],
                        producto["id_proveedor"],
                        producto["id_uso"],
                        producto["id_almacen"],
                        producto["precio_unitario"],
                        producto["precio_total"]
                    ))

                # Confirmar todos los cambios
                connection.commit()
                return id_requerimiento
            except Exception as e:
                print(f"Error al registrar el requerimiento: {e}")
                connection.rollback()  # Revertir la transacción si ocurre un error
                return None
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return None

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
