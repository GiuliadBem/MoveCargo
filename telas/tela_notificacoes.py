import FreeSimpleGUI as sg  # type: ignore
from datetime import datetime, timedelta

class TelaNotificacoes:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None

    #---------------------------------------------------------------
    # Helpers
    #---------------------------------------------------------------

    def abre_tela(self, notificacoes):
        # Cabeçalho
        cabecalho = [sg.Text("Notificações", font=("Helvetica", 16), justification='center', pad=(0, (0, 20)))]
        
        # Área de notificações
        notificacoes_layout = []
        
        for notif in reversed(notificacoes):
            # Define a cor de fundo baseado se foi lida ou não
            bg_color = "#E2EFFF" if notif['lida'] else "#ffffff"  # verde claro para lidas, vermelho claro para não lidas
            
            # Formata o horário
            horario_str = notif['horario'].strftime("%d/%m/%Y %H:%M")
            
            # Cria um "retângulo" de notificação
            notificacao = sg.Frame(
                title='',
                layout=[
                    [sg.Text(notif['mensagem'], size=(30, None), background_color=bg_color)],
                    [sg.Push(background_color=bg_color), 
                     sg.Text(horario_str, font=('Helvetica', 8), background_color=bg_color)]
                ],
                background_color=bg_color,
                border_width=1,
                pad=(0, (0, 10)))
            
            # Adiciona cada notificação como uma linha (lista) no layout
            notificacoes_layout.append([notificacao])
        
        # Botão de voltar
        botoes = [sg.Button("Voltar", size=(10, 1), pad=(0, (20, 0)))]
        
        # Layout completo
        layout = [
            cabecalho,
            [sg.Column(
                [[sg.Col(notificacoes_layout, scrollable=True, vertical_scroll_only=True, size=(300, 400))]],
                pad=(0,0)
            )],
            botoes
        ]

        # Configurações da Tela
        self.__window = sg.Window("Sistema de Fretes", layout, size=(350, 550), element_justification='c')

    def fechar(self):
        if self.__window: 
            self.__window.close()
        self.__window = None

    #---------------------------------------------------------------
    # Execução
    #---------------------------------------------------------------

    def mostra_tela(self, notificacoes):
        if not self.__window: 
            self.abre_tela(notificacoes)

        while True:
            event, _ = self.__window.read()  # type: ignore

            if event in (sg.WINDOW_CLOSED, "Voltar"):
                self.fechar()
                return "Voltar"
            else:
                self.fechar()
                return event