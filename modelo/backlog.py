from modelo.conexion import ConexionDB

class Backlog:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def guardar_backlog(self, backlog_data, backlog_detalle_data):
        """
        Guarda un backlog junto con sus detalles en la base de datos.

        :param backlog_data: Diccionario con los datos de la tabla backlog.
        :param backlog_detalle_data: Lista de diccionarios con los datos de backlogDetalle.
        :return: ID del backlog creado o None en caso de error.
        """
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Insertar en la tabla backlog
                query_backlog = """
                    INSERT INTO backlog (
                        horometro, prioridad, ubicacion, fecha, detalle, hora, recurso_humano, 
                        cantidad_recurso, equipo_soporte, elaborado_por, revisado_por, aprobado_por
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_backlog, (
                    backlog_data['horometro'], backlog_data['prioridad'], backlog_data['ubicacion'],
                    backlog_data['fecha'], backlog_data['detalle'], backlog_data['hora'],
                    backlog_data['recurso_humano'], backlog_data['cantidad_recurso'],
                    backlog_data['equipo_soporte'], backlog_data['elaborado_por'],
                    backlog_data['revisado_por'], backlog_data['aprobado_por']
                ))
                connection.commit()

                # Obtener el ID del backlog recién creado
                cursor.execute("SELECT LAST_INSERT_ID()")
                id_backlog = cursor.fetchone()[0]

                # Insertar los detalles en backlogDetalle
                query_backlog_detalle = """
                    INSERT INTO backlogDetalle (
                        idbacklog, smcs, idproducto, idmarca, idunidadMedida, detalle, precio, necesita, stock
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                for detalle in backlog_detalle_data:
                    cursor.execute(query_backlog_detalle, (
                        id_backlog, detalle['smcs'], detalle['idproducto'], detalle['idmarca'],
                        detalle['idunidadMedida'], detalle['detalle'], detalle['precio'],
                        detalle['necesita'], detalle['stock']
                    ))
                connection.commit()

                return id_backlog
            except Exception as e:
                print(f"Error al guardar el backlog: {e}")
                connection.rollback()
                return None
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return None

    def listar_backlogs(self):
        """
        Lista todos los backlogs registrados en la base de datos.
        :return: Lista de backlogs.
        """
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = "SELECT * FROM backlog"
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar backlogs: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []

    def obtener_backlog_detalle(self, id_backlog):
        """
        Obtiene los detalles de un backlog específico.

        :param id_backlog: ID del backlog.
        :return: Lista de detalles del backlog.
        """
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                query = """
                    SELECT * FROM backlogDetalle WHERE idbacklog = %s
                """
                cursor.execute(query, (id_backlog,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al obtener detalles del backlog: {e}")
                return []
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return []

    def eliminar_backlog(self, id_backlog):
        """
        Elimina un backlog y sus detalles asociados.

        :param id_backlog: ID del backlog a eliminar.
        :return: True si se eliminó correctamente, False en caso contrario.
        """
        connection = self.conexion_db.conectar()
        if connection:
            cursor = self.conexion_db.obtener_cursor()
            try:
                # Eliminar los detalles del backlog primero (por la restricción de clave foránea)
                query_detalle = "DELETE FROM backlogDetalle WHERE idbacklog = %s"
                cursor.execute(query_detalle, (id_backlog,))

                # Eliminar el backlog
                query_backlog = "DELETE FROM backlog WHERE idbacklog = %s"
                cursor.execute(query_backlog, (id_backlog,))

                connection.commit()
                return True
            except Exception as e:
                print(f"Error al eliminar backlog: {e}")
                connection.rollback()
                return False
            finally:
                self.conexion_db.cerrar_conexion()
        else:
            print("No se pudo establecer una conexión a la base de datos.")
            return False
