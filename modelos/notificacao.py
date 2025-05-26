from abc import ABC
from datetime import datetime
import hashlib

class Notificacao(ABC):
    def __init__(self, mensagem: str):
        self.__mensagem = mensagem
        self.__horario = datetime.now()
        self.__lida = False
    
    #---------------------------------------------------------------
    # Getters
    #---------------------------------------------------------------

    @property
    def mensagem(self):
        return self.__mensagem
    
    @property
    def horario(self):
        return self.__horario
    
    @property
    def lida(self):
        return self.__lida
    
    #---------------------------------------------------------------
    # Métodos
    #---------------------------------------------------------------

    def ler(self):
        self.__lida = True