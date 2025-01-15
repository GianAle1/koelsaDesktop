from modelo.conexion import ConexionDB
class Almacen:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def registrar_almacen(self, nombre_almacen,direccion,capacidad):
        """Registra una nueva almacen en la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "INSERT INTO almacen (nombre) VALUES (%s)"
                cursor.execute(query, (nombre_almacen,direccion,capacidad))
                connection.commit()  
                return True
            except Exception as e:
                print(f"Error al registrar la almacen: {e}")
                self.conexion_db.cerrar_conexion()
                return False
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False

    def listar_almacenes(self):
        """Obtiene la lista de alamcenes desde la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            if cursor:
                try:
                    query = "SELECT * FROM almacen"
                    cursor.execute(query)
                    almacenes = cursor.fetchall()
                    return almacenes
                except Exception as e:
                    print(f"Error al listar almacen: {e}")
                    return []
            else:
                print("No se pudo obtener el cursor para la consulta.")
                return []
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []
    def eliminar_alamcen(self, id_alamcen):
        """Elimina una alamcen de la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "DELETE FROM almacen WHERE idalmacen = %s"
                cursor.execute(query, (id_alamcen,))
                connection.commit()  # Confirmar los cambios
                return True
            except Exception as e:
                print(f"Error al eliminar almacen: {e}")
                self.conexion_db.cerrar_conexion()  # Aseguramos cerrar la conexión
                return False
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False

    def obtener_subalmacenes(self, almacen_id):
        """Obtiene los subalmacenes asociados a un almacén específico."""
        connection = self.conexion_db.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT idalmacenDetalle, ubicacion FROM almacenDetalle WHERE idalmacen = %s"
                cursor.execute(query, (almacen_id,))
                resultados = cursor.fetchall()
                if not resultados:
                    print(f"No se encontraron subalmacenes para el almacén ID: {almacen_id}")
                return resultados
            except Exception as e:
                print(f"Error obteniendo subalmacenes: {e}")
                return []
            finally:
                cursor.close()  # Cerrar el cursor explícitamente
                #self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo conectar a la base de datos.")
            return []
