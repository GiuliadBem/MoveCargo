# controladores/controlador_carga.py
from telas.tela_carga import TelaCarga
from telas.tela_cadastro_carga import TelaCadastroCarga
from modelos.carga import Carga
from daos.carga_dao import CargaDAO

class ControladorCarga:
    def __init__(self, controlador_sistema):
        self.__carga_dao = CargaDAO()
        self.__tela_carga = TelaCarga()
        self.__tela_cadastro_carga = TelaCadastroCarga()
        self.__controlador_sistema = controlador_sistema

    @property
    def lista_cargas(self):
        return self.__carga_dao.get_all()

    def procura_carga_por_codigo(self, codigo: str):
        return self.__carga_dao.get(codigo)

    def incluir_carga(self):
        dados = self.__tela_cadastro_carga.pega_dados_carga()
        
        if dados is None:
            self.__tela_carga.mostrar_mensagem("Cadastro cancelado.")
            return

        try:
            # Verifica se já existe uma carga com o mesmo código
            if self.procura_carga_por_codigo(dados["codigo"]):
                self.__tela_carga.mostrar_mensagem("Erro: Já existe uma carga com este código.")
                return

            nova_carga = Carga(
                codigo=dados["codigo"],
                tipo=dados["tipo"],
                descricao=dados["descricao"],
                peso_volume=dados["peso"],
                unidade="kg" if dados["tipo"].name in ["SOLIDA", "VIVA"] else "L",
                perigosa=dados["carga_perigosa"]
            )

            self.__carga_dao.add(nova_carga)
            self.__tela_carga.mostrar_mensagem("Carga cadastrada com sucesso!")
            return nova_carga

        except (KeyError, ValueError, TypeError) as erro:
            self.__tela_carga.mostrar_mensagem(f"Erro ao cadastrar carga: {erro}")
            return None

    def atualizar_carga(self, codigo: str):
        carga = self.procura_carga_por_codigo(codigo)

        if not carga:
            self.__tela_carga.mostrar_mensagem("Carga não encontrada.")
            return

        dados_atuais = {
            "codigo": carga.codigo,
            "descricao": carga.descricao,
            "peso": carga.peso_volume,
            "tipo": carga.tipo,
            "carga_perigosa": carga.perigosa
        }

        novos_dados = self.__tela_cadastro_carga.pega_dados_atualizacao(dados_atuais)

        if novos_dados is None:
            self.__tela_carga.mostrar_mensagem("Atualização cancelada.")
            return

        try:
            # Validação de campos obrigatórios
            for campo in ["codigo", "descricao", "peso", "tipo"]:
                if campo in novos_dados and not novos_dados[campo]:
                    self.__tela_carga.mostrar_mensagem(f"Erro: Campo '{campo}' não pode estar vazio.")
                    return

            # Verifica se o novo código já existe (se foi alterado)
            if novos_dados["codigo"] != carga.codigo and self.procura_carga_por_codigo(novos_dados["codigo"]):
                self.__tela_carga.mostrar_mensagem("Erro: Já existe uma carga com este código.")
                return

            carga.codigo = novos_dados["codigo"]
            carga.descricao = novos_dados["descricao"]
            carga.peso_volume = novos_dados["peso"]
            carga.tipo = novos_dados["tipo"]
            carga.perigosa = novos_dados["carga_perigosa"]
            carga.unidade = "kg" if novos_dados["tipo"].name in ["SOLIDA", "VIVA"] else "L"

            self.__carga_dao.update(carga)
            self.__tela_carga.mostrar_mensagem("Carga atualizada com sucesso!")

        except Exception as e:
            self.__tela_carga.mostrar_mensagem(f"Erro ao atualizar carga: {e}")

    def excluir_carga(self, codigo: str):
        carga = self.procura_carga_por_codigo(codigo)
        if not carga:
            self.__tela_carga.mostrar_mensagem("Carga não encontrada.")
            return

        if self.__tela_carga.confirmar_exclusao(carga.codigo):
            self.__carga_dao.remove(codigo)
            self.__tela_carga.mostrar_mensagem("Carga excluída com sucesso!")
        else:
            self.__tela_carga.mostrar_mensagem("Exclusão cancelada.")

    def listar_cargas(self):
        dados_exibicao = []

        for carga in self.lista_cargas:
            dados_exibicao.append({
                "codigo": carga.codigo,
                "descricao": carga.descricao,
                "peso": carga.peso_volume,
                "tipo": carga.tipo.name if hasattr(carga.tipo, 'name') else str(carga.tipo),
                "carga_perigosa": "Sim" if carga.perigosa else "Não",
                "unidade": carga.unidade
            })
        return dados_exibicao

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def opcoes_carga(self):
        while True:
            opcao = self.__tela_carga.mostrar_cargas(self.listar_cargas())

            if opcao == "cadastrar":
                self.incluir_carga()

            elif isinstance(opcao, dict) and "acao" in opcao:
                codigo_carga = opcao.get("codigo")

                if opcao["acao"] == "editar":
                    self.atualizar_carga(codigo_carga)
                elif opcao["acao"] == "excluir":
                    self.excluir_carga(codigo_carga)

            elif opcao == "voltar":
                break