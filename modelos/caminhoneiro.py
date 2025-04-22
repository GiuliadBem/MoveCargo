from datetime import date
from modelos.pessoa import Pessoa

class Caminhoneiro(Pessoa):
    def __init__(
        self, id: int, usuario: str, senha: str,
        nome: str, cpf: str, data_nascimento: date ,telefone=None, email=None,
        num_cnh=None, possui_MOPP=False,
    ):
        super().__init__(usuario, senha)
        self.__id = id
        self.__nome = nome
        self.__cpf = cpf
        self.__telefone = telefone
        self.__email = email
        self.__num_cnh = num_cnh
        self.__possui_MOPP = possui_MOPP
        self.__data_nascimento = data_nascimento
        self.__freteAtual = None
        self.__notificacoes = []


    # Getters e Setters

    @property
    def id(self):
        return self.__id
    
    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
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
    
    @property
    def data_nascimento(self):
        return self.__data_nascimento
    
    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self.__data_nascimento = data_nascimento