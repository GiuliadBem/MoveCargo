from abc import ABC
import hashlib

class Notificacao(ABC):
    def __init__(self, mensagem: str):
        self.__mensagem = mensagem
        self.__lida = False
    
    #---------------------------------------------------------------
    # Getters
    #---------------------------------------------------------------

    @property
    def mensagem(self):
        self.__lida = True
        return self.__mensagem
    
    @property
    def lida(self):
        return self.__lida