import FreeSimpleGUI as sg # type: ignore

class TelaLogin:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None

    def abre_tela(self):
        style = {
            "titleSize": (8,1),
            "inputSize": (26,1)
        }

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
        self.__window = sg.Window("Login", layout)

    def mostra_tela(self):
        if not self.__window:
            self.abre_tela()

        while True:
            event, values = self.__window.read()  # type: ignore

            # Exit on close or cancel
            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                self.fechar()
                return None, None

            # Attempt login
            if event == "Entrar":
                username = values["username"].strip()
                password = values["password"].strip()

                # Basic validation (non-empty fields)
                if username and password:
                    return username, password
                else:
                    self.mostrar_mensagem("Usuário e senha são obrigatórios!")

    def mostrar_mensagem(self, msg: str):
        self.__window["mensagem"].update(msg) # type: ignore

    def fechar(self):
        self.__window.close() # type: ignore