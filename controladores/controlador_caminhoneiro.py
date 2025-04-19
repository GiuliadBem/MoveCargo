from telas.tela_cadastro_caminhoneiro import TelaCadastroCaminhoneiro
from telas.tela_caminhoneiro import TelaCaminhoneiro
from modelos.caminhoneiro import Caminhoneiro
from daos.caminhoneiro_dao import CaminhoneiroDAO

class ControladorCaminhoneiro:
    def __init__(self, controlador_sistema):
        self.__caminhoneiro_dao = CaminhoneiroDAO()
        self.__tela_caminhoneiro = TelaCaminhoneiro()
        self.__tela_cadastro_caminhoneiro = TelaCadastroCaminhoneiro()
        self.__controlador_sistema = controlador_sistema

    @property
    def lista_caminhoneiros(self):
        return self.__caminhoneiro_dao.get_all()

    def procura_caminhoneiro(self, usuario):
        for caminhoneiro in self.lista_caminhoneiros:
            if caminhoneiro.usuario == usuario:
                return caminhoneiro
        return None

    def incluir_caminhoneiro(self):
        dados = self.__tela_cadastro_caminhoneiro.pega_dados_caminhoneiro()
        try:
            if dados["nome"] == "" or dados["cpf"] == "":
                raise KeyError("Nome ou CPF vazios")
            
            cria_id = len(self.lista_caminhoneiros) 
            while self.procura_caminhoneiro(cria_id) is not None:
                cria_id += 1

            novo_caminhoneiro = Caminhoneiro(
                usuario=dados["usuario"],
                senha=dados["senha"],
                nome=dados["nome"],
                cpf=int(dados["cpf"]),
                telefone=int(dados["telefone"]),
                email=dados["email"],
                num_cnh=int(dados["num_cnh"]),
                cat_cnh=dados["cat_cnh"],
                possui_MOPP=bool(dados["possui_MOPP"]),
                id=cria_id,
            )

            self.__caminhoneiro_dao.add(novo_caminhoneiro)

        except (KeyError, ValueError) as erro:
            self.__tela_caminhoneiro.mostrar_mensagem(f"Erro ao cadastrar caminhoneiro: {erro}")
    

    def listar_caminhoneiros(self):
        dados_exibicao = []
        for c in self.lista_caminhoneiros:
            dados_exibicao.append({
                "id": c.id,
                "nome": c.nome,
                "MOPP": "Sim" if c.possui_MOPP else "Não"
                # "frete": c.frete if hasattr(c, 'frete') else "-"  # incluir futuramente
            })
        return self.__tela_caminhoneiro.mostrar_caminhoneiros(dados_exibicao)

    
    def retornar(self):
        self.__controlador_sistema.abre_tela()
    
    def opcoes_caminhoneiro(self):
        while True:
            opcao = self.listar_caminhoneiros()
            print(opcao)

            if opcao == "cadastrar":
                self.incluir_caminhoneiro()
            elif opcao == "atualizar":
                self.atualizar_caminhoneiro()
            elif opcao == "excluir":
                self.excluir_caminhoneiro()
            elif opcao == "voltar":
                self.__controlador_sistema.abre_tela()
                break
            else:
                self.__tela_caminhoneiro.mostrar_mensagem("Opção inválida. Tente novamente.")