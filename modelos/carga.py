from enums.tipo_carga import TipoCarga

class Carga:
    def __init__(self, codigo: str, tipo: TipoCarga, descricao: str, quantidade: float, carga_perigosa: bool = False):
        if not codigo or not isinstance(codigo, str) or codigo.strip() == "":
            raise ValueError("O código da carga é obrigatório e não pode ser vazio.")
        if not isinstance(tipo, TipoCarga):
            raise TypeError("O tipo da carga deve ser um membro do Enum TipoCarga.")
        if not descricao or not isinstance(descricao, str) or descricao.strip() == "":
            raise ValueError("A descrição da carga é obrigatória e não pode ser vazia.")
        
        self.codigo = codigo.strip()
        self.tipo: TipoCarga = tipo
        self.descricao = descricao.strip()
        self.quantidade = quantidade
        self.carga_perigosa = carga_perigosa

    def __repr__(self):
        return (f"Carga(codigo='{self.codigo}', tipo='{self.tipo.value}', descricao='{self.descricao}', "
                f"quantidade={self.quantidade}, carga_perigosa={self.carga_perigosa})")