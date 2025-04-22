from modelos.pessoa import Pessoa
from telas.tela_login import TelaLogin
import hashlib

class ControladorLogin:
    def __init__(self, controlador_sistema):
        self.__sistema = controlador_sistema
        self.__tela_login = TelaLogin()

    #---------------------------------------------------------------
    # Autenticação
    #---------------------------------------------------------------

    def validacao_senha(self, usuario: Pessoa, password: str, sessao):
        # Hash da senha fornecida pelo usuário realizando a autenticação
        hashed_input = hashlib.sha256(password.encode()).hexdigest()

        # Caso haja correspondência do hash com o da senha atual
        if usuario.senha == hashed_input:
            # Armazena a sessão do usuário
            sessao.login(usuario)
            return True
        else: 
            return False

    def autenticar_usuario(self, username: str, password: str) -> bool:
        # Busca pelo usuário na base de caminhoneiros
        usuario = self.__sistema.controlador_caminhoneiro.procura_caminhoneiro(username)

        # Se usuário caminhoneiro não é encontrado, assume o usuário gerente
        if not usuario and username == "gerente":
            usuario = self.__sistema.controlador_gerente.gerente
        
        # Valida a senha com base nos dados do usuário fornecido
        if usuario and self.validacao_senha(usuario, password, self.__sistema.sessao):
            return True
        
        # Usuário inexistente, ou falha na validação da senha
        else:
            return False
    
    #---------------------------------------------------------------
    # Inicialização do Login
    #---------------------------------------------------------------

    def iniciar_login(self):
        # Inicializa a tela para coleta dos dados de usuário e senha do usuário
        username, password = self.__tela_login.mostra_tela()

        # Finaliza caso o usuário cancele a operação
        if username is None or password is None:
            return "Sair"
        
        # Validação dos dados fornecidos
        authOK = self.autenticar_usuario(username, password)

        # Apresenta erro para o usuário em falha de autenticação
        if not authOK:
            self.__tela_login.mostrar_mensagem("Usuário ou senha inválidos.")
            return "Falha"
        
        # Se autenticação OK, encerra o fluxo de login
        elif authOK:
            self.__tela_login.fechar()
            return "Sucesso"
