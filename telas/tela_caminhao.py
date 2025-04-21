import FreeSimpleGUI as sg

class TelaCaminhao:
    def __init__(self):
        sg.theme("Reddit")
        self.__window = None

    def mostrar_caminhoes(self, lista_caminhoes: list[dict]):
        layout = []

        # Linha superior com título e botão "+"
        topo = [
            sg.Text("Caminhoneiros", font=("Arial", 20), expand_x=True),
            sg.Button("➕", key="adicionar", button_color=("white", "#5F41D9"), size=(3, 1), font=("Arial", 14))
        ]
        layout.append(topo)

        if not lista_caminhoes:
            layout.append([
                sg.Text("⚠️ Nenhum caminhão cadastrado no momento.",
                text_color="red", font=("Arial", 12), justification='center', expand_x=True)
            ])
        else:
            # Cabeçalho
            cabecalho = [
                sg.Text("ID", size=(6, 1), justification='center', font=('Arial', 12, 'bold')),
                sg.Text("Placa", size=(20, 1), justification='center', font=('Arial', 12, 'bold')),
                sg.Text("Capacidade", size=(12, 1), justification='center', font=('Arial', 12, 'bold')),
                sg.Text("Tipo de Carga", size=(12, 1), justification='center', font=('Arial', 12, 'bold')),
                sg.Text("Ações", size=(10, 1), justification='center', font=('Arial', 12, 'bold'))
            ]
            layout.append(cabecalho)
            layout.append([sg.HorizontalSeparator()])

            # Adicionar uma linha para cada caminhão
            for i, c in enumerate(lista_caminhoes):
                linha = [
                    sg.Text(c["id"], size=(6, 1), justification='center'),
                    sg.Text(c["placa"], size=(20, 1), justification='center'),
                    sg.Text(c["capacidade"], size=(12, 1), justification='center'),
                    sg.Text(c["tipo_carga"], size=(12, 1), justification='center'),
                    sg.Button("✎", key=f"editar_{i}", size=(2, 1)),
                    sg.Button("🗑", key=f"excluir_{i}", size=(2, 1))
                ]
                layout.append(linha)

                # Separador entre linhas
                if i < len(lista_caminhoes) - 1:
                    layout.append([sg.HorizontalSeparator()])

        # Rodapé centralizado com botão VOLTAR
        layout.append([sg.Push(), sg.Button("VOLTAR", key="voltar", size=(15, 1), font=("Arial", 12)), sg.Push()])

        self.__window = sg.Window("Lista de Caminhões", layout, size=(750, 420), finalize=True, resizable=True)

        while True:
            evento, valores = self.__window.read()
            print("Evento clicado:", evento)

            if evento in (sg.WINDOW_CLOSED, "voltar"):
                self.__window.close()
                return "voltar"
            elif evento == "adicionar":
                self.__window.close()
                return "cadastrar"
            # Verificar se o evento começa com "editar_"
            elif evento.startswith("editar_"):
                idx = int(evento.split("_")[1])
                id_caminhao = lista_caminhoes[idx]["id"]
                self.__window.close()
                return {"operacao": "editar", "id": id_caminhao}
            # Verificar se o evento começa com "excluir_"
            elif evento.startswith("excluir_"):
                idx = int(evento.split("_")[1])
                id_caminhao = lista_caminhoes[idx]["id"]
                self.__window.close()
                return {"operacao": "excluir", "id": id_caminhao}
            
        self.__window.close()
        return None

    def mostrar_mensagem(self, mensagem: str):
        sg.popup(mensagem)

    def fechar(self):
        if self.__window:
            self.__window.close()
            self.__window = None

    def confirmar_exclusao(self, placa):
        layout = [
            [sg.Text(f"Tem certeza que deseja excluir o caminhão com placa {placa}?", font=("Arial", 12))],
            [sg.Push(), 
            sg.Button("Sim", key="sim", button_color=("white", "red"), size=(10, 1)), 
            sg.Button("Não", key="nao", button_color=("white", "#5F41D9"), size=(10, 1)),
            sg.Push()]
        ]
        
        janela = sg.Window("Confirmar Exclusão", layout, modal=True)
        
        while True:
            evento, _ = janela.read()
            if evento in (sg.WINDOW_CLOSED, "nao"):
                janela.close()
                return False
            elif evento == "sim":
                janela.close()
                return True
            
        self.fechar()
        return False