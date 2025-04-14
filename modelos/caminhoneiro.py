from modelos.pessoa import Pessoa

class Caminhoneiro(Pessoa):
    def __init__(
        self, id: int, usuario: str, senha: str,
        nome: str, cpf: int, telefone: int, email: str,
        num_cnh: int, cat_cnh: str, possui_MOPP: bool,
    ):
        super().__init__(usuario, senha)
        self.__id = id
        self.__nome = nome
        self.__cpf = cpf
        self.__telefone = telefone
        self.__email = email
        self.__num_cnh = num_cnh
        self.__cat_cnh = cat_cnh
        self.__possui_MOPP = possui_MOPP
        self.__freteAtual = None
        self.__notificacoes = []


    # Validação de CPF -> CONTROLADOR(NÃO FAZ SENTIDO SER NO SETTER)
    def validar_cpf(cpf: int):
        cpf_str = str(cpf)

        # Deve ter exatamente 11 dígitos e não pode ter todos os dígitos iguais
        if len(cpf_str) != 11 or cpf_str == cpf_str[0] * 11:
            return False

        # Cálculo do primeiro dígito verificador
        soma1 = sum(int(cpf_str[i]) * (10 - i) for i in range(9))
        digito1 = (soma1 * 10 % 11) % 10

        # Cálculo do segundo dígito verificador
        soma2 = sum(int(cpf_str[i]) * (11 - i) for i in range(10))
        digito2 = (soma2 * 10 % 11) % 10

        return cpf_str[9] == str(digito1) and cpf_str[10] == str(digito2)

    # Getters e Setters

    @property
    def id(self):
        return self.__id
    
    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        if not self.validar_cpf(cpf):
            raise ValueError("CPF inválido.")
        self.__cpf = cpf

    # Validação de telefone
    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        telefone_str = str(telefone)
        if not telefone_str.isdigit() or len(telefone_str) < 10 or len(telefone_str) > 11:
            raise ValueError("Telefone deve conter entre 10 e 11 dígitos.")
        self.__telefone = telefone
    
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def num_cnh(self):
        return self.__num_cnh

    @num_cnh.setter
    def num_cnh(self, num_cnh):
        self.__num_cnh = num_cnh

    @property
    def cat_cnh(self):
        return self.__cat_cnh

    @cat_cnh.setter
    def cat_cnh(self, cat_cnh):
        self.__cat_cnh = cat_cnh

    @property
    def possui_MOPP(self):
        return self.__possui_MOPP

    @possui_MOPP.setter
    def possui_MOPP(self, possui_MOPP):
        self.__possui_MOPP = possui_MOPP

    @property
    def freteAtual(self):
        return self.__freteAtual

    @freteAtual.setter
    def freteAtual(self, freteAtual):
        self.__freteAtual = freteAtual
