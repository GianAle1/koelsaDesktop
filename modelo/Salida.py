from modelo.conexion import ConexionDB

class Salida:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def guardar_salida(self, fecha, idresponsable, idproyecto, productos, observaciones):
        """Guarda una salida de productos en la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Insertar en la tabla salida con idproyecto
                query_salida = """
                    INSERT INTO salida (fecha, idresponsable, idproyecto, observacion) 
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query_salida, (fecha, idresponsable, idproyecto, observaciones))
                connection.commit()

                # Obtener el idsalida recién generado
                cursor.execute("SELECT LAST_INSERT_ID()")
                idsalida = cursor.fetchone()[0]

                # Insertar en la tabla salidaDetalle y actualizar la cantidad en producto
                query_detalle = """
                    INSERT INTO salidaDetalle (idsalida, idproducto, cantidad, idmaquinaria) 
                    VALUES (%s, %s, %s, %s)
                """
                query_actualizar_producto = """
                    UPDATE producto SET cantidad = cantidad - %s WHERE idproducto = %s
                """

                for producto in productos:
                    idproducto, cantidad, idmaquinaria = producto

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
                cursor.close()
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
