# modelo/marca.py
from modelo.conexion import ConexionDB

class Marca:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def registrar_marca(self, nombre_marca):
        """Registra una nueva marca en la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "INSERT INTO marca (nombre) VALUES (%s)"
                cursor.execute(query, (nombre_marca,))
                connection.commit()  # Confirmar los cambios
                # Ahora, cerrar la conexión después de la operación
                #self.conexion_db.cerrar_conexion()
                return True  # Retornamos True si la marca se registró correctamente
            except Exception as e:
                print(f"Error al registrar la marca: {e}")
                self.conexion_db.cerrar_conexion()  # Aseguramos cerrar la conexión
                return False
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False

    def listar_marcas(self):
        """Obtiene la lista de marcas desde la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            if cursor:
                try:
                    query = "SELECT * FROM marca ORDER BY nombre ASC"
                    cursor.execute(query)
                    marcas = cursor.fetchall()
                    return marcas
                except Exception as e:
                    print(f"Error al listar marcas: {e}")
                    return []
            else:
                print("No se pudo obtener el cursor para la consulta.")
                return []
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []
    def eliminar_marca(self, id_marca):
        """Elimina una marca de la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "DELETE FROM marca WHERE idmarca = %s"
                cursor.execute(query, (id_marca,))
                connection.commit()  # Confirmar los cambios
                # self.conexion_db.cerrar_conexion()  # Cerrar la conexión después de la operación
                return True  # Retornamos True si la marca se eliminó correctamente
            except Exception as e:
                print(f"Error al eliminar la marca: {e}")
                self.conexion_db.cerrar_conexion()  # Aseguramos cerrar la conexión
                return False
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False
