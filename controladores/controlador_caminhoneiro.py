from telas.tela_cadastro_caminhoneiro import TelaCaminhoneiro
from modelos.caminhoneiro import Caminhoneiro
from daos.caminhoneiro_dao import CaminhoneiroDAO

class ControladorCaminhoneiro:
    def __init__(self, controlador_sistema):
        self.__caminhoneiro_dao = CaminhoneiroDAO()
        self.__tela_caminhoneiro = TelaCaminhoneiro()
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
        dados = self.__tela_caminhoneiro.pega_dados_caminhoneiro()
        try:
            if dados["nome"] == "" or dados["cpf"] == "":
                raise KeyError("Nome ou CPF vazios")

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
            )

            self.__caminhoneiro_dao.add(novo_caminhoneiro)

        except (KeyError, ValueError) as erro:
            self.__tela_caminhoneiro.mostrar_mensagem(f"Erro ao cadastrar caminhoneiro: {erro}")
    
    def retornar(self):
        self.__controlador_sistema.abre_tela()
    
    def abre_tela(self):
        opcoes = {
            1: self.incluir_caminhoneiro,
            0: self.retornar
        }

        while True:
            opcao = self.__tela_caminhoneiro.tela_opcoes()
            acao = opcoes.get(opcao)
            if acao:
                acao()
            else:
                self.__tela_caminhoneiro.mostrar_mensagem("Opção inválida. Tente novamente.")