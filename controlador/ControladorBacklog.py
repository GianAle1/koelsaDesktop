class ControladorBacklog:
    def __init__(self, modelo_backlog):
        self.modelo_backlog = modelo_backlog

    def guardar_backlog(self, backlog_data, detalles):
        """
        Guarda un backlog con sus detalles correspondientes.

        :param backlog_data: Diccionario con los datos principales del backlog.
        :param detalles: Lista de diccionarios con los detalles del backlog.
        :return: True si se guardó correctamente, False en caso contrario.
        """
        try:
            # Guardar el backlog principal
            idbacklog = self.modelo_backlog.crear_backlog(backlog_data)

            # Guardar los detalles relacionados
            for detalle in detalles:
                detalle['idbacklog'] = idbacklog
                self.modelo_backlog.crear_backlog_detalle(detalle)

            return True
        except Exception as e:
            print(f"Error al guardar el backlog: {e}")
            return False

    def listar_backlogs(self):
        """
        Obtiene una lista de todos los backlogs.

        :return: Lista de backlogs.
        """
        try:
            return self.modelo_backlog.listar_backlogs()
        except Exception as e:
            print(f"Error al listar los backlogs: {e}")
            return []

    def obtener_backlog(self, idbacklog):
        """
        Obtiene un backlog específico junto con sus detalles.

        :param idbacklog: ID del backlog a obtener.
        :return: Diccionario con los datos del backlog y sus detalles.
        """
        try:
            backlog = self.modelo_backlog.obtener_backlog(idbacklog)
            detalles = self.modelo_backlog.listar_backlog_detalles(idbacklog)
            return {"backlog": backlog, "detalles": detalles}
        except Exception as e:
            print(f"Error al obtener el backlog: {e}")
            return None

    def actualizar_backlog(self, idbacklog, nuevos_datos, nuevos_detalles):
        """
        Actualiza un backlog y sus detalles.

        :param idbacklog: ID del backlog a actualizar.
        :param nuevos_datos: Diccionario con los nuevos datos del backlog.
        :param nuevos_detalles: Lista de diccionarios con los nuevos detalles del backlog.
        :return: True si se actualizó correctamente, False en caso contrario.
        """
        try:
            # Actualizar el backlog principal
            self.modelo_backlog.actualizar_backlog(idbacklog, nuevos_datos)

            # Eliminar los detalles anteriores
            self.modelo_backlog.eliminar_backlog_detalles(idbacklog)

            # Insertar los nuevos detalles
            for detalle in nuevos_detalles:
                detalle['idbacklog'] = idbacklog
                self.modelo_backlog.crear_backlog_detalle(detalle)

            return True
        except Exception as e:
            print(f"Error al actualizar el backlog: {e}")
            return False

    def eliminar_backlog(self, idbacklog):
        """
        Elimina un backlog y todos sus detalles asociados.

        :param idbacklog: ID del backlog a eliminar.
        :return: True si se eliminó correctamente, False en caso contrario.
        """
        try:
            self.modelo_backlog.eliminar_backlog(idbacklog)
            return True
        except Exception as e:
            print(f"Error al eliminar el backlog: {e}")
            return False
