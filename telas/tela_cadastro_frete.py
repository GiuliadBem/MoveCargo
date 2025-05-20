import FreeSimpleGUI as sg
from enums.status import Status

class TelaCadastroFrete:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None  # Armazena a própria janela de cadastro de frete

    def pega_dados_frete(self, lista_caminhoneiros, lista_caminhoes, frete=None):
        observacoes_adicionadas = []
        
        # Mapas auxiliares para vincular nome formatado → objeto
        caminhoneiro_map = {f"{c.id} - {c.nome}": c for c in lista_caminhoneiros}
        caminhao_map = {f"{c.id} - {c.modelo} ({c.placa})": c for c in lista_caminhoes}
        
        caminhoneiro_opcoes = list(caminhoneiro_map.keys())
        caminhao_opcoes = list(caminhao_map.keys())
        status_opcoes = [s.name for s in Status]

        valores_padrao = {
            "origem": frete.origem if frete else "",
            "destino": frete.destino if frete else "",
            "distancia": frete.distancia if frete else "",
            "status": frete.status.name if frete else status_opcoes[0],
            "caminhoneiro": f"{frete.caminhoneiro.id} - {frete.caminhoneiro.nome}" if frete else '',
            "caminhao": f"{frete.caminhao.id} - {frete.caminhao.modelo} ({frete.caminhao.placa})" if frete else '',
            "carga": "",  # Pode ser um ID
        }
        
        if frete:
            self.__observacoes_adicionadas = [
                f"{obs.texto} - {obs.data.strftime('%H:%M - %d/%m/%Y')}" for obs in frete.observacoes
            ]

        titulo = "Edição de Frete" if frete else "Cadastro de Frete"
        texto_botao = "Atualizar" if frete else "Cadastrar"

        layout = [
            [sg.Text(titulo, font=("Arial", 16, "bold"), justification="center", expand_x=True)],
            [sg.Text("Origem:", size=(12, 1)), sg.InputText(key="origem", default_text=valores_padrao["origem"]),
             sg.Text("Destino:", size=(12, 1)), sg.InputText(key="destino", default_text=valores_padrao["destino"])],

            [sg.Text("Carga:", size=(12, 1)), sg.InputText(key="carga", default_text=valores_padrao["carga"], size=(32,1)),
             sg.Button("ADICIONAR CARGA", key="add_carga", size=(18,1))],

            [sg.Text("Distância (km):", size=(12, 1)), sg.InputText(key="distancia", default_text=str(valores_padrao["distancia"])),
             sg.Text("Caminhão:", size=(12, 1)), sg.Combo(caminhao_opcoes, default_value=valores_padrao["caminhao"], key="caminhao", size=(30, 1))],

            [sg.Text("Status:", size=(12, 1)), sg.Combo(status_opcoes, default_value=valores_padrao["status"], key="status", size=(20, 1)),
             sg.Text("Caminhoneiro:", size=(12, 1)), sg.Combo(caminhoneiro_opcoes, default_value=valores_padrao["caminhoneiro"], key="caminhoneiro", size=(30, 1))],
            

            [sg.Text("Observações:", size=(12, 1)), sg.Column([[sg.Multiline("\n".join(observacoes_adicionadas), size=(40, 4), disabled=True, key="observacoes_display")]], element_justification='left'),
             sg.Button("ADICIONAR OBSERVAÇÃO", key="add_observacao", size=(22, 2), button_color=("white", "#5F41D9"))],

            [sg.Push(), sg.Button("SALVAR ALTERAÇÕES", key=texto_botao, button_color=("white", "#5F41D9"), size=(20, 1)),
             sg.Button("VOLTAR", button_color=("white", "#C0C0C0"), size=(15, 1)), sg.Push()]
        ]

        self.__window = sg.Window(titulo, layout, resizable=True)

        while True:
            evento, valores = self.__window.read()
            
            if evento in (sg.WINDOW_CLOSED, "VOLTAR"):
                self.__window.close()
                return None
           
            elif evento in ("Cadastrar", "Atualizar"):
                # Valida campos obrigatórios antes de retornar
                campos_obrigatorios = ["origem", "destino", "distancia", "status", "caminhoneiro", "caminhao"] #Add carga depois

                for campo in campos_obrigatorios:
                    if not valores.get(campo) or valores[campo].strip() == "":
                        sg.popup(f"O campo '{campo}' é obrigatório.", title="Campo obrigatório")
                        break
                else:
                    # Se passou por todos os campos: retorna
                    valores["caminhoneiro"] = caminhoneiro_map.get(valores["caminhoneiro"])
                    valores["caminhao"] = caminhao_map.get(valores["caminhao"])
                    self.__window.close()
                    return valores
            
            elif evento == "add_observacao":
                sg.popup("Implementação depois")
                #nova_obs = sg.popup_get_text("Digite a nova observação:")
                #if nova_obs:
                    #from datetime import datetime
                    #texto_formatado = f"{nova_obs} - {datetime.now().strftime('%H:%M - %d/%m/%Y')}"
                    #self.__observacoes_adicionadas.append(texto_formatado)
                    #self.__window["observacoes_display"].update("\n".join(self.__observacoes_adicionadas))
            
            elif evento == "add_carga":
                sg.popup("Abrir formulário de carga separado aqui.")  # Aqui você pode chamar outra tela específica para Carga.

    def fechar(self):
        if self.__window:
            self.__window.close()
            self.__window = None
