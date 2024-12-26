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
                query_salida = "INSERT INTO salida (fecha, responsable, observacion) VALUES (?, ?, ?)"
                cursor.execute(query_salida, (fecha, responsable, observaciones))
                connection.commit()

                # Obtener el idsalida recién generado
                idsalida = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

                # Insertar en la tabla salidaDetalle
                query_detalle = "INSERT INTO salidaDetalle (idsalida, idproducto, cantidad, idmaquinaria) VALUES (?, ?, ?, ?)"
                for producto in productos:
                    producto_seleccionado, cantidad, idmaquinaria = producto
                    cursor.execute("SELECT idproducto FROM producto WHERE descripcion = ?", (producto_seleccionado,))
                    idproducto = cursor.fetchone()[0]
                    cursor.execute(query_detalle, (idsalida, idproducto, cantidad, idmaquinaria))

                # Confirmar cambios
                connection.commit()
                return idsalida
            except Exception as e:
                print(f"Error al guardar la salida: {e}")
                connection.rollback()
                return None
            finally:
                self.conexion_db.cerrar_conexion()

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
    
    def obtener_salidas_por_producto(self, producto_id):
        """Consulta las salidas asociadas a un producto específico."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT s.fecha, sd.cantidad, m.tipo, m.modelo, m.marca
                FROM salidaDetalle sd
                JOIN salida s ON s.idsalida = sd.idsalida
                JOIN maquinaria m ON m.idmaquinaria = sd.idmaquinaria
                WHERE sd.idproducto = ?
                """
                cursor.execute(query, (producto_id,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error obteniendo salidas del producto: {e}")
                return []
            #finally:
                #self.conexion_db.cerrar_conexion()
