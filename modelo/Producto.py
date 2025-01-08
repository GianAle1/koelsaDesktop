from modelo.conexion import ConexionDB

class Producto:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def registrar_producto(self, nombre, descripcion, cantidad, precio, proveedor_id, marca_id, idalmacenDetalle, und_medida, familia):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "INSERT INTO producto (partname, descripcion, cantidad, precio, idproveedor, idmarca, idalmacenDetalle, idunidadMedida,idfamilia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (nombre, descripcion, cantidad, precio,proveedor_id,marca_id,idalmacenDetalle,und_medida,familia))
                connection.commit()             
                return True 
            except Exception as e:
                print(f"Error al registrar el producto: {e}")
                self.conexion_db.cerrar_conexion()  
                return False
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False
        
    def listar_productos(self):
        connection = self.conexion_db.conectar()  # Abre una nueva conexión
        if connection:
            try:
                cursor = connection.cursor()  # Obtén un cursor directamente de la conexión activa
                query = """
                    SELECT 
                    p.idproducto AS ID,
                    p.partname AS PartName,
                    p.descripcion AS Descripción,
                    m.nombre AS Marca,
                    pr.nombre AS Proveedor,
                    f.nomfamilia AS Familia,
                    u.nomUnidad AS UnidadMedida,
                    p.cantidad AS Cantidad,
                    p.precio AS Precio,
                    a.nombre AS Almacen,
                    ad.ubicacion AS Ubicacion
                    FROM producto p
                    LEFT JOIN marca m ON p.idmarca = m.idmarca
                    LEFT JOIN proveedor pr ON p.idproveedor = pr.idproveedor
                    INNER JOIN unidadMedida u ON p.idunidadMedida = u.idunidadMedida
                    INNER JOIN familia f ON p.idfamilia = f.idfamilia
                    LEFT JOIN almacenDetalle ad ON p.idalmacenDetalle = ad.idalmacenDetalle 
                    INNER JOIN almacen a ON a.idalmacen = ad.idalmacen
                """
                cursor.execute(query)  # Ejecuta la consulta
                productos = cursor.fetchall()
                return productos  # Devuelve los resultados
            except Exception as e:
                print(f"Error al obtener productos: {e}")
                return []
            finally:
                # Asegúrate de cerrar el cursor y la conexión después de usarla
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
                    SELECT p.idproducto, p.partname, p.descripcion, m.nombre AS Marca,
                        pr.nombre AS Proveedor, f.nomfamilia AS Familia,
                        u.nomUnidad AS UnidadMedida, p.cantidad, p.precio, a.nombre AS Almacen
                    FROM producto p
                    LEFT JOIN marca m ON p.idmarca = m.idmarca
                    LEFT JOIN proveedor pr ON p.idproveedor = pr.idproveedor
                    LEFT JOIN familia f ON p.idfamilia = f.idfamilia
                    LEFT JOIN UnidadMedida u ON p.idunidadMedida = u.idunidadMedida
                    LEFT JOIN almacenDetalle ad ON p.idalmacenDetalle = ad.idalmacenDetalle
                    LEFT JOIN almacen a ON ad.idalmacen = a.idalmacen
                    WHERE f.nomfamilia = %s
                """
                cursor.execute(query, (familia,))
                productos = cursor.fetchall()
                return productos
            except Exception as e:
                print(f"Error al obtener productos por familia: {e}")
                return []
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []

    