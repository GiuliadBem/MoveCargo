from modelos.gerente import Gerente

class ControladorGerente:
    def __init__(self, controlador_sistema):
        self.__gerente = Gerente()
        self.__controlador_sistema = controlador_sistema

    @property
    def gerente(self):
        return self.__gerente