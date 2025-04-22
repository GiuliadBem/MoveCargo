import FreeSimpleGUI as sg # type: ignore

class TelaLogin:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None

    #---------------------------------------------------------------
    # Helpers
    #---------------------------------------------------------------

    def abre_tela(self):
        # Estilo padronizado
        style = {
            "titleSize": (8,1),
            "inputSize": (26,1)
        }

        # Tela de login
        layout = [
            [
                sg.Text("Usuário:", size=style["titleSize"]), 
                sg.Input(key="username", size=style["inputSize"])
            ],
            [
                sg.Text("Senha:", size=(8,1)), 
                sg.Input(password_char="*", key="password", size=style["inputSize"])
            ],
            [
                sg.Push(),
                sg.Text("", key="mensagem", text_color="red"),
                sg.Push()
            ],
            [
                sg.Push(),
                sg.Button("Entrar"), 
                sg.Button("Cancelar"),
                sg.Push()
            ],
        ]

        # Configurações da Tela
        self.__window = sg.Window("Login", layout)

    def fechar(self):
        # Fecha a tela, caso aberta
        if self.__window: self.__window.close()
        self.__window = None
    
    def mostrar_mensagem(self, msg: str):
        self.__window["mensagem"].update(msg) # type: ignore
    
    #---------------------------------------------------------------
    # Execução
    #---------------------------------------------------------------

    def mostra_tela(self):
        # Abre a tela, caso fechada
        if not self.__window: self.abre_tela()

        # Leitura
        while True:
            event, values = self.__window.read()  # type: ignore

            # Evento de saída
            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                self.fechar()
                return None, None
            # Tentativa de login
            if event == "Entrar":
                username = values["username"].strip()
                password = values["password"].strip()

                # Validação básica de campos vazios
                if not (username and password):
                    self.mostrar_mensagem("Usuário e senha são obrigatórios!")

                # Envio de dados de usuário e login
                else:
                    return username, password