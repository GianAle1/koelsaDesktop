from modelo.conexion import ConexionDB
from decimal import Decimal

class Entrada:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def guardar_entrada(self, fecha, docu_ingreso, productos):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Insertar en la tabla entrada con el nuevo campo docuIngreso
                query_entrada = "INSERT INTO entrada (fecha, docuIngreso) VALUES (%s, %s)"
                cursor.execute(query_entrada, (fecha, docu_ingreso))
                connection.commit()

                # Obtener el identrada recién generado
                cursor.execute("SELECT LAST_INSERT_ID()")  
                identrada = cursor.fetchone()[0]

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
                    idproducto = producto[0]  
                    cantidad = int(producto[2])  
                    precio_nuevo = float(producto[3])  
                    idproveedor = producto[4]  

                    cursor.execute(query_detalle, (identrada, idproducto, cantidad, idproveedor, precio_nuevo))
                    cursor.execute(query_actualizar_producto, (cantidad, precio_nuevo, cantidad, cantidad, idproducto))

                connection.commit()
                return identrada  

            except Exception as e:
                connection.rollback()
                print(f"Error al guardar la entrada: {e}")
                return None
            finally:
                self.conexion_db.cerrar_conexion()


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
                        d.precioEntrada,  -- ✅ Usamos precioEntrada de entradaDetalle
                        f.nomfamilia,
                        e.fecha,
                        e.docuIngreso,  -- ✅ Se añade el campo Documento de Ingreso
                        d.cantidad,
                        prov.nombre AS Proveedor
                    FROM entradaDetalle d
                    JOIN entrada e ON e.identrada = d.identrada
                    JOIN producto p ON p.idproducto = d.idproducto
                    LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                    LEFT JOIN proveedor prov ON d.idproveedor = prov.idproveedor
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
                        d.precioEntrada AS Precio_Entrada,  
                        f.nomfamilia AS Familia,
                        e.fecha AS Fecha_Entrada,
                        e.docuIngreso AS Documento_Ingreso,  
                        d.cantidad AS Cantidad,
                        prov.nombre AS Proveedor
                    FROM entradaDetalle AS d  -- 🔹 Se usa alias 'd'
                    JOIN entrada AS e ON e.identrada = d.identrada  -- ✅ Verifica que identrada exista en ambas tablas
                    JOIN producto AS p ON p.idproducto = d.idproducto
                    LEFT JOIN familia AS f ON p.idfamilia = f.idfamilia
                    LEFT JOIN proveedor AS prov ON d.idproveedor = prov.idproveedor
                    ORDER BY e.fecha DESC;
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
