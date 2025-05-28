# telas/tela_carga.py
import FreeSimpleGUI as sg

class TelaCarga:
    def __init__(self):
        self.__window = None

    def mostrar_cargas(self, lista_cargas):
        # Cabeçalhos da tabela
        headings = ['Código', 'Descrição', 'Peso/Volume', 'Tipo', 'Perigosa']
        
        # Preparar dados para a tabela
        dados_tabela = []
        for carga in lista_cargas:
            dados_tabela.append([
                carga['codigo'],
                carga['descricao'],
                f"{carga['peso']} {carga['unidade']}",
                carga['tipo'],
                carga['carga_perigosa']
            ])

        layout = [
            [sg.Text('Gerenciamento de Cargas', font=('Arial', 16, 'bold'))],
            [sg.Text('_' * 80)],
            [sg.Table(
                values=dados_tabela,
                headings=headings,
                display_row_numbers=False,
                auto_size_columns=True,
                num_rows=min(25, len(dados_tabela)) if dados_tabela else 1,
                key='-TABELA-',
                enable_events=True,
                select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                enable_click_events=True
            )],
            [sg.Text('_' * 80)],
            [
                sg.Button('Nova Carga', key='cadastrar', size=(12, 1)),
                sg.Button('Editar', key='editar', size=(12, 1), disabled=True),
                sg.Button('Excluir', key='excluir', size=(12, 1), disabled=True),
                sg.Button('Voltar', key='voltar', size=(12, 1))
            ]
        ]

        self.__window = sg.Window('Cargas', layout, modal=True, finalize=True)
        
        linha_selecionada = None

        while True:
            event, values = self.__window.read()

            if event in (sg.WIN_CLOSED, 'voltar'):
                self.__window.close()
                return 'voltar'

            if event == 'cadastrar':
                self.__window.close()
                return 'cadastrar'

            if event == '-TABELA-':
                if values['-TABELA-']:
                    linha_selecionada = values['-TABELA-'][0]
                    self.__window['editar'].update(disabled=False)
                    self.__window['excluir'].update(disabled=False)
                else:
                    linha_selecionada = None
                    self.__window['editar'].update(disabled=True)
                    self.__window['excluir'].update(disabled=True)

            if event == 'editar' and linha_selecionada is not None:
                codigo_carga = dados_tabela[linha_selecionada][0]
                self.__window.close()
                return {"acao": "editar", "codigo": codigo_carga}

            if event == 'excluir' and linha_selecionada is not None:
                codigo_carga = dados_tabela[linha_selecionada][0]
                self.__window.close()
                return {"acao": "excluir", "codigo": codigo_carga}

    def confirmar_exclusao(self, codigo_carga):
        return sg.popup_yes_no(
            f'Tem certeza que deseja excluir a carga de código {codigo_carga}?',
            title='Confirmar Exclusão'
        ) == 'Yes'

    def mostrar_mensagem(self, mensagem):
        if "sucesso" in mensagem.lower():
            sg.popup_ok(mensagem, title='Sucesso')
        elif "erro" in mensagem.lower():
            sg.popup_error(mensagem, title='Erro')
        else:
            sg.popup_ok(mensagem, title='Informação')