from daos.dao import DAO
from modelos.caminhao import Caminhao

class CaminhaoDAO(DAO):
    def __init__(self):
        super().__init__("caminhao.pkl")

    def add(self, caminhao: Caminhao):
        super().add(caminhao.id, caminhao)

    def update(self, caminhao: Caminhao):
        super().update(caminhao.id, caminhao)

    def get(self, chave: int):
        return super().get(chave)
    
    def remove(self, chave: int):
        return super().remove(chave)