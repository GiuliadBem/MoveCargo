from controlador_caminhao import ControladorCaminhao

class ControladorSistema:
    def __init__(self):
        self.__controlador_caminhao = ControladorCaminhao()

    def iniciar_sistema(self):
        print("Iniciando sistema...")
