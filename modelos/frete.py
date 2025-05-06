class Frete:
    def __init__(self, id: int, origem: str, destino: str, motivo_cancelamento: str,
                 distancia: int, status, observacoes: list, caminhoneiro, caminhao, carga):
        self.__id = id
        self.__origem = origem
        self.__destino = destino
        self.__motivo_cancelamento = motivo_cancelamento
        self.__distancia = distancia
        self.__status = status
        self.__observacoes = observacoes if observacoes else []
        self.__caminhoneiro = caminhoneiro
        self.__caminhao = caminhao
        self.__carga = carga

    # Getters

    @property
    def id(self):
        return self.__id

    @property
    def origem(self):
        return self.__origem

    @property
    def destino(self):
        return self.__destino

    @property
    def motivo_cancelamento(self):
        return self.__motivo_cancelamento

    @property
    def distancia(self):
        return self.__distancia

    @property
    def status(self):
        return self.__status

    @property
    def observacoes(self):
        return self.__observacoes

    @property
    def caminhoneiro(self):
        return self.__caminhoneiro

    @property
    def caminhao(self):
        return self.__caminhao

    @property
    def carga(self):
        return self.__carga

    # Setters

    @origem.setter
    def origem(self, origem):
        self.__origem = origem

    @destino.setter
    def destino(self, destino):
        self.__destino = destino

    @motivo_cancelamento.setter
    def motivo_cancelamento(self, motivo_cancelamento):
        self.__motivo_cancelamento = motivo_cancelamento

    @distancia.setter
    def distancia(self, distancia):
        self.__distancia = distancia

    @status.setter
    def status(self, status):
        self.__status = status

    @observacoes.setter
    def observacoes(self, observacoes):
        self.__observacoes = observacoes

    @caminhoneiro.setter
    def caminhoneiro(self, caminhoneiro):
        self.__caminhoneiro = caminhoneiro

    @caminhao.setter
    def caminhao(self, caminhao):
        self.__caminhao = caminhao

    @carga.setter
    def carga(self, carga):
        self.__carga = carga
