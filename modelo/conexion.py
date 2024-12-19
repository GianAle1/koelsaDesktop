# modelo/conexion.py
import pyodbc

class ConexionDB:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def conectar(self):
        """
        Establece la conexión con la base de datos SQL Server.
        Si la conexión ya existe, la reutiliza.
        """
        if not self.connection:
            try:
                # Establece la conexión a la base de datos SQL Server
                self.connection = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=DESKTOP-DG21939;'  
                    'DATABASE=koelsa;'
                    'UID=sa;'
                    'PWD=080322'
                )
                self.cursor = self.connection.cursor()
                print("Conexión exitosa a la base de datos")
            except Exception as e:
                print(f"Error al conectar a la base de datos: {e}")
                return None
        return self.connection

    def cerrar_conexion(self):

        if self.connection:
            # Asegúrate de que el cursor no esté cerrado antes de usarlo
            if self.cursor:
                self.cursor.close()  # Cierra el cursor si existe
            self.connection.close()  # Cierra la conexión
            print("Conexión cerrada")


    def obtener_cursor(self):
        """
        Retorna el cursor para realizar las consultas.
        """
        if self.connection:
            return self.cursor
        else:
            print("No hay conexión a la base de datos.")
            return None
