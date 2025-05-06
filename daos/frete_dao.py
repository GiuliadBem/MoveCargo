from daos.dao import DAO
from modelos.frete import Frete

class FreteDAO(DAO):
    def __init__(self):
        super().__init__("frete.pkl")

    def add(self, frete):
        super().add(frete.id, frete)

    def update(self, frete):
        super().update(frete.id, frete)

    def get(self, chave: int):
        return super().get(chave)
    
    def remove(self, chave: int):
        return super().remove(chave)