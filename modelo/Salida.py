from modelo.conexion import ConexionDB

class Salida:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def guardar_salida(self, fecha, responsable, productos, observaciones):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Insertar en la tabla salida
                query_salida = "INSERT INTO salida (fecha, responsable, observacion) VALUES (%s, %s, %s)"
                cursor.execute(query_salida, (fecha, responsable, observaciones))
                connection.commit()

                # Obtener el idsalida recién generado
                cursor.execute("SELECT LAST_INSERT_ID()")
                idsalida = cursor.fetchone()[0]

                # Insertar en la tabla salidaDetalle y actualizar la cantidad en producto
                query_detalle = "INSERT INTO salidaDetalle (idsalida, idproducto, cantidad, idmaquinaria) VALUES (%s, %s, %s, %s)"
                query_actualizar_producto = "UPDATE producto SET cantidad = cantidad - %s WHERE idproducto = %s"

                for producto in productos:
                    idproducto, cantidad, idmaquinaria = producto  # Asegurarse de que `idproducto` es un entero

                    # Verificar el stock actual
                    cursor.execute("SELECT cantidad FROM producto WHERE idproducto = %s", (idproducto,))
                    resultado = cursor.fetchone()

                    if resultado:
                        stock_actual = resultado[0]

                        if stock_actual < cantidad:
                            print(f"No hay suficiente stock para el producto con ID '{idproducto}'. Stock actual: {stock_actual}")
                            raise ValueError(f"Stock insuficiente para el producto con ID '{idproducto}'")

                        # Insertar en salidaDetalle
                        cursor.execute(query_detalle, (idsalida, idproducto, cantidad, idmaquinaria))

                        # Actualizar el stock del producto
                        cursor.execute(query_actualizar_producto, (cantidad, idproducto))
                    else:
                        print(f"El producto con ID '{idproducto}' no fue encontrado en la base de datos.")
                        continue

                # Confirmar cambios
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

    def listar_maquinarias(self):
        """
        Obtiene todas las maquinarias disponibles de la base de datos.
        """
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT idmaquinaria, tipo, modelo, marca FROM maquinaria"
                cursor.execute(query)
                maquinarias = cursor.fetchall()
                return maquinarias
            except Exception as e:
                print(f"Error al obtener maquinarias: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return []

    def listar_productos(self):
        """
        Obtiene todos los productos disponibles de la base de datos.
        """
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
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return []
    
    def obtener_todas_las_salidas(self):
        connection = self.conexion_db.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                SELECT 
                    p.idproducto,
                    p.partname,
                    p.smcs,
                    p.descripcion,
                    f.nomfamilia,
                    s.fecha,
                    d.cantidad,
                    m.tipo,
                    m.modelo,
                    m.marca
                FROM salidaDetalle d
                JOIN salida s ON s.idsalida = d.idsalida
                JOIN producto p ON p.idproducto = d.idproducto
                LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                LEFT JOIN maquinaria m ON m.idmaquinaria = d.idmaquinaria;
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
                        p.idproducto,
                        p.partname,
                        p.smcs,
                        p.descripcion,
                        f.nomfamilia,
                        s.fecha,
                        d.cantidad,
                        m.tipo,
                        m.modelo,
                        m.marca
                    FROM salidaDetalle d
                    JOIN salida s ON s.idsalida = d.idsalida
                    JOIN producto p ON p.idproducto = d.idproducto
                    LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                    LEFT JOIN maquinaria m ON m.idmaquinaria = d.idmaquinaria
                    WHERE p.idproducto = %s;
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
