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