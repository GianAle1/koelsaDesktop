from modelo.conexion import ConexionDB

class Responsable:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def listar_responsables(self):
        """Obtiene la lista de responsables desde la base de datos."""
        connection = self.conexion_db.conectar()
        cursor = None
        responsables = []

        if connection:
            cursor = self.conexion_db.obtener_cursor()
            if cursor:
                try:
                    query = "SELECT idresponsable, Nombre FROM responsable ORDER BY Nombre ASC"
                    cursor.execute(query)
                    responsables = cursor.fetchall()
                except Exception as e:
                    print(f"Error al listar responsables: {e}")
                finally:
                    if cursor:  # ✅ Verificar que el cursor existe antes de cerrarlo
                        cursor.close()
                    self.conexion_db.cerrar_conexion()  # ✅ Cerrar la conexión correctamente
        return responsables
