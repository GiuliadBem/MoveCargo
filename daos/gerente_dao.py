from daos.dao import DAO
from modelos.gerente import Gerente

class GerenteDAO(DAO):
    def __init__(self):
        super().__init__("gerente.pkl")
        try: 
            super().get("gerente")
        except:
            super().add("gerente", Gerente())

    def update(self, gerente: Gerente):
        super().update("gerente", gerente)

    def get(self):
        return super().get("gerente")