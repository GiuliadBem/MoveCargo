from modelos.pessoa import Pessoa
from typing import Optional

class Sessao:
    def __init__(self):
        self.__usuario_atual: Optional[Pessoa] = None

    def login(self, usuario: Pessoa):
        self.__usuario_atual = usuario

    def logout(self):
        self.__usuario_atual = None

    @property
    def usuario_atual(self) -> Optional[Pessoa]:
        return self.__usuario_atual