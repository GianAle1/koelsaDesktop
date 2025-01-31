# modelo/familia.py
from modelo.conexion import ConexionDB

class Familia:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def listar_familias(self):
        """Obtiene todas las familias desde la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            if cursor:
                try:
                    query = "SELECT idfamilia, nomfamilia FROM familia ORDER BY nomfamilia ASC"
                    cursor.execute(query)
                    familias = cursor.fetchall()
                    return familias
                except Exception as e:
                    print(f"Error al listar familias: {e}")
                finally:
                    cursor.close()
                    connection.close()
        return []

    def registrar_familia(self, nombre_familia):
        """Registra una nueva familia en la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = connection.cursor()  # Obtener el cursor directamente de la conexión
            try:
                query = "INSERT INTO familia (nomfamilia) VALUES (%s)"
                cursor.execute(query, (nombre_familia,))
                connection.commit()  # Confirmar la transacción
                return True
            except Exception as e:
                print(f"Error al registrar familia: {e}")
                connection.rollback()  # Revertir cambios en caso de error
                return False
            finally:
                cursor.close()
                connection.close()  # Cerrar conexión después de la operación
        return False

    def eliminar_familia(self, idfamilia):
        """Elimina una familia de la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = connection.cursor()
            try:
                query = "DELETE FROM familia WHERE idfamilia = %s"
                cursor.execute(query, (idfamilia,))
                connection.commit()
                return True
            except Exception as e:
                print(f"Error al eliminar familia: {e}")
                connection.rollback()
                return False
            finally:
                cursor.close()
                connection.close()
        return False
