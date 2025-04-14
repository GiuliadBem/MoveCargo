from daos.dao import DAO
from modelos.caminhoneiro import Caminhoneiro

class CaminhoneiroDAO(DAO):
    def __init__(self):
        super().__init__("caminhoneiro.pkl")

    def add(self, caminhoneiro: Caminhoneiro):
        super().add(caminhoneiro.usuario, caminhoneiro)

    def update(self, caminhoneiro: Caminhoneiro):
        super().update(caminhoneiro.usuario, caminhoneiro)

    def get(self, chave: int):
        return super().get(chave)
    
    def remove(self, chave: int):
        return super().remove(chave)