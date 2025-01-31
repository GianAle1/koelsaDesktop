import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        self.connection = None

    def conectar(self):
        """
        Establece la conexión con la base de datos MySQL.
        Si la conexión ya existe y está activa, la reutiliza.
        """
        try:
            if not self.connection or not self.connection.is_connected():
                # Establece la conexión a la base de datos MySQL
                self.connection = mysql.connector.connect(
                    host='192.168.180.137',        # viaduct.proxy.rlwy.net
                    user='new_user',             # new_user
                    password='new_password',       # root
                    database='koelsa',       # Nombre de tu base de datos
                    port=3310                # 17447
                )
                if self.connection.is_connected():
                    print("Conexión exitosa a la base de datos MySQL")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.connection = None

        return self.connection

    def cerrar_conexion(self):
        """
        Cierra el cursor y la conexión a la base de datos si están activos.
        """
        if self.connection and self.connection.is_connected():
            try:
                self.connection.close()
                print("Conexión cerrada correctamente")
            except Error as e:
                print(f"Error al cerrar la conexión: {e}")

    def obtener_cursor(self):
        """
        Retorna un cursor para realizar consultas.
        Si no hay una conexión activa, intenta reconectar.
        """
        if not self.connection or not self.connection.is_connected():
            print("No hay conexión activa. Intentando reconectar...")
            self.conectar()

        if self.connection and self.connection.is_connected():
            try:
                return self.connection.cursor(buffered=True)  # Usa cursor con buffer para evitar errores con fetches
            except Error as e:
                print(f"Error al obtener el cursor: {e}")
                return None
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return None
