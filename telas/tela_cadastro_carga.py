# telas/tela_cadastro_carga.py
import FreeSimpleGUI as sg
from enums.tipo_carga import TipoCarga
from modelos.carga import Carga

class TelaCadastroCarga:
    def __init__(self):
        self.__window = None

    def mostrar_mensagem(self, mensagem: str, tipo: str = "info"):
        """Mostra uma mensagem ao usuário.
        
        Args:
            mensagem (str): A mensagem a ser exibida
            tipo (str): O tipo da mensagem ('info', 'erro', 'sucesso')
        """
        if tipo == "erro":
            sg.popup_error(mensagem)
        elif tipo == "sucesso":
            sg.popup_ok(mensagem, title="Sucesso")
        else:
            sg.popup_ok(mensagem, title="Informação")

    def pega_dados_carga(self):
        # Lista de tipos de carga para o combo
        tipos_carga = [tipo.name for tipo in TipoCarga]
        
        layout = [
            [sg.Text('Cadastro de Carga', font=('Arial', 16, 'bold'))],
            [sg.Text('_' * 50)],
            [sg.Text('Código*:', size=(12, 1)), sg.Input(key='-CODIGO-', size=(30, 1))],
            [sg.Text('Descrição*:', size=(12, 1)), sg.Input(key='-DESCRICAO-', size=(30, 1))],
            [sg.Text('Quantidade*:', size=(12, 1)), sg.Input(key='-PESO-', size=(15, 1))],
            [sg.Text('Tipo de Carga*:', size=(12, 1)), sg.Combo(tipos_carga, key='-TIPO-', size=(20, 1), readonly=True)],
            [sg.Checkbox('Carga Perigosa', key='-CARGA_PERIGOSA-')],
            [sg.Text('* Campos obrigatórios', text_color='red')],
            [sg.Text('_' * 50)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]

        self.__window = sg.Window('Cadastro de Carga', layout, modal=True, finalize=True)

        while True:
            event, values = self.__window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                self.__window.close()
                return None

            if event == 'Confirmar':
                # Validação dos campos
                if not values['-CODIGO-'].strip():
                    self.mostrar_mensagem('Erro: Código é obrigatório!', tipo="erro")
                    continue

                if not values['-DESCRICAO-'].strip():
                    self.mostrar_mensagem('Erro: Descrição é obrigatória!', tipo="erro")
                    continue

                if not values['-TIPO-']:
                    self.mostrar_mensagem('Erro: Selecione um tipo de carga!', tipo="erro")
                    continue

                try:
                    quantidade = float(values['-PESO-'])
                    if quantidade <= 0:
                        self.mostrar_mensagem('Erro: Quantidade deve ser maior que zero!', tipo="erro")
                        continue
                except ValueError:
                    self.mostrar_mensagem('Erro: Quantidade deve ser um número válido!', tipo="erro")
                    continue

                # Se chegou até aqui, todos os dados são válidos
                dados = {
                    "codigo": values['-CODIGO-'].strip().upper(),
                    "descricao": values['-DESCRICAO-'].strip(),
                    "peso": quantidade,
                    "tipo": TipoCarga[values['-TIPO-']],
                    "carga_perigosa": values.get('-CARGA_PERIGOSA-', False)
                }

                self.__window.close()
                return dados

    def procura_carga_por_codigo(self, codigo: str):
        return self.__carga_dao.get(codigo.upper())