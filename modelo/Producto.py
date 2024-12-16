# modelo/Producto.py
from modelo.conexion import ConexionDB

class Producto:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def registrar_producto(self, partname, descripcion, idmarca, undMedida, cantidad, idproveedor, idalmacen, uso, equipo, precio):
        """Registra un nuevo producto en la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = """
                    INSERT INTO producto (partname, descripcion, idmarca, undMedida, cantidad, idproveedor, idalmacen, uso, equipo, precio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query, (partname, descripcion, idmarca, undMedida, cantidad, idproveedor, idalmacen, uso, equipo, precio))
                connection.commit()
                return True  # Retornamos True si el producto se registró correctamente
            except Exception as e:
                print(f"Error al registrar el producto: {e}")
                self.conexion_db.cerrar_conexion()  # Aseguramos cerrar la conexión
                return False
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False
