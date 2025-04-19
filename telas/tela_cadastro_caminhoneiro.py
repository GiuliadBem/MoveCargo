import FreeSimpleGUI as sg

class TelaCadastroCaminhoneiro:
    def __init__(self):
        sg.theme("Reddit")

    def pega_dados_caminhoneiro(self):
        layout = [
            [sg.Text("CADASTRO DE CAMINHONEIRO", font=("Arial", 16, "bold"), justification="center", expand_x=True)],
            [sg.Text("Nome completo*", size=(20, 1)), sg.InputText(key="nome")],
            [sg.Text("CPF*", size=(20, 1)), sg.InputText(key="cpf")],
            [sg.Text("Email", size=(20, 1)), sg.InputText(key="email")],
            [sg.Text("CNH", size=(20, 1)), sg.InputText(key="num_cnh")],
            [sg.Text("Data de Nascimento*", size=(20, 1)), sg.InputText(key="data_nascimento")],
            [sg.Text("Telefone", size=(20, 1)), sg.InputText(key="telefone")],
            [sg.Text("Usuário*", size=(20, 1)), sg.InputText(key="usuario")],
            [sg.Text("Senha*", size=(20, 1)), sg.InputText(key="senha", password_char="*")],
            [sg.Checkbox("Possui MOPP", key="possui_MOPP")],
            [sg.Button("CADASTRAR", button_color=("white", "#5F41D9"), size=(15, 1)),
             sg.Button("VOLTAR", button_color=("white", "#C0C0C0"), size=(15, 1))],
        ]

        janela = sg.Window("Cadastro de Caminhoneiro", layout)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WINDOW_CLOSED, "VOLTAR"):
                janela.close()
                return None
            elif evento == "CADASTRAR":
                janela.close()
                return valores