# controladores/controlador_carga.py
from telas.tela_cadastro_carga import TelaCadastroCarga
from modelos.carga import Carga
from daos.carga_dao import CargaDAO
from enums.tipo_carga import TipoCarga

class ControladorCarga:
    def __init__(self, controlador_sistema):
        self.__carga_dao = CargaDAO()
        self.__tela_cadastro_carga = TelaCadastroCarga()
        self.__controlador_sistema = controlador_sistema

    @property
    def lista_cargas(self):
        return self.__carga_dao.get_all()

    def procura_carga_por_codigo(self, codigo: str):
        return self.__carga_dao.get(codigo)

    def incluir_carga(self):
        try:
            dados = self.__tela_cadastro_carga.pega_dados_carga()
            if not dados:
                return
            
            # Verifica se já existe uma carga com o mesmo código
            if self.__carga_dao.get(dados['codigo']):
                self.__tela_cadastro_carga.mostrar_mensagem("Já existe uma carga cadastrada com este código.", tipo="erro")
                return
            
            # Cria uma nova carga com os dados fornecidos
            carga = Carga(
                codigo=dados['codigo'],
                tipo=dados['tipo'],
                descricao=dados['descricao'],
                quantidade=dados['peso'],  # Usando o peso como quantidade
                carga_perigosa=dados['carga_perigosa']
            )
            
            # Salva a carga no DAO
            try:
                self.__carga_dao.add(carga)
                self.__tela_cadastro_carga.mostrar_mensagem("Carga cadastrada com sucesso!", tipo="sucesso")
                return carga
            except Exception as e:
                self.__tela_cadastro_carga.mostrar_mensagem(f"Erro ao salvar a carga: {str(e)}", tipo="erro")
                
        except (ValueError, TypeError) as e:
            self.__tela_cadastro_carga.mostrar_mensagem(f"Erro ao cadastrar carga: {str(e)}", tipo="erro")
        except Exception as e:
            self.__tela_cadastro_carga.mostrar_mensagem(f"Erro inesperado ao cadastrar carga: {str(e)}", tipo="erro")

    def excluir_carga(self, codigo: str):
        carga = self.procura_carga_por_codigo(codigo)
        if not carga:
            self.__tela_cadastro_carga.mostrar_mensagem("Carga não encontrada.")
            return

        if self.__tela_cadastro_carga.confirmar_exclusao(carga.codigo):
            self.__carga_dao.remove(codigo)
            self.__tela_cadastro_carga.mostrar_mensagem("Carga excluída com sucesso!")
        else:
            self.__tela_cadastro_carga.mostrar_mensagem("Exclusão cancelada.")

    def listar_cargas(self):
        dados_exibicao = []

        for carga in self.lista_cargas:
            dados_exibicao.append({
                "codigo": carga.codigo,
                "descricao": carga.descricao,
                "peso": carga.quantidade,
                "tipo": carga.tipo.name if hasattr(carga.tipo, 'name') else str(carga.tipo),
                "carga_perigosa": "Sim" if carga.carga_perigosa else "Não"
            })
        return dados_exibicao

    def retornar(self):
        self.__controlador_sistema.abre_tela()