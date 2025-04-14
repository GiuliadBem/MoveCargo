from modelos.pessoa import Pessoa

class Gerente(Pessoa):
    def __init__(self):
        super().__init__("gerente", "123456")
    
    #---------------------------------------------------------------
    # Getters
    #---------------------------------------------------------------

    @property
    def nome(self):
        return "Gerente"