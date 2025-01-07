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
                query_requerimiento = "INSERT INTO Requerimiento (fechaRequerimiento, criterio) VALUES (%s, %s)"
                cursor.execute(query_requerimiento, (fecha, criterio))
                connection.commit()

                cursor.execute("SELECT LAST_INSERT_ID()")
                id_requerimiento = cursor.fetchone()[0]

                # Insertar los detalles del requerimiento
                query_detalle = """
                    INSERT INTO requerimientoDetalle (
                        idrequerimiento, idproducto, cantidad, idproveedor, iduso, idalmacen, idmaquinaria, precioUnitario, precioTotal
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            try:
                cursor = connection.cursor()
                query = """
                    SELECT
                        r.idrequerimiento AS ID,
                        r.fechaRequerimiento AS Fecha,
                        r.criterio AS Criterio,
                        COUNT(rd.idproducto) AS Productos,
                        SUM(rd.precioTotal) AS Total
                    FROM Requerimiento r
                    LEFT JOIN requerimientoDetalle rd ON r.idrequerimiento = rd.idrequerimiento
                    GROUP BY r.idrequerimiento, r.fechaRequerimiento, r.criterio
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar requerimientos: {e}")
                return []
            #finally:
                #cursor.close()  # Cierra el cursor
                #connection.close()  # Cierra la conexión
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []

        
    def obtener_detalle_requerimiento(self, id_requerimiento):
        connection = self.conexion_db.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT

                        p.descripcion AS Descripción,
                        rd.cantidad AS Cantidad,
                        rd.precioUnitario AS PrecioUnitario,
                        rd.precioTotal AS PrecioTotal,
                        u.nomUso AS Uso,
                        pr.nombre AS Proveedor,
                        m.Modelo AS Maquinaria,
                        a.nombre AS Almacén
                    FROM requerimientoDetalle rd
                    LEFT JOIN producto p ON rd.idproducto = p.idproducto
                    LEFT JOIN uso u ON rd.iduso = u.iduso
                    LEFT JOIN proveedor pr ON rd.idproveedor = pr.idproveedor
                    LEFT JOIN maquinaria m ON rd.idmaquinaria = m.idmaquinaria
                    LEFT JOIN almacen a ON rd.idalmacen = a.idalmacen
                    WHERE rd.idrequerimiento = %s;
                """
                cursor.execute(query, (id_requerimiento,))
                resultado = cursor.fetchall()
                return resultado
            except Exception as e:
                print(f"Error al obtener detalle del requerimiento: {e}")
                return []
            finally:
                if connection:
                    connection.close()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []

    def actualizar_detalle_requerimiento(self, id_detalle, cantidad, id_proveedor, precio_unitario):
        connection = self.conexion_db.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                precio_total = cantidad * precio_unitario
                query = """
                    UPDATE requerimientoDetalle
                    SET 
                        cantidad = %s,
                        idproveedor = %s,
                        precioUnitario = %s,
                        precioTotal = %s
                    WHERE idrequerimientoDetalle = %s
                """
                parametros = (cantidad, id_proveedor, precio_unitario, precio_total, id_detalle)
                cursor.execute(query, parametros)
                connection.commit()
                return True
            except Exception as e:
                print(f"Error al actualizar detalle: {e}")
                return False
            finally:
                if connection:
                    connection.close()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False
