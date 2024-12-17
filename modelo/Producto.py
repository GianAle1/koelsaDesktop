# modelo/Producto.py
from modelo.conexion import ConexionDB

class Producto:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def registrar_producto(self, nombre, descripcion, cantidad, precio, proveedor_id, marca_id, almacen_id, und_medida, uso, equipo, familia):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "INSERT INTO producto (partname, descripcion, cantidad, precio, idproveedor, idmarca, idalmacen, idunidadMedida, iduso, idequipo,idfamilia) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.execute(query, (nombre, descripcion, cantidad, precio,proveedor_id,marca_id,almacen_id,und_medida,uso,equipo,familia))
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
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = """
            SELECT 
                p.idproducto AS ID,
                p.partname AS PartName,
                p.descripcion AS Descripción,
                m.nombre AS Marca,
                pr.nombre AS Proveedor,
                f.nomfamilia as Familia,
                u.nomUnidad AS "Unidad de Medida",
                p.cantidad AS Cantidad,
                p.precio AS Precio,
                a.nombre AS Almacén
            FROM producto p
            LEFT JOIN marca m ON p.idmarca = m.idmarca
            LEFT JOIN proveedor pr ON p.idproveedor = pr.idproveedor
            INNER JOIN UnidadMedida u ON p.idunidadMedida = u.idunidadMedida
            INNER JOIN familia  f ON p.idfamilia = f.idfamilia
            INNER JOIN almacen a ON p.idalmacen = a.idalmacen;
            """
                cursor.execute(query)
                productos = cursor.fetchall()
                return productos 
            except Exception as e:
                print(f"Error al obtener productos: {e}")
                return []
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []