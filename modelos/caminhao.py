from enums.tipo_carga import TipoCarga

class Caminhao:
    def __init__(self, id: int, placa: str, modelo: str, marca: str, ano: int, capacidade: float, tipo_carga: str):
        self.__id = id
        self.__placa = placa
        self.__modelo = modelo
        self.__marca = marca
        self.__ano = ano
        self.__capacidade = capacidade
        self.__tipo_carga = TipoCarga[tipo_carga]

    @property
    def id(self):
        return self.__id
    
    @property
    def placa(self):
        return self.__placa
    
    @property
    def modelo(self):
        return self.__modelo
    
    @property
    def marca(self):
        return self.__marca
        
    @property
    def ano(self):
        return self.__ano
    
    @property
    def capacidade(self):
        return self.__capacidade
        
    @property
    def tipo_carga(self):
        return self.__tipo_carga
    
    @placa.setter
    def placa(self, placa):
        if isinstance(placa, str):
            self.__placa = placa

    @modelo.setter
    def modelo(self, modelo):
        if isinstance(modelo, str):
            self.__modelo = modelo

    @marca.setter
    def marca(self, marca):
        if isinstance(marca, str):
            self.__marca = marca

    @ano.setter
    def ano(self, ano):
        if isinstance(ano, int):
            self.__ano = ano

    @capacidade.setter
    def capacidade(self, capacidade):
        if isinstance(capacidade, (int, float)):
            self.__capacidade = float(capacidade)

    @tipo_carga.setter
    def tipo_carga(self, tipo_carga):
        if isinstance(tipo_carga, TipoCarga):
            self.__tipo_carga = tipo_carga