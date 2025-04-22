import FreeSimpleGUI as sg
from enums.tipo_carga import TipoCarga

class TelaCadastroCaminhao:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None # Armazena a própria janela de cadastro do caminhão
            
    def pega_dados_caminhao(self):
        # Obter valores do enum para preencher a combobox
        tipos_carga = [tipo.name for tipo in TipoCarga]  # Obtem os nomes (SOLIDO, LIQUIDO, etc)
        
        layout = [
            [sg.Text("Cadastro de Caminhão", font=("Arial", 16, "bold"), justification="center", expand_x=True)],
            [sg.Text("Placa:", size=(20, 1)), sg.InputText(key="placa")],
            [sg.Text("Modelo:", size=(20, 1)), sg.InputText(key="modelo")],
            [sg.Text("Marca:", size=(20, 1)), sg.InputText(key="marca")],
            [sg.Text("Ano:", size=(20, 1)), sg.InputText(key="ano")],
            [sg.Text("Capacidade:", size=(20, 1)), sg.InputText(key="capacidade")],
            [sg.Text("Tipo de Carga:", size=(20, 1)), sg.Combo(tipos_carga, default_value=tipos_carga[0], key="tipo_carga", size=(18, 1))],
            [sg.Button("Cadastrar", button_color=("white", "#5F41D9"), size=(15, 1)),
            sg.Button("Voltar", button_color=("white", "#C0C0C0"), size=(15, 1))]
        ]

        self.__window = sg.Window("Cadastro de Caminhão", layout)
        while True:
            # valores é um dicionário que é retornado por window.read(), e contém todos os valores do input
            evento, valores = self.__window.read()
            if evento in (sg.WINDOW_CLOSED, "Voltar"):
                self.__window.close()
                return None
            elif evento == "Cadastrar":
                self.__window.close()
                return valores
    
    def fechar(self):
        if self.__window:
            self.__window.close()
            self.__window = None