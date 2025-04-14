from modelos.login import Login
from telas.tela_login import TelaLogin

class ControladorLogin:
    def __init__(self, controlador_sistema):
        self.__sistema = controlador_sistema
        self.__tela_login = TelaLogin()

    def autenticar_usuario(self, username: str, password: str) -> bool:
        usuario = self.__sistema.controlador_caminhoneiro.get_by_usuario(username)
        if not usuario:
            usuario = self.__sistema.controlador_gerente.get_by_usuario(username)
        
        if usuario and Login.authenticate(usuario, password, self.__sistema.sessao):
            return True
        return False

    def iniciar_login(self):
        username, password = self.__tela_login.mostra_tela()
        if username is None or password is None:
            return False  # User canceled or closed the window
        
        if self.autenticar_usuario(username, password):
            self.__tela_login.fechar()
            return True
        else:
            self.__tela_login.mostrar_mensagem("Usuário ou senha inválidos.")
            return False
