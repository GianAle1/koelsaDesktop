from modelo.conexion import ConexionDB

class Salida:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def guardar_salida(self, idmaquinaria, fecha, responsable, productos):
        """
        Guarda una salida junto con sus detalles y actualiza el inventario de productos.
        """
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Insertar en la tabla salida
                query_salida = """
                INSERT INTO salida (idmaquinaria, fecha, responsable)
                VALUES (?, ?, ?)
                """
                cursor.execute(query_salida, (idmaquinaria, fecha, responsable))
                connection.commit()

                # Obtener el idsalida recién generado
                idsalida = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

                # Insertar en la tabla salidaDetalle y actualizar la cantidad en producto
                query_detalle = """
                INSERT INTO salidaDetalle (idsalida, idproducto, cantidad)
                VALUES (?, ?, ?)
                """
                query_actualizar_producto = """
                UPDATE producto
                SET cantidad = cantidad - ?
                WHERE idproducto = ?
                """

                for producto in productos:
                    # Obtener el idproducto basado en la descripción del producto
                    cursor.execute("SELECT idproducto FROM producto WHERE descripcion = ?", (producto[0],))
                    result = cursor.fetchone()
                    if result:
                        idproducto = result[0]  # Extraer el ID del producto

                        # Insertar en salidaDetalle
                        cursor.execute(query_detalle, (idsalida, idproducto, producto[1]))

                        # Actualizar la cantidad en la tabla producto
                        cursor.execute(query_actualizar_producto, (producto[1], idproducto))
                    else:
                        print(f"Producto no encontrado: {producto[0]}")
                        continue

                # Confirmar todos los cambios
                connection.commit()
                print("Salida registrada exitosamente.")
                return idsalida
            except Exception as e:
                print(f"Error al guardar la salida: {e}")
                connection.rollback()
                return False
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return False

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
