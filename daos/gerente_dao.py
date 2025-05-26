from daos.dao import DAO
from modelos.gerente import Gerente

class GerenteDAO(DAO):
    def __init__(self):
        super().__init__("gerente.pkl")
        if not "gerente" in super().get_all():
            super().add("gerente", Gerente())

    def update(self, gerente: Gerente):
        super().update("gerente", gerente)

    def get(self):
        return super().get("gerente")