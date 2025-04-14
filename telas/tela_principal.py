import FreeSimpleGUI as sg

class TelaPrincipal:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None

    def abre_tela(self, nome_usuario: str, is_gerente: bool):
        acesso = "Gerente" if is_gerente else "Caminhoneiro"

        layout = [
            [sg.Push(), sg.Text(f"Usuario:", font=("Helvetica", 10, '')), sg.Text(nome_usuario, font=("Helvetica", 10, 'bold'))],
            [sg.Text(f"Acesso {acesso}", font=('Helvetica', 12, 'bold'))],
            [sg.Text("", size=(1,1))],
            [sg.Button("Caminhões", size=(20, 1))],
            [sg.Button("Perfil", size=(20, 1))],
            [sg.Button("Sair", size=(20, 1))]
        ]

        if is_gerente:
            layout.insert(3, [sg.Button("Caminhoneiros", size=(20, 1))])

        self.__window = sg.Window(
            "Sistema de Gerenciamento de Frota", 
            layout, 
            element_justification='c',
            finalize=True,
            size=(800, 600)
        )

    def mostra_tela(self, nome_usuario: str, is_gerente: bool):
        if not self.__window:
            self.abre_tela(nome_usuario, is_gerente)

        event, values = self.__window.read() # type: ignore

        # Exit on close or cancel
        if event in (sg.WINDOW_CLOSED, "Sair"):
            self.fechar()
            return "Sair"
        else:
            return event


    def fechar(self):
        if self.__window:
            self.__window.close()

    def mostrar_mensagem(self, titulo: str, mensagem: str):
        sg.popup(mensagem, title=titulo)


print(TelaPrincipal().mostra_tela("Joao", is_gerente = False))