from telas.tela_sistema import TelaSistema
from controladores.controlador_caminhao import ControladorCaminhao
from controladores.controlador_caminhoneiro import ControladorCaminhoneiro
from controladores.controlador_frete import ControladorFrete
from controladores.controlador_gerente import ControladorGerente
from controladores.controlador_login import ControladorLogin
from modelos.sessao import Sessao


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema()
        self.__controlador_caminhao = ControladorCaminhao(self)
        self.__controlador_caminhoneiro = ControladorCaminhoneiro(self)
        self.__controlador_frete = ControladorFrete(self)
        self.__controlador_gerente = ControladorGerente(self)
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
    def controlador_frete(self):
        return self.__controlador_frete
    
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
        # Solicitar Autenticação
        while True:
            autenticacao = self.controlador_login.iniciar_login()
            match autenticacao:
                # Sucesso na autenticação
                case "Sucesso": break

                # Usuário ou senha incorretos
                case "Falha": pass

                # Sair do programa
                case "Sair": return
        
        # Fluxo do programa
        while True:
            botao = self.__tela_sistema.mostra_tela(self.sessao.usuario_atual.usuario) # type: ignore
            match botao:
                # Botões Gerente
                case "Fretes": self.controlador_frete.opcoes_frete("Gerente")
                case "Caminhoneiros": self.controlador_caminhoneiro.opcoes_caminhoneiro()
                case "Caminhões": self.controlador_caminhao.opcoes_caminhao()
                case "Relatórios": pass

                # Botões Caminhoneiro
                case "Meus Fretes": self.controlador_frete.opcoes_meus_fretes(self.sessao.usuario_atual.id)
                case "Meu Cadastro": self.controlador_caminhoneiro.atualizar_caminhoneiro(self.sessao.usuario_atual.id)

                # Sair do programa
                case "Sair": return
