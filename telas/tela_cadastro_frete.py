import FreeSimpleGUI as sg
from enums.status import Status
from enums.motivo_cancelamento import MotivoCancelamento
from datetime import datetime
#from controladores.controlador_carga import ControladorCarga --> isso aqui esta errado em um nivel
from enums.tipo_carga import TipoCarga

class TelaCadastroFrete:
    def __init__(self, controlador_frete=None):
        sg.theme("Reddit")
        self.__window = None  # Armazena a própria janela de cadastro de frete
        # self.__controlador_carga = ControladorCarga(self)
        self.__controlador_frete = controlador_frete  # Referência ao controlador de frete

    def __verificar_motivo_cancelamento(self, valores: dict) -> bool:
        """Verifica se o motivo do cancelamento foi informado quando necessário."""
        return not (valores["status"] == "CANCELADO" and not valores.get("motivo_cancelamento"))

    def __mostrar_erro_motivo_cancelamento(self):
        """Exibe mensagem de erro quando o motivo do cancelamento não foi informado."""
        sg.popup("É necessário informar o motivo do cancelamento!", title="Campo obrigatório")

    def atualizar_display_carga(self, carga):
        """Atualiza o display da carga na tela"""
        if self.__window and carga:
            self.__window["carga_display"].update(self.formatar_resumo_carga(carga))
            self.__carga_atual = carga  # Armazena a carga atual

    def mostrar_lista_cargas(self, lista_cargas):
        """Mostra uma janela com a lista de cargas disponíveis para seleção"""
        if not lista_cargas:
            sg.popup("Não há cargas cadastradas.", title="Aviso")
            return None

        # Preparar dados para a tabela
        dados_tabela = []
        for carga in lista_cargas:
            dados_tabela.append([
                carga.codigo,
                carga.descricao,
                f"{carga.quantidade} {self.get_unidade_medida(carga.tipo)}",
                carga.tipo.name,
                "Sim" if carga.carga_perigosa else "Não"
            ])

        layout = [
            [sg.Text('Selecione uma Carga', font=('Arial', 16, 'bold'))],
            [sg.Table(
                values=dados_tabela,
                headings=['Código', 'Descrição', 'Quantidade', 'Tipo', 'Perigosa'],
                display_row_numbers=False,
                auto_size_columns=True,
                num_rows=min(10, len(dados_tabela)),
                key='-TABELA-',
                enable_events=True,
                select_mode=sg.TABLE_SELECT_MODE_BROWSE
            )],
            [sg.Button('Selecionar', key='selecionar', size=(10, 1)),
             sg.Button('Nova Carga', key='nova_carga', size=(10, 1)),
             sg.Button('Cancelar', key='cancelar', size=(10, 1))]
        ]

        window = sg.Window('Selecionar Carga', layout, modal=True, finalize=True)
        
        while True:
            evento, valores = window.read()
            
            if evento in (sg.WINDOW_CLOSED, 'cancelar'):
                window.close()
                return None
                
            elif evento == 'nova_carga':
                window.close()
                return 'nova_carga'
                
            elif evento == 'selecionar' and valores['-TABELA-']:
                indice_selecionado = valores['-TABELA-'][0]
                carga_selecionada = lista_cargas[indice_selecionado]
                window.close()
                return carga_selecionada

    def get_unidade_medida(self, tipo_carga):
        """Retorna a unidade de medida baseada no tipo de carga"""
        if tipo_carga == TipoCarga.LIQUIDA:
            return "L"
        elif tipo_carga == TipoCarga.SOLIDA:
            return "Kg"
        elif tipo_carga == TipoCarga.GASOSA:
            return "M3"
        elif tipo_carga == TipoCarga.VIVA:
            return "Un"
        return ""

    def formatar_lista_cargas(self, lista_cargas):
        """Formata a lista de cargas para exibição"""
        if not lista_cargas:
            return "Nenhuma carga disponível."
        
        for carga in lista_cargas:
            if carga.tipo == TipoCarga.LIQUIDA:
                unidade = "L"
            elif carga.tipo == TipoCarga.SOLIDA:
                unidade = "Kg"
            elif carga.tipo == TipoCarga.GASOSA:
                unidade = "M3"
            elif carga.tipo == TipoCarga.VIVA:
                unidade = "Un"
            else:
                unidade = ""
            
            texto = f"{carga.codigo} - {carga.descricao} - {carga.quantidade} {unidade}"            
            if(carga.carga_perigosa):
                texto += " (PERIGOSA)"
            texto += "\n"

        return texto

    def pega_dados_frete(self, lista_caminhoneiros, lista_caminhoes, frete=None, modo_atualizacao_status=False):
        observacoes_adicionadas = []
        self.__carga_atual = frete.carga if frete else None  # Armazena a carga atual
        
        # Mapas auxiliares para vincular nome formatado → objeto
        caminhoneiro_map = {f"{c.id} - {c.nome}": c for c in lista_caminhoneiros}
        caminhao_map = {f"{c.id} - {c.modelo} ({c.placa})": c for c in lista_caminhoes}
        
        caminhoneiro_opcoes = list(caminhoneiro_map.keys())
        caminhao_opcoes = list(caminhao_map.keys())
        status_opcoes = [s.name for s in Status]
        motivo_opcoes = [m.name for m in MotivoCancelamento]

        # Obter lista de cargas disponíveis
        lista_cargas = []
        if self.__controlador_frete:
            lista_cargas = self.__controlador_frete.obter_lista_cargas()

        valores_padrao = {
            "origem": frete.origem if frete else "",
            "destino": frete.destino if frete else "",
            "distancia": frete.distancia if frete else "",
            "status": frete.status.name if frete else status_opcoes[0],
            "caminhoneiro": f"{frete.caminhoneiro.id} - {frete.caminhoneiro.nome}" if frete else '',
            "caminhao": f"{frete.caminhao.id} - {frete.caminhao.modelo} ({frete.caminhao.placa})" if frete else '',
            "carga": self.formatar_lista_cargas(lista_cargas) if lista_cargas else "Nenhuma carga disponível.",
            "motivo_cancelamento": frete.motivo_cancelamento.name if frete and frete.motivo_cancelamento else "",
            "prazo_entrega": frete.prazo_entrega.strftime("%d/%m/%Y %H:%M") if frete and frete.prazo_entrega else ""
        }
        
        if frete:
            self.__observacoes_adicionadas = [
                f"{obs.texto} - {obs.data.strftime('%H:%M - %d/%m/%Y')}" for obs in frete.observacoes
            ]

        # Define o título e texto do botão baseado no modo
        if modo_atualizacao_status:
            titulo = "Atualizar Status do Frete"
            texto_botao = "Atualizar Status"
        else:
            titulo = "Edição de Frete" if frete else "Cadastro de Frete"
            texto_botao = "Atualizar" if frete else "Cadastrar"

        # Layout base
        layout = [
            [sg.Text(titulo, font=("Arial", 16, "bold"), justification="center", expand_x=True)],
            [sg.Text("Origem:", size=(20, 1)), 
             sg.InputText(key="origem", default_text=valores_padrao["origem"], 
                         text_color="gray" if modo_atualizacao_status else None,
                         disabled=modo_atualizacao_status)],
            [sg.Text("Destino:", size=(20, 1)), 
             sg.InputText(key="destino", default_text=valores_padrao["destino"], 
                         text_color="gray" if modo_atualizacao_status else None,
                         disabled=modo_atualizacao_status)],
            
            [sg.Text("Carga:", size=(20, 1)),
             sg.Multiline(default_text=valores_padrao["carga"], size=(40, 4), 
                         text_color="gray" if modo_atualizacao_status else None,
                         disabled=True, key="carga_display"),
             sg.Button("ADICIONAR CARGA", key="add_carga", size=(15, 1), disabled=modo_atualizacao_status)],
            
            [sg.Text("Distância (km):", size=(20, 1)), 
             sg.InputText(key="distancia", default_text=str(valores_padrao["distancia"]), 
                         text_color="gray" if modo_atualizacao_status else None,
                         disabled=modo_atualizacao_status)],
            
            # Status
            [sg.Text("Status:", size=(20, 1)), 
             sg.Combo(status_opcoes, default_value=valores_padrao["status"], 
                     key="status", size=(18, 1), readonly=True, enable_events=True, disabled= not modo_atualizacao_status)],
            
            # Motivo do cancelamento (inicialmente invisível)
            [sg.Text("Motivo do Cancelamento:", size=(20, 1), key="motivo_label", visible=False),
             sg.Combo(motivo_opcoes, default_value=valores_padrao["motivo_cancelamento"],
                     key="motivo_cancelamento", size=(25, 1), readonly=True, visible=False,
                     text_color="gray" if modo_atualizacao_status else None)],
            
            [sg.Text("Caminhoneiro:", size=(20, 1)), 
             sg.Combo(caminhoneiro_opcoes, default_value=valores_padrao["caminhoneiro"], 
                     key="caminhoneiro", size=(30, 1), 
                     text_color="gray" if modo_atualizacao_status else None,
                     disabled=modo_atualizacao_status)],
            [sg.Text("Caminhão:", size=(20, 1)), 
             sg.Combo(caminhao_opcoes, default_value=valores_padrao["caminhao"], 
                     key="caminhao", size=(30, 1), 
                     text_color="gray" if modo_atualizacao_status else None,
                     disabled=modo_atualizacao_status)],
            
            [sg.Text("Prazo de Entrega:", size=(20, 1)),
             sg.InputText(key="prazo_entrega", default_text=valores_padrao["prazo_entrega"].split(" ")[0] if valores_padrao["prazo_entrega"] else "",
                         text_color="gray" if modo_atualizacao_status else None,
                         disabled=modo_atualizacao_status, size=(18, 1)),
             sg.CalendarButton("📅", target="prazo_entrega", format="%d/%m/%Y", 
                             disabled=modo_atualizacao_status),
             sg.InputText(key="hora_entrega", default_text=valores_padrao["prazo_entrega"].split(" ")[1] if valores_padrao["prazo_entrega"] else "",
                         text_color="gray" if modo_atualizacao_status else None,
                         disabled=modo_atualizacao_status, size=(8, 1)),
             sg.Text("(HH:MM)", size=(8, 1), text_color="gray")],
            
            [sg.Text("Observações:", size=(20, 1)),
             sg.Multiline("\n".join(observacoes_adicionadas), size=(25, 4), 
                         text_color="gray" if modo_atualizacao_status else None,
                         disabled=True, key="observacoes_display"),
             sg.Button("ADICIONAR OBSERVAÇÃO", key="add_observacao", size=(20, 1), disabled=modo_atualizacao_status)],
            
            [sg.Button(texto_botao, button_color=("white", "#5F41D9"), size=(15, 1)),
            sg.Button("Voltar", button_color=("white", "#C0C0C0"), size=(15, 1))]
        ]

        self.__window = sg.Window(titulo, layout, size=(650, 450), resizable=True, finalize=True)

        # Mostra o campo de motivo se o status inicial for CANCELADO
        if valores_padrao["status"] == "CANCELADO":
            self.__window["motivo_label"].update(visible=True)
            self.__window["motivo_cancelamento"].update(visible=True)
        else:
            self.__window["motivo_label"].update(visible=False)
            self.__window["motivo_cancelamento"].update(visible=False)

        while True:
            evento, valores = self.__window.read()
            
            if evento in (sg.WINDOW_CLOSED, "Voltar"):
                self.__window.close()
                return None
            
            elif evento == "status":
                # Mostra/esconde o campo de motivo do cancelamento baseado no status selecionado
                if valores["status"] == "CANCELADO":
                    self.__window["motivo_label"].update(visible=True)
                    self.__window["motivo_cancelamento"].update(visible=True, value="", 
                                                              text_color="gray" if modo_atualizacao_status else None)
                else:
                    self.__window["motivo_label"].update(visible=False)
                    self.__window["motivo_cancelamento"].update(visible=False, value="", 
                                                              text_color="gray" if modo_atualizacao_status else None)
            
            elif evento in ("Cadastrar", "Atualizar", "Atualizar Status"):
                # Valida campos obrigatórios apenas se não estiver no modo de atualização de status
                if not modo_atualizacao_status:
                    campos_obrigatorios = ["origem", "destino", "distancia", "status", "caminhoneiro", "caminhao", "prazo_entrega", "hora_entrega"] #COLOCAR CARGA POSTERIORMENTE

                    for campo in campos_obrigatorios:
                        if not valores.get(campo) or valores[campo].strip() == "":
                            sg.popup(f"O campo '{campo}' é obrigatório.", title="Campo obrigatório")
                            break
                    else:
                        # Se passou por todos os campos: retorna
                        valores["caminhoneiro"] = caminhoneiro_map.get(valores["caminhoneiro"])
                        valores["caminhao"] = caminhao_map.get(valores["caminhao"])
                        valores["carga"] = self.__carga_atual  # Inclui a carga atual nos valores retornados
                        
                        # Converte a string da data e hora para objeto datetime
                        try:
                            data_hora = f"{valores['prazo_entrega']} {valores['hora_entrega']}"
                            valores["prazo_entrega"] = datetime.strptime(data_hora, "%d/%m/%Y %H:%M")
                        except ValueError:
                            sg.popup("Formato de data/hora inválido. Use o formato dd/mm/aaaa HH:MM.", title="Erro")
                            continue
                        
                        self.__window.close()
                        return valores
                else:
                    # No modo de atualização de status, valida o motivo do cancelamento se necessário
                    motivo = self.__verificar_motivo_cancelamento(valores)

                    if not motivo:
                        self.__mostrar_erro_motivo_cancelamento()
                        continue
                    
                    # Se passou pela validação, retorna os valores
                    valores["caminhoneiro"] = caminhoneiro_map.get(valores["caminhoneiro"])
                    valores["caminhao"] = caminhao_map.get(valores["caminhao"])
                    self.__window.close()
                    return valores
            
            elif evento == "add_observacao":
                sg.popup("Implementação depois")
            
            elif evento == "add_carga":
                # carga = self.controlador_carga.inclui_carga()
                valores["carga"] = ""
                break
                
                if self.__controlador_frete:
                    carga = self.__controlador_frete.abrir_cadastro_carga()
                    if carga:
                        self.__carga_atual = carga  # Atualiza a carga atual
                        self.atualizar_display_carga(carga)
                else:
                    sg.popup_error("Erro: Controlador de frete não inicializado")

    def formatar_resumo_carga(self, carga):
        if not carga:
            return "Nenhuma carga definida."
        if(carga.tipo == TipoCarga.LIQUIDA):
            unidade_medida = "L"
        elif(carga.tipo == TipoCarga.SOLIDA):
            unidade_medida = "Kg"
        elif(carga.tipo == TipoCarga.GASOSA):
            unidade_medida = "M3"
        elif(carga.tipo == TipoCarga.VIVA):
            unidade_medida = "Un"
        else:
            unidade_medida = ""
        return (f"{carga.codigo} - {carga.tipo} ({carga.quantidade} {unidade_medida})")

    def fechar(self):
        if self.__window:
            self.__window.close()
            self.__window = None
