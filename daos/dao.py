import pickle

class DAO:
    def __init__(self, nome_do_arquivo):
        self.__nome_do_arquivo = nome_do_arquivo
        self.__dados = {}

    def __dump(self):
        pickle.dump(self.__dados, open(self.__nome_do_arquivo, "wb"))

    def __load(self):
        self.__dados = pickle.load(open(self.__nome_do_arquivo, "rb"))

    # Esse método precisa chamar o self.__dump()
    def add(self, chave, valor):
        self.__dados[chave] = valor
        self.__dump() # Atualiza o arquivo depois de add

    def update(self, chave, valor):
        if(self.__dados[chave] != None):
            self.__dados[chave] = valor # Atualiza o valor da chave
            self.__dump() # Atualiza o arquivo

    def get(self, chave):
        return self.__dados[chave]

    def remove(self, chave):
        self.__dados.pop(chave)
        self.__dump()

    def get_all(self):
        return self.__dados.values()