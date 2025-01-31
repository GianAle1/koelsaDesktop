from modelo.conexion import ConexionDB

class Producto:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def registrar_producto(self, nombre, descripcion, cantidad, precio, codigoInterno, sap, marca_id, idalmacenDetalle, und_medida, familia):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = """
                    INSERT INTO producto 
                    (partname, descripcion, cantidad, precio, codigoInterno,ubicacion, idmarca, idalmacen, idunidadMedida, idfamilia) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nombre, descripcion, cantidad, precio, codigoInterno, sap, marca_id, idalmacenDetalle, und_medida, familia))
                connection.commit()             
                return True 
            except Exception as e:
                print(f"Error al registrar el producto: {e}")
                return False
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False

    def listar_productos(self):
        connection = self.conexion_db.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT 
                    p.idproducto AS ID,
                    p.partname AS PartName,
                    p.descripcion AS Descripción,
                    m.nombre AS Marca,
                    f.nomfamilia AS Familia,
                    u.nomUnidad AS UnidadMedida,
                    p.cantidad AS Cantidad,
                    p.precio AS Precio,
                    p.codigoInterno AS CodigoInterno,
                    p.ubicacion AS Ubicacion,
                    a.nombre AS Almacen
                    FROM producto p
                    LEFT JOIN marca m ON p.idmarca = m.idmarca
                    LEFT JOIN unidadMedida u ON p.idunidadMedida = u.idunidadMedida
                    LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                    LEFT JOIN almacen a ON p.idalmacen = a.idalmacen
                    ORDER BY p.descripcion ASC;
                """
                cursor.execute(query)
                productos = cursor.fetchall()
                return productos
            except Exception as e:
                print(f"Error al obtener productos: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []


    def listar_productos_por_familia(self, familia):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = """
                    SELECT 
                    p.idproducto, 
                    p.partname, 
                    p.descripcion, 
                    m.nombre AS Marca,
                    f.nomfamilia AS Familia,
                    u.nomUnidad AS UnidadMedida, 
                    p.cantidad, 
                    p.precio,
                    p.codigoInterno, 
                    a.nombre AS Almacen,
                    p.ubicacion AS Ubicacion
                FROM producto p
                LEFT JOIN marca m ON p.idmarca = m.idmarca
                LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                LEFT JOIN UnidadMedida u ON p.idunidadMedida = u.idunidadMedida
                LEFT JOIN almacen a ON p.idalmacen = a.idalmacen 
                WHERE f.nomfamilia = %s
                ORDER BY p.descripcion ASC;
                """
                cursor.execute(query, (familia,))
                productos = cursor.fetchall()
                return productos
            except Exception as e:
                print(f"Error al obtener productos por familia: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []
