from abc import ABC
from ast import Str
import hashlib
from modelos.frete import Frete

class Notificacao(ABC):
    def __init__(self, mensagem: str, frete: Frete):
        self.__mensagem = mensagem
        self.__frete = frete
        self.__lida = False
    
    #---------------------------------------------------------------
    # Getters
    #---------------------------------------------------------------

    @property
    def mensagem(self):
        self.__lida = True
        return self.__mensagem
    
    @property
    def frete(self):
        return self.__frete
    
    @property
    def lida(self):
        return self.__lida
    
    #---------------------------------------------------------------
    # Métodos
    #---------------------------------------------------------------