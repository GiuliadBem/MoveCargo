from daos.caminhao_dao import CaminhaoDAO
from modelos.caminhao import Caminhao

class ControladorCaminhao:
    def __init__(self):
        self.__caminhao_dao = CaminhaoDAO()
        self.add_caminhao()

    def add_caminhao(self):
        dados_caminhao = {
            "id": 1,  # você pode gerar um ID único
            "placa": "ABC1234",  # formato padrão de placa
            "modelo": "FH 540",  # exemplo de modelo Volvo
            "marca": "Volvo",    # exemplo de marca
            "ano": 2023,         # ano do caminhão
            "capacidade": 40.0,  # capacidade em toneladas
            "tipo_carga": "SOLIDO"  # deve ser um dos valores: SOLIDO, LIQUIDO, GASOSO, VIVA
        }

        novo_caminhao = Caminhao(dados_caminhao["id"],
                                 dados_caminhao["placa"],
                                 dados_caminhao["modelo"],
                                 dados_caminhao["marca"],
                                 dados_caminhao["ano"],
                                 dados_caminhao["capacidade"],
                                 dados_caminhao["tipo_carga"])
        
        self.__caminhao_dao.add(novo_caminhao)