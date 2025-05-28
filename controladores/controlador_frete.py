from telas.tela_fretes import TelaFrete
from telas.tela_cadastro_frete import TelaCadastroFrete
from telas.tela_atualizacao_status import TelaAtualizacaoStatus
from modelos.frete import Frete
from daos.frete_dao import FreteDAO
from enums.status import Status
from enums.motivo_cancelamento import MotivoCancelamento
from datetime import datetime

class ControladorFrete:
    def __init__(self, controlador_sistema):
        self.__frete_dao = FreteDAO()
        self.__tela_frete = TelaFrete()
        self.__tela_cadastro_frete = TelaCadastroFrete(self)
        self.__tela_atualizacao_status = TelaAtualizacaoStatus()
        self.__controlador_sistema = controlador_sistema

    @property
    def lista_fretes(self):
        return self.__frete_dao.get_all()

    def procura_frete_por_id(self, id):
        for frete in self.lista_fretes:
            if frete.id == id:
                return frete
        return None

    def incluir_frete(self):
        
        lista_caminhoes = self.__controlador_sistema.controlador_caminhao.lista_caminhoes
        lista_caminhoneiros = self.__controlador_sistema.controlador_caminhoneiro.lista_caminhoneiros
        lista_caminhoes_livres = self.lista_caminhoes_livres(lista_caminhoes)
        lista_caminhoneiros_livres = self.lista_caminhoneiros_livres(lista_caminhoneiros)
        
        dados = self.__tela_cadastro_frete.pega_dados_frete(lista_caminhoneiros_livres, lista_caminhoes_livres)
        
        if dados == None:
            self.__tela_frete.mostrar_mensagem("Cadastro cancelado.")
            return

        try:
            cria_id = len(self.lista_fretes)
            while self.procura_frete_por_id(cria_id) is not None:
                cria_id += 1

            # Temporariamente, vamos usar uma carga vazia e sem observacoes
            carga = None  #carga = dados["carga"]
            observacoes = ""  # [Observacao(**obs) for obs in dados.get("observacoes", [])] 
            caminhao = dados["caminhao"]
            caminhoneiro = dados["caminhoneiro"]

            #vef_carga = self.verifica_tipo_carga(carga, caminhao)
            #if not vef_carga:
             #   self.__tela_frete.mostrar_mensagem("Erro: Caminhão incompatível com o tipo de carga.")
             #   return
            
           # vef_mopp = self.verifica_Mopp(carga, caminhoneiro)
            #if not vef_mopp:
              #  self.__tela_frete.mostrar_mensagem("Caminhoneiro não possui licença MOPP para carga perigosa.")
            #    return

            novo_frete = Frete(
                id=cria_id,
                origem=dados["origem"],
                destino=dados["destino"],
                motivo_cancelamento=None,
                distancia=dados["distancia"],
                status=Status.NAO_INICIADO,
                observacoes=observacoes,
                caminhoneiro=caminhoneiro,
                caminhao=caminhao,
                carga=carga,
                prazo_entrega=dados["prazo_entrega"]
            )

            self.__frete_dao.add(novo_frete)
            self.__tela_frete.mostrar_mensagem("Frete cadastrado com sucesso!")

        except (KeyError, ValueError, TypeError) as erro:
            self.__tela_frete.mostrar_mensagem(f"Erro ao cadastrar frete: {erro}")

    def atualizar_frete(self, id_frete):
        frete = self.procura_frete_por_id(id_frete)

        if not frete:
            self.__tela_frete.mostrar_mensagem("Frete não encontrado.")
            return
    
        lista_caminhoes = self.__controlador_sistema.controlador_caminhao.lista_caminhoes
        lista_caminhoneiros = self.__controlador_sistema.controlador_caminhoneiro.lista_caminhoneiros
        lista_caminhoes_livres = self.lista_caminhoes_livres(lista_caminhoes)
        lista_caminhoneiros_livres = self.lista_caminhoneiros_livres(lista_caminhoneiros)
        
        novos_dados = self.__tela_cadastro_frete.pega_dados_frete(lista_caminhoneiros_livres, lista_caminhoes_livres, frete)

        if novos_dados is None:
            self.__tela_frete.mostrar_mensagem("Atualização cancelada.")
            return

        try:

            # Temporariamente, vamos usar uma carga vazia e sem observacoes
            carga = None  #carga = dados["carga"]
            observacoes = ""  # [Observacao(**obs) for obs in dados.get("observacoes", [])] 
            caminhao = novos_dados["caminhao"]
            caminhoneiro = novos_dados["caminhoneiro"]


            #vef_carga = self.verifica_tipo_carga(carga, caminhao)
            #vef_capacidade = self.verifica_capacidade(carga, caminhao)
            #if not vef_carga:
            #    self.__tela_frete.mostrar_mensagem("Caminhão incompatível com o tipo de carga.")
            #    return
            #elif not vef_capacidade:
            #    self.__tela_frete.mostrar_mensagem("Carga maior que capacidade do Caminhão")
            #    return
            
           # vef_mopp = self.verifica_Mopp(carga, caminhoneiro)
            #if not vef_mopp:
            #    self.__tela_frete.mostrar_mensagem("Caminhoneiro não possui licença MOPP para carga perigosa.")
            #    return

            frete.origem = novos_dados.get("origem", frete.origem)
            frete.destino = novos_dados.get("destino", frete.destino)
            frete.distancia = novos_dados.get("distancia", frete.distancia)
            frete.prazo_entrega = novos_dados.get("prazo_entrega", frete.distancia)
            frete.caminhoneiro = caminhoneiro
            frete.caminhao = caminhao
            frete.carga = carga
            frete.observacoes = observacoes
               
            self.__frete_dao.update(frete)
            self.__tela_frete.mostrar_mensagem("Frete atualizado com sucesso!")

        except Exception as e:
            self.__tela_frete.mostrar_mensagem(f"Erro ao atualizar frete: {e}")

    def excluir_frete(self, id):
        id_frete = id

        if id_frete is None:
            self.__tela_frete.mostrar_mensagem("Nenhum frete selecionado.")
            return

        frete = self.procura_frete_por_id(id_frete)
        if not frete:
            self.__tela_frete.mostrar_mensagem("Frete não encontrado.")
            return

        if self.__tela_frete.confirmar_exclusao(frete.id):
            self.__frete_dao.remove(id_frete)
            self.__tela_frete.mostrar_mensagem("Frete excluído com sucesso!")
        else:
            self.__tela_frete.mostrar_mensagem("Exclusão cancelada.")

    def listar_fretes_gerente(self):
        dados_exibicao = []

        for frete in self.lista_fretes:
            dados_exibicao.append({
                "id": frete.id,
                #"carga": frete.carga.tipo.name,
                "caminhoneiro": frete.caminhoneiro.nome,
                "status": frete.status.name,
                "prazo_entrega": frete.prazo_entrega
            })
        return dados_exibicao
    
    # Validação de compatibilidade caminhão/carga
    def verifica_tipo_carga(self, carga, caminhao):
        tipo_carga = carga.tipo_carga
        tipo_carga_caminhao = caminhao.tipo_carga
        
        if tipo_carga != tipo_carga_caminhao:
            return False
        
    # Validação de carga perigosa
    def verifica_Mopp(self, carga, caminhoneiro):
        caminhoneiro_mopp = caminhoneiro.possui_MOPP
        
        if carga.perigosa and not caminhoneiro_mopp: #Verificar qual será o metodo 
            return False
    
    #Validação da capacidade
    def verifica_capacidade(self, carga, caminhao):
        if carga.quantidade > caminhao.capacidade:
            return False
    
    def lista_caminhoneiros_livres(self, lista_caminhoneiro):
        lista_caminhoneiros_livres = []
        for c in lista_caminhoneiro:
            id_caminhoneiro = c.id
            frete_atual = None
            for f in self.lista_fretes:
                if f.caminhoneiro.id == id_caminhoneiro and f.status in [Status.NAO_INICIADO, Status.EM_ANDAMENTO, Status.SUSPENSO]:
                    frete_atual = f
            if frete_atual == None:
                lista_caminhoneiros_livres.append(c)
        return lista_caminhoneiros_livres
    
    def lista_caminhoes_livres(self, lista_caminhao):
        lista_caminhoes_livres = []
        for c in lista_caminhao:
            id_caminhao = c.id
            frete_atual = None
            for f in self.lista_fretes:
                if f.caminhao.id == id_caminhao and f.status in [Status.NAO_INICIADO, Status.EM_ANDAMENTO, Status.SUSPENSO]:
                    frete_atual = f
            if frete_atual == None:
                lista_caminhoes_livres.append(c)
        return lista_caminhoes_livres



    # -- Atualizar Status Frete ----------------------------------------------------------------------------------------------------------------------------------------------- #
    def listar_fretes_para_atualizacao_gerente(self):
        dados_exibicao = []

        for frete in self.lista_fretes:
            # Verifica se o prazo expirou e se o frete não está finalizado
            if (frete.prazo_entrega and datetime.now() > frete.prazo_entrega and 
                frete.status not in [Status.CONCLUIDO, Status.CANCELADO]):
                dados_exibicao.append({
                    "id": frete.id,
                    #"carga": frete.carga.tipo.name,
                    "caminhoneiro": frete.caminhoneiro.nome,
                    "origem": frete.origem,
                    "destino": frete.destino,
                    "status": frete.status.name,
                    "prazo_entrega": frete.prazo_entrega
                })
        return dados_exibicao
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def opcoes_frete(self, usuario, modo_atualizacao_status=False):
        while True:
            if usuario == "Gerente":
                if modo_atualizacao_status:
                    lista_fretes = self.listar_fretes_para_atualizacao_gerente()
                    opcao = self.__tela_atualizacao_status.mostrar_fretes_para_atualizacao(lista_fretes, perfil="gerente")
                else:
                    opcao = self.__tela_frete.mostrar_fretes(self.listar_fretes_gerente(), "gerente")

            if opcao == "cadastrar":
                self.incluir_frete()

            elif isinstance(opcao, dict) and "acao" in opcao:
                id_frete = opcao.get("id")

                if opcao["acao"] == "editar":
                    self.atualizar_frete(id_frete)
                elif opcao["acao"] == "excluir":
                    self.excluir_frete(id_frete)
                elif opcao["acao"] == "atualizar" and modo_atualizacao_status:
                    self.atualizar_status_frete_gerente(id_frete)

            elif opcao == "voltar":
                break

    # -- Atualizar Status do Frete -------------------------------------------------------------------------------------------------------------------------------------- #
    def atualizar_status_frete(self, id_frete):
        frete = self.procura_frete_por_id(id_frete)

        if not frete:
            self.__tela_frete.mostrar_mensagem("Frete não encontrado.")
            return

        # Verificar se o frete pertence ao caminhoneiro logado
        if frete.caminhoneiro.id != self.__controlador_sistema.sessao.usuario_atual.id:
            self.__tela_frete.mostrar_mensagem("Você não tem permissão para atualizar este frete.")
            return

        # Verificar se o frete está ativo
        if frete.status not in [Status.NAO_INICIADO, Status.EM_ANDAMENTO, Status.SUSPENSO]:
            self.__tela_frete.mostrar_mensagem("Este frete não está ativo.")
            return

        # Verificar se o prazo expirou
        if frete.prazo_entrega and datetime.now() > frete.prazo_entrega:
            self.__tela_frete.mostrar_mensagem("O prazo de entrega expirou. Apenas o gerente pode atualizar o status.")
            return

        # Obter os novos dados usando a tela de cadastro em modo de atualização de status
        dados = self.__tela_cadastro_frete.pega_dados_frete(
            self.__controlador_sistema.controlador_caminhoneiro.lista_caminhoneiros,
            self.__controlador_sistema.controlador_caminhao.lista_caminhoes,
            frete,
            modo_atualizacao_status=True
        )

        if dados is None:
            self.__tela_frete.mostrar_mensagem("Atualização cancelada.")
            return

        # Atualizar o status e motivo do cancelamento
        frete.status = Status[dados["status"]]
        frete.motivo_cancelamento = MotivoCancelamento[dados["motivo_cancelamento"]] if dados["status"] == "CANCELADO" else None
        self.__frete_dao.update(frete)
        self.__tela_frete.mostrar_mensagem("Status atualizado com sucesso!")

    def atualizar_status_frete_gerente(self, id_frete):
        frete = self.procura_frete_por_id(id_frete)
        if not frete:
            self.__tela_frete.mostrar_mensagem("Frete não encontrado.")
            return

        dados_frete = self.__tela_cadastro_frete.pega_dados_frete(
            self.__controlador_sistema.controlador_caminhoneiro.lista_caminhoneiros,
            self.__controlador_sistema.controlador_caminhao.lista_caminhoes,
            frete,
            modo_atualizacao_status=True
        )
        if not dados_frete:
            return

        # Atualizar status
        frete.status = Status[dados_frete["status"]]
        
        # Se o status for CANCELADO, salvar o motivo
        if frete.status == Status.CANCELADO:
            frete.motivo_cancelamento = dados_frete["motivo_cancelamento"]

        # Salvar as alterações no arquivo
        self.__frete_dao.update(frete)
        
        self.__tela_frete.mostrar_mensagem("Status atualizado com sucesso!")
        return frete

    def listar_meus_fretes(self, id_caminhoneiro):
        dados_exibicao = []
        for f in self.lista_fretes:
            if f.caminhoneiro.id == id_caminhoneiro:
                # Verifica se o frete pode ser atualizado pelo caminhoneiro
                pode_atualizar = (
                    f.status in [Status.NAO_INICIADO, Status.EM_ANDAMENTO, Status.SUSPENSO] and
                    (not f.prazo_entrega or datetime.now() <= f.prazo_entrega)
                )
                
                dados_exibicao.append({
                    "id": f.id,
                    "origem": f.origem,
                    "destino": f.destino,
                    "status": f.status.name,
                    "prazo_entrega": f.prazo_entrega,
                    "pode_atualizar": pode_atualizar
                })
        return self.__tela_atualizacao_status.mostrar_fretes_para_atualizacao(dados_exibicao, perfil="caminhoneiro")
    
    def opcoes_meus_fretes(self, id_caminhoneiro):
        while True:
            opcao = self.listar_meus_fretes(id_caminhoneiro)

            if opcao == "voltar":
                break
            elif isinstance(opcao, dict) and opcao["acao"] == "atualizar":
                id_frete = opcao["id"]
                self.atualizar_status_frete(id_frete)
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

    def obter_lista_cargas(self):
        """Retorna a lista de todas as cargas disponíveis"""
        return self.__controlador_sistema.controlador_carga.lista_cargas

    def abrir_cadastro_carga(self):
        """Abre a tela de cadastro de carga e retorna a carga cadastrada"""
        # Abre a tela de cadastro de carga
        self.__controlador_sistema.controlador_carga.incluir_carga()
        
        # Retorna a última carga cadastrada (se houver)
        cargas = self.__controlador_sistema.controlador_carga.lista_cargas
        if cargas:
            # Retorna a última carga cadastrada
            ultima_carga = cargas[-1]
            # Atualiza o display da carga na tela
            if self.__tela_cadastro_frete:
                self.__tela_cadastro_frete.atualizar_display_carga(ultima_carga)
            return ultima_carga
        return None
