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
                cursor.execute("SELECT LAST_INSERT_ID()")  # Para MySQL
                identrada = cursor.fetchone()[0]

                # Consultas SQL
                query_detalle = """
                    INSERT INTO entradaDetalle (identrada, idproducto, cantidad, idproveedor, precioEntrada) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                query_actualizar_producto = """
                    UPDATE producto 
                    SET 
                        precio = ((precio * cantidad) + (%s * %s)) / (cantidad + %s),
                        cantidad = cantidad + %s
                    WHERE idproducto = %s
                """

                for producto in productos:
                    # Validaciones y extracción de datos
                    if not isinstance(producto[0], int):
                        raise ValueError(f"El ID del producto no es válido: {producto[0]}")
                    if not isinstance(producto[2], (int, float)) or producto[2] <= 0:
                        raise ValueError(f"La cantidad debe ser un número positivo: {producto[2]}")
                    if not isinstance(producto[3], (int, float, Decimal)) or producto[3] <= 0:
                        raise ValueError(f"El precio debe ser un número positivo: {producto[3]}")
                    if not isinstance(producto[4], int):
                        raise ValueError(f"El ID del proveedor no es válido: {producto[4]}")

                    idproducto = producto[0]  # ID del producto
                    cantidad = int(producto[2])  # Cantidad ingresada
                    precio_nuevo = Decimal(str(producto[3]))  # Convertir a Decimal
                    idproveedor = producto[4]  # ID del proveedor

                    # Validación adicional de datos
                    print(f"Procesando producto - ID: {idproducto}, Cantidad: {cantidad}, Precio: {precio_nuevo}, Proveedor: {idproveedor}")

                    # Insertar en entradaDetalle (✅ Corregido: precio_nuevo es el precioEntrada)
                    cursor.execute(query_detalle, (identrada, idproducto, cantidad, idproveedor, precio_nuevo))

                    # Actualizar la cantidad y calcular el nuevo precio promedio
                    cursor.execute(query_actualizar_producto, (precio_nuevo, cantidad, cantidad, cantidad, idproducto))

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
        connection = self.conexion_db.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT 
                        p.idproducto,
                        p.partname,
                        p.codigoInterno,
                        p.descripcion,
                        d.precioDetalle,
                        f.nomfamilia,
                        e.fecha,
                        d.cantidad
                    FROM entradaDetalle d
                    JOIN entrada e ON e.identrada = d.identrada
                    JOIN producto p ON p.idproducto = d.idproducto
                    LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                    WHERE p.idproducto = %s;
                """
                cursor.execute(query, (producto_id,))
                entradas = cursor.fetchall()
                return entradas
            except Exception as e:
                print(f"Error al obtener entradas para el producto {producto_id}: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo conectar a la base de datos.")
            return []

    def obtener_todas_las_entradas(self):
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
                    d.precioEntrada,
                    f.nomfamilia AS Familia,
                    e.fecha AS Fecha_Entrada,
                    d.cantidad AS Cantidad,
                    prov.nombre AS Proveedor
                FROM entradaDetalle d
                JOIN entrada e ON e.identrada = d.identrada
                JOIN producto p ON p.idproducto = d.idproducto
                LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                LEFT JOIN proveedor prov ON d.idproveedor = prov.idproveedor;

                """
                cursor.execute(query)
                entradas = cursor.fetchall()
                return entradas
            except Exception as e:
                print(f"Error al obtener todas las entradas: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo conectar a la base de datos.")
            return []
