from modelo.conexion import ConexionDB

class ModeloBacklog:
    def __init__(self):
        self.conexion_db = ConexionDB()

    def listar_backlogs(self):
        connection = self.conexion_db.conectar()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT * FROM backlog"
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error al listar backlogs: {e}")
                return []
            finally:
                connection.close()
        else:
            print("No se pudo conectar a la base de datos.")
            return []

    def guardar_backlog(self, backlog_data, detalles_temporales):
        connection = self.conexion_db.conectar()
        if connection:
            try:
                cursor = connection.cursor()

                # Guardar en la tabla backlog
                query_backlog = """
                    INSERT INTO backlog (
                        horometro, prioridad, ubicacion, fecha, detalle, hora,
                        recurso_humano, cantidad_recurso, equipo_soporte,
                        elaborado_por, revisado_por, aprobado_por
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_backlog, (
                    backlog_data["horometro"],
                    backlog_data["prioridad"],
                    backlog_data["ubicacion"],
                    backlog_data["fecha"],
                    backlog_data["detalle"],
                    backlog_data["hora"],
                    backlog_data["recurso_humano"],
                    backlog_data["cantidad_recurso"],
                    backlog_data["equipo_soporte"],
                    backlog_data["elaborado_por"],
                    backlog_data["revisado_por"],
                    backlog_data["aprobado_por"]
                ))
                connection.commit()

                # Obtener el ID del backlog recién creado
                backlog_id = cursor.lastrowid

                # Guardar en la tabla backlogDetalle
                query_detalle = """
                    INSERT INTO backlogDetalle (
                        idbacklog, smcs, idproducto, idmarca, detalle, precio, necesita, stock
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                for detalle in detalles_temporales:
                    # Asegúrate de que `detalle` sea un diccionario
                    cursor.execute(query_detalle, (
                        backlog_id,
                        detalle["smcs"],
                        int(detalle["idproducto"]),  # Convertir a int si es necesario
                        int(detalle["idmarca"]),    # Convertir a int si es necesario
                        detalle["detalle"],
                        float(detalle["precio"]),  # Convertir a float si es necesario
                        int(detalle["necesita"]),  # Convertir a int si es necesario
                        int(detalle["stock"])      # Convertir a int si es necesario
                    ))
                connection.commit()

                return backlog_id
            except Exception as e:
                print(f"Error al guardar backlog: {e}")
                connection.rollback()
                return None
            finally:
                connection.close()
        else:
            print("No se pudo conectar a la base de datos.")
            return None
