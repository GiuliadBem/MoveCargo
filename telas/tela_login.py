import FreeSimpleGUI as sg

class TelaLogin:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None

    def abre_tela(self):
        style = {
            "titleSize": (8,1),
            "inputSize": (26,1)
        }

        blankLine = [sg.Text("", size=(1,1))]

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
                sg.Text("", size=(30, 1), key="mensagem", text_color="red")
            ],
            [
                sg.Push(),  # pushes next elements to center
                sg.Button("Entrar"), 
                sg.Button("Cancelar"),
                sg.Push()   # pushes back to center from other side
            ],
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