from modelo.conexion import ConexionDB

class Entrada:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def guardar_entrada(self, fecha, productos):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Insertar en la tabla entrada
                query_entrada = "INSERT INTO entrada (fecha) VALUES (?)"
                cursor.execute(query_entrada, (fecha,))
                connection.commit()

                # Obtener el identrada recién generado
                identrada = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

                # Insertar en la tabla entradaDetalle
                query_detalle = "INSERT INTO entradaDetalle (identrada, idproducto, cantidad) VALUES (?, ?, ?)"
                for producto in productos:
                    # Obtener el idproducto basado en la descripción del producto
                    cursor.execute("SELECT idproducto FROM producto WHERE descripcion = ?", (producto[0],))
                    result = cursor.fetchone()
                    if result:
                        idproducto = result[0]  # Extraer el ID del resultado
                        cursor.execute(query_detalle, (identrada, idproducto, producto[1]))
                    else:
                        print(f"Producto no encontrado: {producto[0]}")
                        continue

                # Confirmar todos los cambios
                connection.commit()
                print("Entrada guardada exitosamente.")
                return True
            except Exception as e:
                print(f"Error al guardar la entrada: {e}")
                connection.rollback()
                return False
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return False
