from modelo.conexion import ConexionDB

class Maquinaria:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def obtener_maquinarias(self):
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT idmaquinaria, modelo, serie FROM maquinaria ORDER BY serie ASC"
                cursor.execute(query)
                maquinarias = cursor.fetchall()
                return maquinarias
            except Exception as e:
                print(f"Error al obtener maquinarias: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo conectar a la base de datos.")
            return []   
    