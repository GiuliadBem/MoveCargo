import pickle
from daos.dao import DAO
from modelos.carga import Carga

class CargaDAO(DAO):
    def __init__(self):
        super().__init__('cargas.pkl')

    def add(self, carga: Carga):
        super().add(carga.codigo, carga)

    def update(self, carga: Carga):
        super().update(carga.codigo, carga)

    def get(self, codigo: str):
        return super().get(codigo)
    
    def remove(self, codigo: str):
        return super().remove(codigo)
    
    def get_all(self):
        return list(super().get_all())