from modelo.conexion import ConexionDB

class Requerimiento:
    def __init__(self):
        self.conexion_db = ConexionDB()

    
    def guardar_requerimiento(self, fecha, criterio, productos):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Insertar en la tabla Requerimiento
                query_requerimiento = "INSERT INTO Requerimiento (fechaRequerimiento, critero) VALUES (?, ?)"
                cursor.execute(query_requerimiento, (fecha, criterio))
                connection.commit()

                # Obtener el ID del requerimiento recién generado
                id_requerimiento = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

                # Insertar los detalles del requerimiento
                query_detalle = """
                    INSERT INTO requerimientoDetalle (
                        idrequerimiento, idproducto, cantidad, idproveedor, iduso, idalmacen, idmaquinaria, precioUnitario, precioTotal
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                for producto in productos:
                    cursor.execute(query_detalle, (
                        id_requerimiento,
                        producto["id_producto"],
                        producto["cantidad"],
                        producto["id_proveedor"],
                        producto["id_uso"],
                        producto["id_almacen"],
                        producto["id_maquinaria"],
                        producto["precio_unitario"],
                        producto["precio_total"]
                    ))
                connection.commit()
                return id_requerimiento
            except Exception as e:
                print(f"Error al guardar el requerimiento: {e}")
                connection.rollback()
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
                cursor.execute("SELECT idproducto, descripcion FROM producto")
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
                cursor.execute("SELECT idproveedor, nombre FROM proveedor")
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
                cursor.execute("SELECT iduso, descripcion FROM uso")
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
                cursor.execute("SELECT idalmacen, nombre FROM almacen")
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar almacenes: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []

    def listar_maquinarias(self):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                cursor.execute("SELECT idmaquinaria, descripcion FROM maquinaria")
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar maquinarias: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []
        
    def listar_requerimientos(self):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = """
                    SELECT
                        r.idrequerimiento AS ID,
                        r.fechaRequerimiento AS Fecha,
                        r.critero AS Criterio,
                        COUNT(rd.idproducto) AS Productos,
                        SUM(rd.precioTotal) AS Total
                    FROM Requerimiento r
                    LEFT JOIN requerimientoDetalle rd ON r.idrequerimiento = rd.idrequerimiento
                    GROUP BY r.idrequerimiento, r.fechaRequerimiento, r.critero
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar requerimientos: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []
