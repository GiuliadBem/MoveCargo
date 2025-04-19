import FreeSimpleGUI as sg

class TelaCaminhoneiro:
    def __init__(self):
        sg.theme("Reddit")

    def mostrar_caminhoneiros(self, lista_caminhoneiros: list[dict]):
        layout = []

        # Linha superior com título e botão "+"
        topo = [
            sg.Text("Caminhoneiros", font=("Arial", 20), expand_x=True),
            sg.Button("➕", key="adicionar", button_color=("white", "#5F41D9"), size=(3, 1), font=("Arial", 14))
        ]
        layout.append(topo)

        if not lista_caminhoneiros:
            layout.append([
                sg.Text("⚠️ Nenhum caminhoneiro cadastrado no momento.",
                        text_color="red", font=("Arial", 12), justification='center', expand_x=True)
            ])
        else:
            header = ["ID", "Usuário", "Possui MOPP", "Frete Atual", "", "", ""]
            dados_tabela = []

            for c in lista_caminhoneiros:
                dados_tabela.append([
                    c["id"],
                    c["nome"],
                    c["MOPP"],
                    "-",  # ou c["frete"] se já tiver implementado
                    "✎",  # editar
                    "🗑",  # excluir
                    "👁"   # visualizar
                ])

            layout.append([
                sg.Table(
                    values=dados_tabela,
                    headings=header,
                    auto_size_columns=False,
                    justification='center',
                    num_rows=10,
                    key='-TABELA-',
                    enable_events=True,
                    col_widths=[6, 20, 12, 12, 5, 5, 5],
                    font=("Arial", 12),
                    alternating_row_color="#f0f0f0"
                )
            ])

        # Rodapé centralizado com botão VOLTAR
        layout.append([sg.Push(), sg.Button("VOLTAR", key="voltar", size=(15, 1), font=("Arial", 12)), sg.Push()])

        self.__window = sg.Window("Lista de Caminhoneiros", layout, size=(750, 420), finalize=True, resizable=True)

        while True:
            evento, valores = self.__window.read()
            print("Evento clicado:", evento)
            if evento in (sg.WINDOW_CLOSED, "voltar"):
                break
            elif evento == "adicionar":
                acao = "cadastrar"
                self.__window.close()
                return acao
            elif evento == "-TABELA-" and lista_caminhoneiros:
                index = valores["-TABELA-"][0]
                self.__window.close()
                return index

        self.__window.close()