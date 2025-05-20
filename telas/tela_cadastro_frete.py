import FreeSimpleGUI as sg
from enums.status import Status

class TelaCadastroFrete:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None  # Armazena a própria janela de cadastro de frete

    def pega_dados_cadastro(self, lista_caminhoneiros, lista_caminhoes, frete=None, modo_atualizacao_status=False):
        status_opcoes = [s.name for s in Status]
        caminhoneiro_opcoes = [f"{cm.id} - {cm.nome}" for cm in lista_caminhoneiros]
        caminhao_opcoes = [f"{c.id} - {c.modelo} ({c.placa})" for c in lista_caminhoes]

        valores_padrao = {
            "origem": frete.origem if frete else "",
            "destino": frete.destino if frete else "",
            "distancia": frete.distancia if frete else "",
            "status": frete.status.name if frete else status_opcoes[0],
            "caminhoneiro": f"{frete.caminhoneiro.id} - {frete.caminhoneiro.nome}" if frete else caminhoneiro_opcoes[0],
            "caminhao": f"{frete.caminhao.id} - {frete.caminhao.modelo} ({frete.caminhao.placa})" if frete else caminhao_opcoes[0],
        }

        # Define o título e texto do botão baseado no modo
        if modo_atualizacao_status:
            titulo = "Atualizar Status do Frete"
            texto_botao = "Atualizar Status"
        else:
            titulo = "Edição de Frete" if frete else "Cadastro de Frete"
            texto_botao = "Atualizar" if frete else "Cadastrar"

        layout = [
            [sg.Text(titulo, font=("Arial", 16, "bold"), justification="center", expand_x=True)],
            [sg.Text("Origem:", size=(20, 1)), 
            sg.InputText(key="origem", default_text=valores_padrao["origem"], 
                        disabled=modo_atualizacao_status)],
            [sg.Text("Destino:", size=(20, 1)), 
            sg.InputText(key="destino", default_text=valores_padrao["destino"], 
                        disabled=modo_atualizacao_status)],
            [sg.Text("Distância (km):", size=(20, 1)), 
            sg.InputText(key="distancia", default_text=str(valores_padrao["distancia"]), 
                        disabled=modo_atualizacao_status)],
            [sg.Text("Status:", size=(20, 1)), 
            sg.Combo(status_opcoes, default_value=valores_padrao["status"], 
                    key="status", size=(18, 1))],
            [sg.Text("Caminhoneiro:", size=(20, 1)), 
            sg.Combo(caminhoneiro_opcoes, default_value=valores_padrao["caminhoneiro"], 
                    key="caminhoneiro", size=(30, 1), disabled=modo_atualizacao_status)],
            [sg.Text("Caminhão:", size=(20, 1)), 
            sg.Combo(caminhao_opcoes, default_value=valores_padrao["caminhao"], 
                    key="caminhao", size=(30, 1), disabled=modo_atualizacao_status)],
            [sg.Button(texto_botao, button_color=("white", "#5F41D9"), size=(15, 1)),
            sg.Button("Voltar", button_color=("white", "#C0C0C0"), size=(15, 1))]
        ]

        self.__window = sg.Window(titulo, layout)

        while True:
            evento, valores = self.__window.read()
            if evento in (sg.WINDOW_CLOSED, "Voltar"):
                self.__window.close()
                return None
            elif evento in ("Cadastrar", "Atualizar", "Atualizar Status"):
                self.__window.close()
                return valores

    def fechar(self):
        if self.__window:
            self.__window.close()
            self.__window = None
