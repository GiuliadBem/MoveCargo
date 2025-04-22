from modelos.pessoa import Pessoa

class Sessao:
    def __init__(self):
        self.__usuario_atual = None

    #---------------------------------------------------------------
    # Getters
    #---------------------------------------------------------------

    @property
    def usuario_atual(self):
        return self.__usuario_atual
    
    #---------------------------------------------------------------
    # Métodos
    #---------------------------------------------------------------

    def login(self, usuario: Pessoa):
        # Realiza o armazenamento do usuário atual
        self.__usuario_atual = usuario

    def logout(self):
        # Realiza a limpeza do usuário atual
        self.__usuario_atual = None