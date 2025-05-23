import FreeSimpleGUI as sg

class TelaAtualizacaoStatus:
    def __init__(self):
        sg.theme("Reddit")

    def mostrar_fretes_para_atualizacao(self, lista_fretes: list[dict]):
        layout = []

        # Título
        layout.append([
            sg.Text("Atualizar Status dos Fretes", font=("Arial", 20), justification="center", expand_x=True)
        ])

        # Verifica se lista está vazia
        if not lista_fretes:
            layout.append([sg.Text("⚠️ Nenhum frete encontrado.", text_color="red")])
        else:
            layout.append([
                sg.Text("ID", size=(5, 1)),
                sg.Text("Caminhoneiro", size=(20, 1)),
                sg.Text("Status", size=(15, 1)),
                sg.Text("Prazo", size=(15, 1)),
                sg.Text("Ações", size=(10, 1)),
            ])
            for frete in lista_fretes:
                layout.append([
                    sg.Text(str(frete["id"]), size=(5, 1)),
                    sg.Text(frete["caminhoneiro"], size=(20, 1)),
                    sg.Text(frete["status"], size=(15, 1)),
                    sg.Text(frete["prazo_entrega"].strftime("%d/%m/%Y %H:%M") if frete["prazo_entrega"] else "Não definido", size=(15, 1)),
                    sg.Button("Atualizar", key=f"atualizar_{frete['id']}", size=(10, 1))
                ])

        layout.append([
            sg.Push(),
            sg.Button("VOLTAR", key="voltar", size=(15, 1), font=("Arial", 12)),
            sg.Push()
        ])

        self.__window = sg.Window("Atualizar Status dos Fretes", layout, size=(800, 420), finalize=True, resizable=True)

        while True:
            evento, _ = self.__window.read()
            if evento in (sg.WINDOW_CLOSED, "voltar"):
                self.__window.close()
                return "voltar"
            elif evento.startswith("atualizar_"):
                id_frete = int(evento.split("_")[1])
                self.__window.close()
                return {"acao": "atualizar", "id": id_frete} 