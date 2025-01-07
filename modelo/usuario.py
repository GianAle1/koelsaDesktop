from modelo.conexion import ConexionDB  # Importamos la clase ConexionDB

class Usuario:
    def __init__(self):
        self.db = ConexionDB()  # Usamos la clase de conexión
        self.conn = None  # La conexión será gestionada por ConexionDB

    def verificar_credenciales(self, username, password):
        """Verifica las credenciales del usuario en la base de datos."""
        try:
            # Establecemos la conexión
            self.conn = self.db.conectar()  # Usamos la conexión gestionada por ConexionDB
            if not self.conn:
                return False  # Si no se pudo establecer la conexión, retornamos False

            cursor = self.conn.cursor()  # Obtenemos el cursor para realizar la consulta
            query = "SELECT * FROM usuario WHERE correo = %s AND contraseña = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            return False
        finally:
            # Asegúrate de cerrar el cursor después de usarlo
            if cursor:
                cursor.close()
            # Aseguramos también cerrar la conexión aquí si es necesario
            if self.conn:
                self.conn.close()

    def cerrar_conexion(self):
        """Cerrar la conexión con la base de datos."""
        self.db.cerrar_conexion()  # Llamamos al método de ConexionDB para cerrar la conexión
