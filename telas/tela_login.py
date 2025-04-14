import FreeSimpleGUI as sg

class TelaLogin:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None

    def abre_tela(self):
        layout = [
            [sg.Text("Usuário:"), sg.Input(key="username")],
            [sg.Text("Senha:"), sg.Input(password_char="*", key="password")],
            [sg.Button("Entrar"), sg.Button("Cancelar")],
            [sg.Text("", size=(30, 1), key="mensagem", text_color="red")]
        ]
        self.__window = sg.Window("Login", layout)

    def mostra_tela(self):
        if not self.__window:
            self.abre_tela()
        while True:
            event, values = self.__window.read() # type: ignore
            if event == sg.WINDOW_CLOSED or event == "Cancelar":
                break
            if event == "Entrar":
                return values["username"], values["password"]
        self.__window.close()
        return None, None

    def mostrar_mensagem(self, msg: str):
        self.__window["mensagem"].update(msg) # type: ignore

    def fechar(self):
        self.__window.close() # type: ignore

telaLogin = TelaLogin()
print(str(telaLogin.mostra_tela()))