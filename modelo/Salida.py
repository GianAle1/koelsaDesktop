from modelo.conexion import ConexionDB

class Salida:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def guardar_salida(self, fecha, id_responsable, id_proyecto, productos, observaciones):
        """Guarda una nueva salida en la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Insertar en la tabla salida
                query_salida = "INSERT INTO salida (fecha, idresponsable, idproyecto, observacion) VALUES (%s, %s, %s, %s)"
                cursor.execute(query_salida, (fecha, id_responsable, id_proyecto, observaciones))
                connection.commit()

                # Obtener el ID de la salida recién creada
                cursor.execute("SELECT LAST_INSERT_ID()")
                idsalida = cursor.fetchone()[0]

                # Insertar los productos en salidaDetalle
                query_detalle = "INSERT INTO salidaDetalle (idsalida, idproducto, cantidad, idmaquinaria) VALUES (%s, %s, %s, %s)"
                query_actualizar_producto = "UPDATE producto SET cantidad = cantidad - %s WHERE idproducto = %s"

                for producto in productos:
                    if len(producto) != 3:
                        print(f"Error en el formato del producto: {producto}")
                        continue  # Saltar el producto si no tiene el formato correcto

                    idproducto, cantidad, idmaquinaria = producto
                    
                    # Verificar stock actual
                    cursor.execute("SELECT cantidad FROM producto WHERE idproducto = %s", (idproducto,))
                    resultado = cursor.fetchone()

                    if resultado:
                        stock_actual = resultado[0]

                        if stock_actual < cantidad:
                            raise ValueError(f"Stock insuficiente para el producto con ID {idproducto}. Disponible: {stock_actual}")

                        # Insertar en salidaDetalle
                        cursor.execute(query_detalle, (idsalida, idproducto, cantidad, idmaquinaria))

                        # Actualizar stock del producto
                        cursor.execute(query_actualizar_producto, (cantidad, idproducto))

                # Confirmar cambios en la base de datos
                connection.commit()
                return idsalida

            except Exception as e:
                print(f"Error al guardar la salida: {e}")
                connection.rollback()
                return None

            finally:
                self.conexion_db.cerrar_conexion()

        else:
            print("No se pudo establecer conexión con la base de datos.")
            return None

    def listar_proyectos(self):
        """Obtiene la lista de proyectos desde la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT idproyecto, nombre, ubicacion FROM proyecto"
                cursor.execute(query)
                proyectos = cursor.fetchall()
                return proyectos
            except Exception as e:
                print(f"Error al obtener proyectos: {e}")
                return []
            finally:
                cursor.close()
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return []

    def listar_maquinarias(self):
        """Obtiene todas las maquinarias disponibles de la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT idmaquinaria, modelo, serie FROM maquinaria"
                cursor.execute(query)
                maquinarias = cursor.fetchall()
                return maquinarias
            except Exception as e:
                print(f"Error al obtener maquinarias: {e}")
                return []
            finally:
                cursor.close()
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return []

    def listar_productos(self):
        """Obtiene todos los productos disponibles de la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT idproducto, descripcion, cantidad FROM producto"
                cursor.execute(query)
                productos = cursor.fetchall()
                return productos
            except Exception as e:
                print(f"Error al obtener productos: {e}")
                return []
            finally:
                cursor.close()
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return []



    def obtener_todas_las_salidas(self):
        """Obtiene todas las salidas de productos, ordenadas por fecha de mayor a menor."""
        connection = self.conexion_db.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT 
                        p.idproducto AS ID_Producto,
                        p.partname AS Nombre_Producto,
                        p.codigoInterno AS Codigo_Interno,
                        p.descripcion AS Descripcion,
                        p.precio AS Precio,
                        f.nomfamilia AS Familia,
                        s.fecha AS Fecha_Salida,  
                        d.cantidad AS Cantidad,
                        'Salida' AS Tipo,
                        COALESCE(m.serie, 'N/A') AS Maquinaria_Serie,
                        COALESCE(m.marca, 'N/A') AS Marca,
                        r.nombre AS Responsable  
                    FROM salidaDetalle d
                    JOIN salida s ON s.idsalida = d.idsalida
                    JOIN producto p ON p.idproducto = d.idproducto
                    LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                    LEFT JOIN maquinaria m ON d.idmaquinaria = m.idmaquinaria
                    LEFT JOIN responsable r ON s.idresponsable = r.idresponsable
                    ORDER BY s.fecha DESC;  --  Ordenado de mayor a menor fecha
                """
                cursor.execute(query)
                salidas = cursor.fetchall()
                return salidas
            except Exception as e:
                print(f"Error al obtener todas las salidas: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo conectar a la base de datos.")
            return []

    def obtener_salidas_por_producto(self, producto_id):
        connection = self.conexion_db.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT 
                        p.idproducto AS ID_Producto,
                        p.partname AS Nombre_Producto,
                        p.codigoInterno AS Codigo_Interno,
                        p.descripcion AS Descripcion,
                        p.precio AS Precio,
                        f.nomfamilia AS Familia,
                        s.fecha AS Fecha_Salida,  
                        d.cantidad AS Cantidad,
                        'Salida' AS Tipo,
                        COALESCE(m.serie, 'N/A') AS Maquinaria_Serie,
                        COALESCE(m.marca, 'N/A') AS Marca,
                        r.nombre AS Responsable  
                    FROM salidaDetalle d
                    JOIN salida s ON s.idsalida = d.idsalida
                    JOIN producto p ON p.idproducto = d.idproducto
                    LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                    LEFT JOIN maquinaria m ON d.idmaquinaria = m.idmaquinaria
                    LEFT JOIN responsable r ON s.idresponsable = r.idresponsable
                    WHERE p.idproducto = %s  -- 🔹 Filtramos por el ID del producto
                    ORDER BY s.fecha DESC;
                """
                cursor.execute(query, (producto_id,))
                salidas = cursor.fetchall()
                return salidas
            except Exception as e:
                print(f"Error al obtener salidas para el producto {producto_id}: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo conectar a la base de datos.")
            return []
