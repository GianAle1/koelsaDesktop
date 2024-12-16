# modelo/marca.py
from modelo.conexion import ConexionDB

class Uso:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def listar_usos(self):
        """Obtiene la lista de marcas desde la base de datos."""
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            if cursor:
                try:
                    query = "SELECT * FROM uso"
                    cursor.execute(query)
                    usos = cursor.fetchall()
                    return usos
                except Exception as e:
                    print(f"Error al listar marcas: {e}")
                    return []
            else:
                print("No se pudo obtener el cursor para la consulta.")
                return []
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []
    