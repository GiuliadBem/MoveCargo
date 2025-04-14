from controladores.controlador_caminhao import ControladorCaminhao
from controladores.controlador_caminhoneiro import ControladorCaminhoneiro
from controladores.controlador_gerente import ControladorGerente
from controladores.controlador_login import ControladorLogin
from modelos.sessao import Sessao


class ControladorSistema:
    def __init__(self):
        self.__controlador_caminhao = ControladorCaminhao()
        self.__controlador_caminhoneiro = ControladorCaminhoneiro()
        self.__controlador_gerente = ControladorGerente()
        self.__controlador_login = ControladorLogin(self)
        self.__sessao = Sessao()

    #---------------------------------------------------------------
    # Getters
    #---------------------------------------------------------------

    @property
    def controlador_caminhao(self):
        return self.__controlador_caminhao
    
    @property
    def controlador_caminhoneiro(self):
        return self.__controlador_caminhoneiro
    
    @property
    def controlador_gerente(self):
        return self.__controlador_gerente
    
    @property
    def controlador_login(self):
        return self.__controlador_login
    
    @property
    def sessao(self):
        return self.__sessao
    
    #---------------------------------------------------------------
    # Inicialização do Sistema
    #---------------------------------------------------------------

    def iniciar_sistema(self):
        print("Iniciando sistema...")
        while (self.__sessao.usuario_atual == None):
            self.__controlador_login.iniciar_login()
        
        print(f"Login realizado com sucesso para o usuário: ${self.__sessao.usuario_atual.usuario}")