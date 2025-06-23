import FreeSimpleGUI as sg
from enums.status import Status
from enums.motivo_cancelamento import MotivoCancelamento
from datetime import datetime
from enums.tipo_carga import TipoCarga

class TelaCadastroFrete:
    def __init__(self, controlador_frete=None):
        sg.theme("Reddit")
        self.__window = None  # Armazena a própria janela de cadastro de frete
        self.__controlador_frete = controlador_frete  # Referência ao controlador de frete

    def __verificar_motivo_cancelamento(self, valores: dict) -> bool:
        """Verifica se o motivo do cancelamento foi informado quando necessário."""
        return not (valores["status"] == "CANCELADO" and not valores.get("motivo_cancelamento"))

    def __mostrar_erro_motivo_cancelamento(self):
        """Exibe mensagem de erro quando o motivo do cancelamento não foi informado."""
        sg.popup("É necessário informar o motivo do cancelamento!", title="Campo obrigatório")

    def __obter_status_validos_para_transicao(self, status_atual):
        """
        Retorna a lista de status válidos para transição a partir do status atual.
        Evita importação circular com o controlador.
        """
        from enums.status import Status
        
        transicoes_permitidas = {
            Status.NAO_INICIADO: [Status.EM_ANDAMENTO, Status.CANCELADO],
            Status.EM_ANDAMENTO: [Status.SUSPENSO, Status.CONCLUIDO, Status.CANCELADO],
            Status.SUSPENSO: [Status.EM_ANDAMENTO, Status.CANCELADO],
            Status.CONCLUIDO: [],
            Status.CANCELADO: []
        }
        
        return transicoes_permitidas.get(status_atual, [])

    def __validar_transicao_status(self, status_atual, novo_status):
        """
        Valida se a transição de status é permitida.
        Retorna (é_válido, mensagem_erro)
        """
        from enums.status import Status
        from datetime import datetime
        
        # Verificar se é uma transição válida
        status_validos = self.__obter_status_validos_para_transicao(status_atual)
        if novo_status not in status_validos:
            return False, f"Transição de '{status_atual.value}' para '{novo_status.value}' não é permitida."
        
        # Verificar se o frete não está em estado final
        if status_atual in [Status.CONCLUIDO, Status.CANCELADO]:
            return False, f"Frete já está {status_atual.value.lower()}. Não é possível alterar o status."
        
        return True, ""

    def atualizar_carga_na_interface(self, janela: sg.Window, carga, modo_atualizacao_status: bool):
        """Atualiza a exibição da carga na interface, mostrando todos os atributos de forma compacta (até 2 linhas)."""
        self.__carga_atual = carga
        if carga:
            unidade = self.get_unidade_medida(carga.tipo)
            texto = (
                f"Código: {carga.codigo} | Tipo: {carga.tipo.name} ({carga.tipo.value}) | Desc: {carga.descricao} | "
                f"Qtde: {carga.quantidade} {unidade} | Perigosa: {'Sim' if carga.carga_perigosa else 'Não'}"
            )
        else:
            texto = "Nenhuma carga cadastrada."

        if janela is not None and "carga_display" in janela.AllKeysDict:
            janela["carga_display"].update(value=texto)

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


    def pega_dados_frete(self, lista_caminhoneiros, lista_caminhoes, frete=None, modo_atualizacao_status=False):
        observacoes_adicionadas = []
        self.__carga_atual = frete.carga if frete else None  # Armazena a carga atual
        
        # Mapas auxiliares para vincular nome formatado → objeto
        caminhoneiro_map = {f"{c.id} - {c.nome}": c for c in lista_caminhoneiros}
        caminhao_map = {f"{c.id} - {c.modelo} ({c.placa})": c for c in lista_caminhoes}
        
        caminhoneiro_opcoes = list(caminhoneiro_map.keys())
        caminhao_opcoes = list(caminhao_map.keys())
        # Definir opções de status baseado no modo e status atual
        if modo_atualizacao_status and frete:
            # No modo de atualização, mostrar apenas status válidos para transição
            status_validos = self.__obter_status_validos_para_transicao(frete.status)
            status_opcoes = [s.name for s in status_validos]
            
            # Se não há transições válidas, mostrar mensagem
            if not status_opcoes:
                sg.popup(f"Este frete está {frete.status.value.lower()}. Não é possível alterar o status.", 
                        title="Status Final")
                return None
        else:
            # No modo de cadastro, mostrar todos os status
            from enums.status import Status
            status_opcoes = [s.name for s in Status]
        
        motivo_opcoes = [m.name for m in MotivoCancelamento]


        valores_padrao = {
            "origem": frete.origem if frete else "",
            "destino": frete.destino if frete else "",
            "distancia": frete.distancia if frete else "",
            "status": frete.status.name if frete else status_opcoes[0],
            "caminhoneiro": f"{frete.caminhoneiro.id} - {frete.caminhoneiro.nome}" if frete else '',
            "caminhao": f"{frete.caminhao.id} - {frete.caminhao.modelo} ({frete.caminhao.placa})" if frete else '',
            "carga":  frete.carga if frete else "Nenhuma carga cadastrada",
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
            
            [sg.Text("Carga:", size=(20, 1))],
            [sg.Multiline("", size=(70, 2), key="carga_display", disabled=True, no_scrollbar=True)],
            [sg.Button("ADICIONAR CARGA", key="add_carga", size=(20, 1), disabled=modo_atualizacao_status),
            sg.Button("Excluir", key="excluir_carga", size=(10, 1), disabled=modo_atualizacao_status)],
            
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
        
        if frete:
            self.atualizar_carga_na_interface(self.__window, self.__carga_atual, modo_atualizacao_status)

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
                valores["carga"] = self.__carga_atual
                if not modo_atualizacao_status:
                    campos_obrigatorios = ["origem", "destino", "distancia", "status", "caminhoneiro","caminhao","prazo_entrega", "hora_entrega"] 

                    vef_campos = self.verificar_campos(valores, campos_obrigatorios)
                    print(valores)  
                    if vef_campos:
                        sg.popup(vef_campos, title="Campo obrigatório")
                        continue
                    else:
                        # Caminhoneiro
                        if not valores.get("caminhoneiro") or valores["caminhoneiro"] == valores_padrao["caminhoneiro"]:
                            valores["caminhoneiro"] = valores["caminhoneiro"] = frete.caminhoneiro  # mantém o objeto original do frete
                        else:
                            valores["caminhoneiro"] = caminhoneiro_map[valores["caminhoneiro"]]

                        # Caminhão
                        if not valores.get("caminhao") or valores["caminhao"] == valores_padrao["caminhao"]:
                            valores["caminhao"] = frete.caminhao  # mantém o objeto original do frete
                        else:
                            valores["caminhao"] = caminhao_map[valores["caminhao"]]
                       
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
                    
                    # Validar se o status selecionado é válido para transição
                    if frete and valores["status"] != frete.status.name:
                        from enums.status import Status
                        novo_status = Status[valores["status"]]
                        eh_valido, mensagem_erro = self.__validar_transicao_status(frete.status, novo_status)
                        
                        if not eh_valido:
                            sg.popup(mensagem_erro, title="Transição Inválida")
                            continue
                    
                    # Se passou pela validação, retorna os valores
                    valores["caminhoneiro"] = caminhoneiro_map.get(valores["caminhoneiro"])
                    valores["caminhao"] = caminhao_map.get(valores["caminhao"])
                    self.__window.close()
                    return valores
            
            elif evento == "add_observacao":
                sg.popup("Implementação depois")
            
            elif evento == "add_carga":
                if self.__controlador_frete:
                    carga = self.__controlador_frete.abrir_cadastro_carga()
                    print("Carga retornada:", carga)  # DEBUG
                if carga:
                    self.atualizar_carga_na_interface(self.__window, carga, modo_atualizacao_status)

            elif evento == "excluir_carga":
                # Confirmação antes de excluir a carga, com código e botões em português
                if self.__carga_atual:
                    resposta = sg.popup(
                        f"Tem certeza que deseja excluir a carga com o código {self.__carga_atual.codigo}?",
                        title="Confirmar Exclusão",
                        custom_text=("Sim", "Não")
                    )
                    if resposta == "Sim":
                        self.__carga_atual = None
                        self.atualizar_carga_na_interface(self.__window, None, modo_atualizacao_status)
    
    def verificar_campos(self,valores, campos_obrigatorios):
        for campo in campos_obrigatorios:
            if not valores.get("carga"):
                mensagem = "é obrigatório cadastrar uma carga."
                return mensagem
            if not valores.get(campo) or valores[campo].strip() == "":
                mensagem = f"O campo '{campo}' é obrigatório."
                return mensagem
        return None

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
   