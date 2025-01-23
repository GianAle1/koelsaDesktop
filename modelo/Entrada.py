from modelo.conexion import ConexionDB
from decimal import Decimal

class Entrada:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def guardar_entrada(self, fecha, productos):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Insertar en la tabla entrada
                query_entrada = "INSERT INTO entrada (fecha) VALUES (%s)"
                cursor.execute(query_entrada, (fecha,))
                connection.commit()

                # Obtener el identrada recién generado
                cursor.execute("SELECT LAST_INSERT_ID()")  # Cambiado para MySQL
                identrada = cursor.fetchone()[0]

                # Insertar en la tabla entradaDetalle y actualizar la cantidad en producto
                query_detalle = "INSERT INTO entradaDetalle (identrada, idproducto, cantidad) VALUES (%s, %s, %s)"
                query_actualizar_producto = """
                    UPDATE producto 
                    SET cantidad = cantidad + %s, 
                        precio = ((precio * cantidad) + (%s * %s)) / (cantidad + %s)
                    WHERE idproducto = %s
                """

                for producto in productos:
                    idproducto = producto[0]  # ID del producto
                    cantidad = int(producto[1])  # Cantidad ingresada
                    precio_nuevo = Decimal(producto[2])  # Convertir el precio a Decimal

                    # Validar que cantidad y precio sean positivos
                    if cantidad <= 0 or precio_nuevo <= 0:
                        raise ValueError("La cantidad y el precio deben ser mayores a 0.")

                    # Insertar en entradaDetalle
                    cursor.execute(query_detalle, (identrada, idproducto, cantidad))

                    # Actualizar la cantidad y calcular el nuevo precio promedio
                    cursor.execute(query_actualizar_producto, (cantidad, precio_nuevo, cantidad, cantidad, idproducto))

                # Confirmar todos los cambios
                connection.commit()
                print("Entrada guardada exitosamente.")
                return identrada  # Retorna el ID de la entrada creada
            except Exception as e:
                print(f"Error al guardar la entrada: {e}")
                connection.rollback()
                return None
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return None

    def obtener_entradas_por_producto(self, producto_id):
        """Consulta las entradas asociadas a un producto específico."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT e.fecha, d.cantidad
                FROM entradaDetalle d
                JOIN entrada e ON e.identrada = d.identrada
                WHERE d.idproducto = %s
                """
                cursor.execute(query, (producto_id,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error obteniendo entradas del producto: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
    