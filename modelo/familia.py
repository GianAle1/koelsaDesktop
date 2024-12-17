from modelo.conexion import ConexionDB

class Familia:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def listar_familias(self):
        """Obtiene la lista de familias desde la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            if cursor:
                try:
                    query = "SELECT * FROM familia"
                    cursor.execute(query)
                    familias = cursor.fetchall()
                    return familias
                except Exception as e:
                    print(f"Error al listar familias: {e}")
                    return []
            else:
                print("No se pudo obtener el cursor para la consulta.")
                return []
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []