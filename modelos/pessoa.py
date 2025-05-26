from abc import ABC
import hashlib

from modelos.notificacao import Notificacao

class Pessoa(ABC):
    def __init__(self, usuario: str, senha: str):
        self.__usuario = usuario.lower()
        self.__senha = self.__hash_senha(senha)
        self.__notificacoes: list[Notificacao] = []
    
    #---------------------------------------------------------------
    # Getters
    #---------------------------------------------------------------

    @property
    def usuario(self):
        return self.__usuario
    
    @property
    def senha(self):
        return self.__senha
    
    @property
    def notificacoes(self):
        return self.__notificacoes
    
    def receber_notificacao(self, notificacao: Notificacao):
        self.__notificacoes.append(notificacao)
    
    def limpar_notificacoes(self):
        self.__notificacoes = []
    
    #---------------------------------------------------------------
    # Métodos
    #---------------------------------------------------------------

    def __hash_senha(self, senha: str) -> str:
        # Hash password for storing
        return hashlib.sha256(senha.encode()).hexdigest()