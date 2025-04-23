import FreeSimpleGUI as sg
from enums.tipo_carga import TipoCarga

class TelaCadastroCaminhao:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None # Armazena a própria janela de cadastro do caminhão
            
    def pega_dados_caminhao(self, caminhao=None):
        # Obter valores do enum para preencher a combobox
        tipos_carga = [tipo.name for tipo in TipoCarga]  # Obtem os nomes (SOLIDA, LIQUIDA, etc)

        # Define valores padrão (vazio para novo caminhão, dados existentes para edição)
        valores_padrao = {
            "placa": caminhao.placa if caminhao else "",
            "modelo": caminhao.modelo if caminhao else "",
            "marca": caminhao.marca if caminhao else "",
            "ano": caminhao.ano if caminhao else "",
            "capacidade": caminhao.capacidade if caminhao else "",
            "tipo_carga": caminhao.tipo_carga.name if caminhao else tipos_carga[0]
        }

        # Determinar a unidade inicial
        tipo_padrao = valores_padrao["tipo_carga"]
        unidade_inicial = "kg" if tipo_padrao in ["SOLIDA", "VIVA"] else "L"

        # Título da janela (Cadastro ou Edição)
        titulo = "Edição de Caminhão" if caminhao else "Cadastro de Caminhão"
        # Texto do botão principal
        texto_botao = "Atualizar" if caminhao else "Cadastrar"

        layout = [
            [sg.Text(titulo, font=("Arial", 16, "bold"), justification="center", expand_x=True)],
            [sg.Text("Placa:", size=(20, 1)), sg.InputText(key="placa", default_text=valores_padrao["placa"])],
            [sg.Text("Modelo:", size=(20, 1)), sg.InputText(key="modelo", default_text=valores_padrao["modelo"])],
            [sg.Text("Marca:", size=(20, 1)), sg.InputText(key="marca", default_text=valores_padrao["marca"])],
            [sg.Text("Ano:", size=(20, 1)), sg.InputText(key="ano", default_text=valores_padrao["ano"])],
            [sg.Text("Capacidade:", size=(20, 1)), sg.InputText(key="capacidade", default_text=valores_padrao["capacidade"], size=(15, 1)), sg.Text(unidade_inicial, key="unidade_medida", size=(3, 1))],
            [sg.Text("Tipo de Carga:", size=(20, 1)), sg.Combo(tipos_carga, default_value=valores_padrao["tipo_carga"], key="tipo_carga", size=(18, 1))],
            [sg.Button(texto_botao, button_color=("white", "#5F41D9"), size=(15, 1)),
            sg.Button("Voltar", button_color=("white", "#C0C0C0"), size=(15, 1))]
        ]

        self.__window = sg.Window(titulo, layout)

        while True:
            # valores é um dicionário que é retornado por window.read(), e contém todos os valores do input
            evento, valores = self.__window.read()

            # Atualizar a unidade de medida quando o tipo de carga mudar
            if evento == "tipo_carga":
                tipo_selecionado = valores["tipo_carga"]
                unidade = "kg" if tipo_selecionado in ["SOLIDA", "VIVA"] else "L"
                self.__window["unidade_medida"].update(unidade)
                
            if evento in (sg.WINDOW_CLOSED, "Voltar"):
                self.__window.close()
                return None
            elif evento == "Cadastrar" or evento == "Atualizar":
                self.__window.close()
                return valores
    
    def fechar(self):
        if self.__window:
            self.__window.close()
            self.__window = None