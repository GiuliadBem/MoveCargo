from telas.tela_cadastro_caminhao import TelaCadastroCaminhao
from telas.tela_caminhao import TelaCaminhao
from modelos.caminhao import Caminhao
from daos.caminhao_dao import CaminhaoDAO

class ControladorCaminhao:
    def __init__(self, controlador_sistema):
        self.__caminhao_dao = CaminhaoDAO()
        self.__tela_caminhao = TelaCaminhao()
        self.__tela_cadastro_caminhao = TelaCadastroCaminhao()
        self.__controlador_sistema = controlador_sistema

    @property
    def lista_caminhoes(self):
        return self.__caminhao_dao.get_all()
    
    def procura_caminhao(self, id):
        for caminhao in self.lista_caminhoes:
            if caminhao.id == id:
                return caminhao
        return None
    
    def incluir_caminhao(self):
        dados = self.__tela_cadastro_caminhao.pega_dados_caminhao()

        # Verificar se dados não é None antes de prosseguir
        if dados is None:
            return # Sai da função se não houver dados (cancelamento/fechamento)

        try:
            if dados["placa"] == "" or dados["modelo"] == "" or dados["capacidade"] == "" or dados["tipo_carga"] == "":
                raise KeyError("Campos obrigatórios não preenchidos")
            
            cria_id = len(self.lista_caminhoes)

            while self.procura_caminhao(cria_id) is not None:
                cria_id += 1

            novo_caminhao = Caminhao(
                id = cria_id,
                placa = dados["placa"],
                modelo = dados["modelo"],
                marca = dados["marca"],
                ano = dados["ano"],
                capacidade = dados["capacidade"],
                tipo_carga = dados["tipo_carga"]
            )

            self.__caminhao_dao.add(novo_caminhao)

        except (KeyError, ValueError) as erro:
            self.__tela_caminhao.mostrar_mensagem(f"Erro ao cadastrar caminhão: {erro}")

    def listar_caminhoes(self):
        dados_exibicao = []
        for c in self.lista_caminhoes:
            dados_exibicao.append({
                "id": c.id,
                "placa": c.placa,
                "capacidade": c.capacidade,
                "tipo_carga": c.tipo_carga.value
            })
        return self.__tela_caminhao.mostrar_caminhoes(dados_exibicao)
    
    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def opcoes_caminhao(self):
        while True:
            opcao = self.listar_caminhoes()
            print(opcao)
            
            # Se o resultado for uma string, é uma ação simples
            if isinstance(opcao, str):
                if opcao == "cadastrar":
                    self.incluir_caminhao()
                elif opcao == "voltar":
                    self.__controlador_sistema.abre_tela()
                    break

            # Se a opcao for um dicionário, contém operação e ID
            elif isinstance(opcao, dict):
                if opcao["operacao"] == "excluir":
                    self.excluir_caminhao(opcao["id"])
                elif opcao["operacao"] == "editar":
                    self.atualizar_caminhao(opcao["id"])
            else:
                self.__tela_caminhao.mostrar_mensagem("Opção inválida")

    def excluir_caminhao(self, id_caminhao):
        # Se o ID não foi passado como parâmetro, então é uma chamada direta
        if id_caminhao is None:
            return
        
        # Buscar o caminhão pelo ID
        caminhao = self.procura_caminhao(id_caminhao)
    
        if caminhao is not None:
            # Confirmar exclusão
            if self.__tela_caminhao.confirmar_exclusao(caminhao.placa):
                # Remover o caminhão
                self.__caminhao_dao.remove(caminhao.id)
                self.__tela_caminhao.mostrar_mensagem(f"Caminhão com placa {caminhao.placa} excluído com sucesso!")
        else:
            self.__tela_caminhao.mostrar_mensagem("Caminhão não encontrado!")