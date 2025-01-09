from modelo.backlog import ModeloBacklog

class ControladorBacklog:
    def __init__(self):
        # El modelo se inicializa internamente, como en otros controladores
        self.modelo_backlog = ModeloBacklog()

    def listar_backlogs(self):
        try:
            return self.modelo_backlog.listar_backlogs()
        except Exception as e:
            print(f"Error al listar backlogs: {e}")
            return []

    def guardar_backlog(self, backlog_data, detalles_temporales):
        try:
            return self.modelo_backlog.guardar_backlog(backlog_data, detalles_temporales)
        except Exception as e:
            print(f"Error al guardar backlog: {e}")
            return None
