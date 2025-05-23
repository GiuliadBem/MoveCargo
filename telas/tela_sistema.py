import FreeSimpleGUI as sg  # type: ignore

class TelaSistema:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None

    #---------------------------------------------------------------
    # Helpers
    #---------------------------------------------------------------

    def abre_tela(self, usuario):
        # Tela Gerente
        if usuario == "gerente":
            layout = [
                [sg.Text("Menu Principal - Gerente", font=("Helvetica", 15), justification='center', expand_x=True)],
                [sg.VPush()],
                [sg.Button("Fretes", size=(15, 2))],
                [sg.Button("Caminhoneiros", size=(15, 2))],
                [sg.Button("Caminhões", size=(15, 2))],
                [sg.Button("Relatórios", size=(15, 2))],
                [sg.Button("Atualizar Status", size=(15, 2))],
                [sg.VPush()],
                [sg.Button("Sair", size=(15, 1))]
            ]
        # Tela Caminhoneiro
        else:
            layout = [
                [sg.Text("Menu Principal - Caminhoneiro", font=("Helvetica", 15), justification='center', expand_x=True)],
                [sg.VPush()],
                [sg.Button("Meus Fretes", size=(15, 2))],
                [sg.Button("Meu Cadastro", size=(15, 2))],
                [sg.VPush()],
                [sg.Button("Sair", size=(15, 1))]
            ]

        # Configurações da Tela
        self.__window = sg.Window("Sistema de Fretes", layout, size=(300, 550), element_justification='c')

    def fechar(self):
        # Fecha a tela, caso aberta
        if self.__window: self.__window.close()
        self.__window = None

    #---------------------------------------------------------------
    # Execução
    #---------------------------------------------------------------

    def mostra_tela(self, usuario):
        # Abre a tela, caso fechada
        if not self.__window: self.abre_tela(usuario)

        # Leitura
        while True:
            event, _ = self.__window.read()  # type: ignore

            # Evento de saída
            if event in (sg.WINDOW_CLOSED, "Sair"):
                self.fechar()
                return "Sair"
            # Outros
            else:
                self.fechar()
                return event