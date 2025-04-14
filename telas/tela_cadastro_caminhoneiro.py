import FreeSimpleGUI as sg

class TelaCaminhoneiro:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None

    def tela_opcoes(self):
            layout = [
                [sg.Text("CAMINHONEIROS", font=("Arial", 14), justification='center', expand_x=True)],
                [sg.Button("Cadastrar Caminhoneiro", size=(25, 1), key=1)],
                [sg.Button("Retornar ao Menu Principal", size=(25, 1), key=0)],
            ]

            self.__window = sg.Window("Menu Caminhoneiro", layout)

            while True:
                event, _ = self.__window.read()
                if event in (sg.WINDOW_CLOSED, 0):
                    return 0
                elif event in (1, 2, 3, 4):
                    return event
                
    def pega_dados_caminhoneiro(self):
            layout = [
                [sg.Text("Cadastro de Caminhoneiro", font=("Arial", 14), justification="center", expand_x=True)],
                [sg.Text("Usuário:", size=(15, 1)), sg.InputText(key="usuario")],
                [sg.Text("Senha:", size=(15, 1)), sg.InputText(key="senha", password_char="*")],
                [sg.Text("Nome:", size=(15, 1)), sg.InputText(key="nome")],
                [sg.Text("CPF:", size=(15, 1)), sg.InputText(key="cpf")],
                [sg.Text("Telefone:", size=(15, 1)), sg.InputText(key="telefone")],
                [sg.Text("E-mail:", size=(15, 1)), sg.InputText(key="email")],
                [sg.Text("Número CNH:", size=(15, 1)), sg.InputText(key="num_cnh")],
                [sg.Text("Categoria CNH:", size=(15, 1)), sg.InputText(key="cat_cnh")],
                [sg.Text("Possui MOPP (Sim/Não):", size=(15, 1)), sg.InputText(key="possui_MOPP")],
                [sg.Button("Confirmar"), sg.Button("Cancelar")]
            ]

            janela = sg.Window("Cadastro de Caminhoneiro", layout)
            while True:
                evento, valores = janela.read()
                if evento in (sg.WINDOW_CLOSED, "Cancelar"):
                    janela.close()
                    return None
                elif evento == "Confirmar":
                    janela.close()
                    return valores

    def mostrar_mensagem(self, msg: str):
        sg.popup(msg, title="Aviso")

    def fechar(self):
        if self.__window:
            self.__window.close()