# telas/tela_cadastro_carga.py
import FreeSimpleGUI as sg
from enums.tipo_carga import TipoCarga

class TelaCadastroCarga:
    def __init__(self):
        self.__window = None

    def pega_dados_carga(self):
        # Lista de tipos de carga para o combo
        tipos_carga = [tipo.name for tipo in TipoCarga]
        
        layout = [
            [sg.Text('Cadastro de Carga', font=('Arial', 16, 'bold'))],
            [sg.Text('_' * 50)],
            [sg.Text('Código*:', size=(12, 1)), sg.Input(key='-CODIGO-', size=(30, 1))],
            [sg.Text('Descrição*:', size=(12, 1)), sg.Input(key='-DESCRICAO-', size=(30, 1))],
            [sg.Text('Peso*:', size=(12, 1)), sg.Input(key='-PESO-', size=(15, 1))],
            [sg.Text('Tipo de Carga*:', size=(12, 1)), sg.Combo(tipos_carga, key='-TIPO-', size=(20, 1), readonly=True, enable_events=True)],
            [sg.Text('Unidade:', size=(12, 1)), sg.Text('kg', key='-UNIDADE-', size=(5, 1))],
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

            if event == '-TIPO-':
                # Atualiza a unidade baseado no tipo de carga
                tipo_selecionado = values['-TIPO-']
                unidade = "kg" if tipo_selecionado in ["SOLIDA", "VIVA"] else "L"
                self.__window['-UNIDADE-'].update(unidade)

            if event == 'Confirmar':
                # Validação dos campos
                if not values['-CODIGO-'].strip():
                    sg.popup_error('Erro: Código é obrigatório!')
                    continue

                if not values['-DESCRICAO-'].strip():
                    sg.popup_error('Erro: Descrição é obrigatória!')
                    continue

                if not values['-TIPO-']:
                    sg.popup_error('Erro: Selecione um tipo de carga!')
                    continue

                try:
                    peso = float(values['-PESO-'])
                    if peso <= 0:
                        sg.popup_error('Erro: Peso deve ser maior que zero!')
                        continue
                except ValueError:
                    sg.popup_error('Erro: Peso deve ser um número válido!')
                    continue

                # Se chegou até aqui, todos os dados são válidos
                dados = {
                    "codigo": values['-CODIGO-'].strip().upper(),
                    "descricao": values['-DESCRICAO-'].strip(),
                    "peso": peso,
                    "tipo": TipoCarga[values['-TIPO-']],
                    "carga_perigosa": values['-CARGA_PERIGOSA-']
                }

                self.__window.close()
                return dados

    def pega_dados_atualizacao(self, dados_atuais):
        tipos_carga = [tipo.name for tipo in TipoCarga]
        
        layout = [
            [sg.Text('Atualizar Carga', font=('Arial', 16, 'bold'))],
            [sg.Text('_' * 50)],
            [sg.Text('Código*:', size=(12, 1)), 
             sg.Input(default_text=dados_atuais['codigo'], key='-CODIGO-', size=(30, 1))],
            [sg.Text('Descrição*:', size=(12, 1)), 
             sg.Input(default_text=dados_atuais['descricao'], key='-DESCRICAO-', size=(30, 1))],
            [sg.Text('Peso*:', size=(12, 1)), 
             sg.Input(default_text=str(dados_atuais['peso']), key='-PESO-', size=(15, 1))],
            [sg.Text('Tipo de Carga*:', size=(12, 1)), 
             sg.Combo(tipos_carga, 
                     default_value=dados_atuais['tipo'].name if hasattr(dados_atuais['tipo'], 'name') else str(dados_atuais['tipo']),
                     key='-TIPO-', size=(20, 1), readonly=True, enable_events=True)],
            [sg.Text('Unidade:', size=(12, 1)), 
             sg.Text('kg' if dados_atuais['tipo'].name in ["SOLIDA", "VIVA"] else "L", 
                    key='-UNIDADE-', size=(5, 1))],
            [sg.Checkbox('Carga Perigosa', default=dados_atuais['carga_perigosa'], key='-CARGA_PERIGOSA-')],
            [sg.Text('* Campos obrigatórios', text_color='red')],
            [sg.Text('_' * 50)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]

        self.__window = sg.Window('Atualizar Carga', layout, modal=True, finalize=True)

        while True:
            event, values = self.__window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                self.__window.close()
                return None

            if event == '-TIPO-':
                # Atualiza a unidade baseado no tipo de carga
                tipo_selecionado = values['-TIPO-']
                unidade = "kg" if tipo_selecionado in ["SOLIDA", "VIVA"] else "L"
                self.__window['-UNIDADE-'].update(unidade)

            if event == 'Confirmar':
                # Validação dos campos
                if not values['-CODIGO-'].strip():
                    sg.popup_error('Erro: Código é obrigatório!')
                    continue

                if not values['-DESCRICAO-'].strip():
                    sg.popup_error('Erro: Descrição é obrigatória!')
                    continue

                if not values['-TIPO-']:
                    sg.popup_error('Erro: Selecione um tipo de carga!')
                    continue

                try:
                    peso = float(values['-PESO-'])
                    if peso <= 0:
                        sg.popup_error('Erro: Peso deve ser maior que zero!')
                        continue
                except ValueError:
                    sg.popup_error('Erro: Peso deve ser um número válido!')
                    continue

                dados = {
                    "codigo": values['-CODIGO-'].strip().upper(),
                    "descricao": values['-DESCRICAO-'].strip(),
                    "peso": peso,
                    "tipo": TipoCarga[values['-TIPO-']],
                    "carga_perigosa": values['-CARGA_PERIGOSA-']
                }

                self.__window.close()
                return dados