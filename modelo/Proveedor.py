from modelo.conexion import ConexionDB

class Proveedor:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def registrar_proveedor(self, nombre, direccion, telefono, correo,ruc):
        """Registra un nuevo proveedor en la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "INSERT INTO proveedor (nombre, direccion, telefono, correo,ruc) VALUES (%s, %s, %s, %s,%s)"
                cursor.execute(query, (nombre, direccion, telefono, correo,ruc))
                connection.commit()  # Confirmar los cambios
                return True  # Retornamos True si el proveedor se registró correctamente
            except Exception as e:
                print(f"Error al registrar el proveedor: {e}")
                self.conexion_db.cerrar_conexion()  # Aseguramos cerrar la conexión
                return False
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False
    def listar_proveedores(self):
        """Obtiene todos los proveedores registrados en la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT idproveedor, nombre,ruc,direccion,telefono, correo FROM proveedor ORDER BY nombre ASC"
                cursor.execute(query)
                proveedores = cursor.fetchall()
                return proveedores  # Retorna la lista de proveedores
            except Exception as e:
                print(f"Error al obtener proveedores: {e}")
               # self.conexion_db.cerrar_conexion()
                return []
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []

    def eliminar_proveedor(self, id_proveedor):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "DELETE FROM proveedor WHERE idproveedor = %s"
                cursor.execute(query, (id_proveedor,))
                connection.commit()
                return cursor.rowcount > 0  # Retorna True si se eliminó al menos un registro
            except Exception as e:
                print(f"Error al eliminar proveedor: {e}")
                return False
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo conectar a la base de datos.")
            return False
    
    