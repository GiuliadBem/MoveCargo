import FreeSimpleGUI as sg

class TelaCadastroCaminhao:
    def __init__(self):
        sg.theme("Reddit")
            
    def pega_dados_caminhao(self):
            layout = [
                [sg.Text("Cadastro de Caminhão", font=("Arial", 16, "bold"), justification="center", expand_x=True)],
                [sg.Text("Placa:", size=(20, 1)), sg.InputText(key="placa")],
                [sg.Text("Modelo:", size=(20, 1)), sg.InputText(key="modelo")],
                [sg.Text("Marca:", size=(20, 1)), sg.InputText(key="marca")],
                [sg.Text("Ano:", size=(20, 1)), sg.InputText(key="ano")],
                [sg.Text("Capacidade:", size=(20, 1)), sg.InputText(key="capacidade")],
                [sg.Text("Tipo de Carga:", size=(20, 1)), sg.InputText(key="tipo_carga")],
                [sg.Button("Cadastrar", button_color=("white", "#5F41D9"), size=(15, 1)),
             sg.Button("Voltar", button_color=("white", "#C0C0C0"), size=(15, 1))]
            ]

            janela = sg.Window("Cadastro de Caminhão", layout)
            while True:
                evento, valores = janela.read()
                if evento in (sg.WINDOW_CLOSED, "Voltar"):
                    janela.close()
                    return None
                elif evento == "Cadastrar":
                    janela.close()
                    return valores
    