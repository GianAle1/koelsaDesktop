from modelo.Responsable import Responsable

class ControladorResponsable:
    def __init__(self):
        self.responsable_modelo = Responsable()

    def listar_responsables(self):
        """Retorna la lista de responsables desde el modelo."""
        return self.responsable_modelo.listar_responsables()
