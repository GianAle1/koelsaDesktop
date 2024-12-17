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
                # Consulta SQL para insertar el producto
                query = "INSERT INTO producto (partname, descripcion, cantidad, precio, idproveedor, idmarca, idalmacen, idunidadMedida, iduso, idequipo,idfamilia) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.execute(query, (nombre, descripcion, cantidad, precio,proveedor_id,marca_id,almacen_id,und_medida,uso,equipo,familia))
                connection.commit()  # Confirmar los cambios                
                return True 
            except Exception as e:
                print(f"Error al registrar el producto: {e}")
                self.conexion_db.cerrar_conexion()  # Aseguramos cerrar la conexión
                return False
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False