from enums.tipo_carga import TipoCarga

class Carga:
    def __init__(self, codigo: str, tipo: TipoCarga, descricao: str, peso_volume: float, unidade: str, perigosa: bool = False):
        if not codigo or not isinstance(codigo, str) or codigo.strip() == "":
            raise ValueError("O código da carga é obrigatório e não pode ser vazio.")
        if not isinstance(tipo, TipoCarga):
            raise TypeError("O tipo da carga deve ser um membro do Enum TipoCarga.")
        
        self.codigo = codigo.strip()
        self.tipo: TipoCarga = tipo
        self.descricao = descricao
        self.peso_volume = peso_volume
        self.unidade = unidade
        self.perigosa = perigosa

    def __repr__(self):
        return (f"Carga(codigo='{self.codigo}', tipo='{self.tipo.value}', descricao='{self.descricao}', "
                f"peso_volume={self.peso_volume}, unidade='{self.unidade}', perigosa={self.perigosa})")