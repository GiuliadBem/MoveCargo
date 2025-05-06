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
    
    def procura_caminhoneiro_por_id(self, id):
        for caminhoneiro in self.lista_caminhoneiros:
            if caminhoneiro.id == id:
                return caminhoneiro
        return None

    def incluir_caminhoneiro(self):
        dados = self.__tela_cadastro_caminhoneiro.pega_dados_cadastro()
        if dados == None:
            return
        try:
            cria_id = len(self.lista_caminhoneiros) 
            while self.procura_caminhoneiro_por_id(cria_id) is not None:
                cria_id += 1

            novo_caminhoneiro = Caminhoneiro(
                usuario=dados["usuario"],
                senha=dados["senha"],
                nome=dados["nome"],
                cpf=dados["cpf"],
                data_nascimento = dados["data_nascimento"],
                telefone=dados["telefone"],
                email=dados["email"],
                num_cnh=dados["num_cnh"],
                possui_MOPP=bool(dados["possui_MOPP"]),
                id=cria_id,
            )

            self.__caminhoneiro_dao.add(novo_caminhoneiro)

        except (KeyError, ValueError) as erro:
            self.__tela_caminhoneiro.mostrar_mensagem(f"Erro ao cadastrar caminhoneiro: {erro}")

    def atualizar_caminhoneiro(self, id_caminhoneiro):
        caminhoneiro = self.procura_caminhoneiro_por_id(id_caminhoneiro)

        if not caminhoneiro:
            self.__tela_caminhoneiro.mostrar_mensagem("Caminhoneiro não encontrado.")
            return

        # Dados atuais para exibir no formulário (pré-preenchidos)
        dados_atuais = {
            "nome": caminhoneiro.nome,
            "cpf": str(caminhoneiro.cpf),
            "data_nascimento": caminhoneiro.data_nascimento,
            "telefone": caminhoneiro.telefone,
            "email": caminhoneiro.email,
            "num_cnh": caminhoneiro.num_cnh,
            "possui_MOPP": caminhoneiro.possui_MOPP,
            "usuario": caminhoneiro.usuario,
            "senha": caminhoneiro.senha,
        }

        campos_editaveis = [
            "telefone", "email", "num_cnh", "possui_MOPP"
        ]

        novos_dados = self.__tela_cadastro_caminhoneiro.pega_dados_atualizacao(dados_atuais, campos_editaveis)

        if novos_dados is None:
            self.__tela_caminhoneiro.mostrar_mensagem("Atualização cancelada.")
            return

        try:
            for campo in campos_editaveis:
                valor = novos_dados.get(campo)

                # Converte checkbox em booleano
                if campo == "possui_MOPP":
                    valor = bool(valor)

                setattr(caminhoneiro, campo, valor)

            self.__caminhoneiro_dao.update(caminhoneiro)
            self.__tela_caminhoneiro.mostrar_mensagem("Caminhoneiro atualizado com sucesso!")

        except Exception as e:
            self.__tela_caminhoneiro.mostrar_mensagem(f"Erro ao atualizar caminhoneiro: {e}")


    def excluir_caminhoneiro(self, id):
        id_caminhoneiro = id

         #Verificação caso utilize a função em outro lugar
        if id_caminhoneiro is None:
            self.__tela_caminhoneiro.mostrar_mensagem("Nenhum caminhoneiro selecionado.")
            return

        caminhoneiro = self.procura_caminhoneiro_por_id(id_caminhoneiro)
        # Verificação caso utilize a função em outro lugar
        if not caminhoneiro:
            self.__tela_caminhoneiro.mostrar_mensagem("Caminhoneiro não encontrado.")
            return

        # Chamada para a tela confirmar
        if self.__tela_caminhoneiro.confirmar_exclusao(caminhoneiro.nome):
            self.__caminhoneiro_dao.remove(id_caminhoneiro)
            self.__tela_caminhoneiro.mostrar_mensagem("Caminhoneiro excluído com sucesso!")
        else:
            self.__tela_caminhoneiro.mostrar_mensagem("Exclusão cancelada.")


    def listar_caminhoneiros(self):
        dados_exibicao = []
        for c in self.lista_caminhoneiros:
            dados_exibicao.append({
                "id": c.id,
                "nome": c.nome,
                "MOPP": "Sim" if c.possui_MOPP else "Não"
                # "frete": c.frete if tem_frete(c, 'frete') else "-"  # incluir futuramente
            })
        return self.__tela_caminhoneiro.mostrar_caminhoneiros(dados_exibicao)

    
    def retornar(self):
        self.__controlador_sistema.abre_tela()
    
    def opcoes_caminhoneiro(self):
        while True:
            opcao = self.listar_caminhoneiros()

            if opcao == "cadastrar":
                self.incluir_caminhoneiro()

            elif isinstance(opcao, dict) and "acao" in opcao:
                id_caminhoneiro = opcao.get("id")

                if opcao["acao"] == "editar":
                    self.atualizar_caminhoneiro(id_caminhoneiro)

                elif opcao["acao"] == "excluir":
                    self.excluir_caminhoneiro(id_caminhoneiro)

            elif opcao == "voltar":
                break  # aqui sai do loop e volta ao sistema
    
    def editar_meu_cadastro(self, usuario_logado):
        caminhoneiro = self.procura_caminhoneiro(usuario_logado)

        if not caminhoneiro:
            self.__tela_caminhoneiro.mostrar_mensagem("Caminhoneiro não encontrado.")
            return

        # Define os campos permitidos para edição pelo próprio caminhoneiro
        dados_atuais = {
            "nome": caminhoneiro.nome,
            "telefone": caminhoneiro.telefone,
            "email": caminhoneiro.email,
            "senha": caminhoneiro.senha
        }

        novos_dados = self.__tela_cadastro_caminhoneiro.pega_dados_atualizacao(dados_atuais)

        if novos_dados is None:
            self.__tela_caminhoneiro.mostrar_mensagem("Atualização cancelada.")
            return

        try:
            caminhoneiro.nome = novos_dados["nome"]
            caminhoneiro.telefone = novos_dados["telefone"]
            caminhoneiro.email = novos_dados["email"]
            caminhoneiro.senha = novos_dados["senha"]

            self.__caminhoneiro_dao.update(caminhoneiro)
            self.__tela_caminhoneiro.mostrar_mensagem("Cadastro atualizado com sucesso!")

        except Exception as e:
            self.__tela_caminhoneiro.mostrar_mensagem(f"Erro ao atualizar cadastro: {e}")