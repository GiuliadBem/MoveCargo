import FreeSimpleGUI as sg  # type: ignore

class TelaSistema:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None

    #---------------------------------------------------------------
    # Helpers
    #---------------------------------------------------------------

    def abre_tela(self, usuario, notificacoes_nao_lidas=1):
        # Common elements for notification bell
        notification_bell = [
            sg.Button('🔔', key='Notificações', button_color=('black', sg.theme_background_color())), 
            sg.Text(
                str(notificacoes_nao_lidas) if notificacoes_nao_lidas > 0 else '',
                size=(2, 1),
                font=('Helvetica', 10, 'bold'),
                background_color='red' if notificacoes_nao_lidas > 0 else sg.theme_background_color(),
                text_color='white',
                pad=(0, 0),
                justification='center',
                border_width=1,
                relief='solid',
                key='notification_count',
                visible=notificacoes_nao_lidas > 0
            )
        ]

        # Tela Gerente
        if usuario == "gerente":
            layout = [
                [sg.Text("Menu Principal - Gerente", font=("Helvetica", 15), justification='center', expand_x=True)],
                [sg.Column([notification_bell], element_justification='right')],
                [sg.VPush()],
                [sg.Button("Fretes", size=(15, 2))],
                [sg.Button("Caminhoneiros", size=(15, 2))],
                [sg.Button("Caminhões", size=(15, 2))],
                [sg.Button("Relatórios", size=(15, 2))],
                [sg.Button("Atualizar Status dos Fretes", key="Atualizar Status", size=(15, 2))],
                [sg.VPush()],
                [sg.Button("Sair", size=(15, 1))]
            ]
        # Tela Caminhoneiro
        else:
            layout = [
                [sg.Text("Menu Principal - Caminhoneiro", font=("Helvetica", 15), justification='center', expand_x=True)],
                [sg.Column([notification_bell], element_justification='right')],
                [sg.VPush()],
                [sg.Button("Meus Fretes", size=(15, 2))],
                [sg.Button("Meu Cadastro", size=(15, 2))],
                [sg.VPush()],
                [sg.Button("Sair", size=(15, 1))]
            ]

        # Configurações da Tela
        self.__window = sg.Window("Sistema de Fretes", layout, size=(300, 600), element_justification='c')

    def fechar(self):
        if self.__window: 
            self.__window.close()
        self.__window = None

    #---------------------------------------------------------------
    # Execução
    #---------------------------------------------------------------

    def mostra_tela(self, usuario, notificacoes_nao_lidas):
        if not self.__window: 
            self.abre_tela(usuario, notificacoes_nao_lidas)

        while True:
            event, _ = self.__window.read()  # type: ignore

            if event in (sg.WINDOW_CLOSED, "Sair"):
                self.fechar()
                return "Sair"
            else:
                self.fechar()
                return event