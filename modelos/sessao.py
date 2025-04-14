from modelos.pessoa import Pessoa

class Sessao:
    def __init__(self):
        self.__usuario_atual = None

    def login(self, usuario: Pessoa):
        self.__usuario_atual = usuario

    def logout(self):
        self.__usuario_atual = None

    @property
    def usuario_atual(self):
        return self.__usuario_atual