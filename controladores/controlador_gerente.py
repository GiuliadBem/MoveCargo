from daos.gerente_dao import GerenteDAO
from modelos.gerente import Gerente
from modelos.notificacao import Notificacao

class ControladorGerente:
    def __init__(self, controlador_sistema):
        self.__gerente_dao = GerenteDAO()
        self.__controlador_sistema = controlador_sistema

    #---------------------------------------------------------------
    # Getters
    #---------------------------------------------------------------

    @property
    def gerente(self):
        return self.__gerente_dao.get()
    
    #---------------------------------------------------------------
    # Métodos
    #---------------------------------------------------------------

    def notifica_gerente(self, notificacao: Notificacao):
        gerente = self.gerente
        gerente.receber_notificacao(notificacao)
        self.__gerente_dao.update(gerente)