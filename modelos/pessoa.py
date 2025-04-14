from abc import ABC
import hashlib

class Pessoa(ABC):
    def __init__(self, usuario: str, senha: str):
        self.__usuario = usuario
        self.__senha = self.__hash_senha(senha)
    
    # Getters

    @property
    def usuario(self):
        return self.__usuario
    
    @property
    def senha(self):
        return self.__senha

    def __hash_senha(self, senha: str) -> str:
        # Hash password for storing
        return hashlib.sha256(senha.encode()).hexdigest()