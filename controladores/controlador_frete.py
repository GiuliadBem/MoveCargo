from telas.tela_fretes import TelaFrete
from telas.tela_cadastro_frete import TelaCadastroFrete
from modelos.frete import Frete
from daos.frete_dao import FreteDAO

class ControladorFrete:
    def __init__(self, controlador_sistema):
        self.__frete_dao = FreteDAO()
        self.__tela_frete = TelaFrete()
        self.__tela_cadastro_frete = TelaCadastroFrete()
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
        
        dados = self.__tela_cadastro_frete.pega_dados_cadastro(lista_caminhoneiros, lista_caminhoes)
        
        if dados is None:
            self.__tela_frete.mostrar_mensagem("Cadastro cancelado.")
            return

        # Valida campos obrigatórios no controlador
        campos_obrigatorios = ["origem", "destino", "distancia", "caminhoneiro", "caminhao", "carga"]
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                self.__tela_frete.mostrar_mensagem(f"Erro: Campo '{campo}' é obrigatório.")
                return

        try:
            cria_id = len(self.lista_fretes)
            while self.procura_frete_por_id(cria_id) is not None:
                cria_id += 1

            carga = Carga(**dados["carga"])
            observacoes = [Observacao(**obs) for obs in dados.get("observacoes", [])]
            caminhao = dados["caminhao"]
            caminhoneiro = dados["caminhoneiro"]

            # Validação de compatibilidade caminhão/carga
            if carga.tipo != caminhao.tipo_carga:
                self.__tela_frete.mostrar_mensagem("Erro: Caminhão incompatível com o tipo de carga.")
                return

            # Validação de carga perigosa
            if carga.carga_perigosa and not caminhoneiro.possui_mopp:
                self.__tela_frete.mostrar_mensagem("Erro: Caminhoneiro não possui licença MOPP para carga perigosa.")
                return

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
                carga=carga
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

        dados_atuais = {
            "origem": frete.origem,
            "destino": frete.destino,
            "distancia": frete.distancia,
            "status": frete.status,
            "motivo_cancelamento": frete.motivo_cancelamento,
        }

        dados_permitidos = ["origem", "destino", "distancia", "status", "motivo_cancelamento"]

        novos_dados = self.__tela_cadastro_frete.pega_dados_atualizacao(dados_atuais, dados_permitidos)

        if novos_dados is None:
            self.__tela_frete.mostrar_mensagem("Atualização cancelada.")
            return

        try:
            # Validação de campos obrigatórios
            for campo in ["origem", "destino", "distancia"]:
                if campo in novos_dados and not novos_dados[campo]:
                    self.__tela_frete.mostrar_mensagem(f"Erro: Campo '{campo}' não pode estar vazio.")
                    return

            frete.origem = novos_dados.get("origem", frete.origem)
            frete.destino = novos_dados.get("destino", frete.destino)
            frete.distancia = novos_dados.get("distancia", frete.distancia)
            frete.status = novos_dados.get("status", frete.status)

            if frete.status == Status.CANCELADO:
                if not novos_dados.get("motivo_cancelamento"):
                    self.__tela_frete.mostrar_mensagem("Erro: É obrigatório fornecer o motivo do cancelamento.")
                    return
                frete.motivo_cancelamento = novos_dados["motivo_cancelamento"]

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

    def listar_fretes(self):
        dados_exibicao = []
        for f in self.lista_fretes:
            dados_exibicao.append({
                "id": f.id,
                "origem": f.origem,
                "destino": f.destino,
                "status": f.status.name,
            })
        return self.__tela_frete.mostrar_fretes(dados_exibicao)

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def opcoes_frete(self):
        while True:
            opcao = self.listar_fretes()

            if opcao == "cadastrar":
                self.incluir_frete()

            elif isinstance(opcao, dict) and "acao" in opcao:
                id_frete = opcao.get("id")

                if opcao["acao"] == "editar":
                    self.atualizar_frete(id_frete)

                elif opcao["acao"] == "excluir":
                    self.excluir_frete(id_frete)

            elif opcao == "voltar":
                break
