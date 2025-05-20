import FreeSimpleGUI as sg

class TelaFrete:
    def __init__(self):
        sg.theme("Reddit")

    def mostrar_fretes(self, lista_fretes: list[dict]):
        layout = []

        # Título e botão +
        topo = [
            sg.Text("Fretes", font=("Arial", 20), expand_x=True),
            sg.Button("➕", key="adicionar", button_color=("white", "#5F41D9"), size=(3, 1), font=("Arial", 14))
        ]
        layout.append(topo)

        if not lista_fretes:
            layout.append([sg.Text("⚠️ Nenhum frete cadastrado.", text_color="red", font=("Arial", 12))])
        else:
            layout.append([
                sg.Text("ID", size=(5, 1)),
                sg.Text("Origem", size=(15, 1)),
                sg.Text("Destino", size=(15, 1)),
                sg.Text("Distância (km)", size=(12, 1)),
                sg.Text("Status", size=(12, 1)),
                sg.Text("Ações", size=(12, 1)),
            ])

            for frete in lista_fretes:
                layout.append([
                    sg.Text(str(frete["id"]), size=(5, 1)),
                    sg.Text(frete["origem"], size=(15, 1)),
                    sg.Text(frete["destino"], size=(15, 1)),
                    sg.Text(str(frete["distancia"]), size=(12, 1)),
                    sg.Text(frete["status"], size=(12, 1)),
                    sg.Button("✎", key=f"editar_{frete['id']}", size=(3, 1)),
                    sg.Button("🗑", key=f"excluir_{frete['id']}", size=(3, 1))
                ])

        layout.append([sg.Push(), sg.Button("VOLTAR", key="voltar", size=(15, 1), font=("Arial", 12)), sg.Push()])
        self.__window = sg.Window("Lista de Fretes", layout, size=(850, 450), finalize=True, resizable=True)

        while True:
            evento, valores = self.__window.read()
            print("Evento:", evento)

            if evento in (sg.WINDOW_CLOSED, "voltar"):
                self.__window.close()
                return "voltar"
            elif evento == "adicionar":
                acao = "cadastrar"
                self.__window.close()
                return acao
            elif evento.startswith("editar_"):
                id_frete = int(evento.split("_")[1])
                acao = {"acao": "editar", "id": id_frete}
                self.__window.close()
                return acao
            elif evento.startswith("excluir_"):
                id_frete = int(evento.split("_")[1])
                acao = {"acao": "excluir", "id": id_frete}
                self.__window.close()
                return acao

    def confirmar_exclusao(self, id_frete):
        resposta = sg.popup_yes_no(f"Tem certeza que deseja excluir o frete ID {id_frete}?",
                                    title="Confirmar Exclusão")
        return resposta == "Yes"

    def mostrar_mensagem(self, mensagem: str, titulo: str = "Aviso"):
        sg.popup(mensagem, title=titulo, font=("Arial", 12))

    # -- Atualizar Status do Frete -------------------------------------------------------------------------------------------------------------------------------------- #
    def mostrar_meus_fretes(self, lista_fretes: list[dict]):
        layout = []

        # Título
        topo = [
            sg.Text("Meus Fretes", font=("Arial", 20), expand_x=True)
        ]
        layout.append(topo)

        if not lista_fretes:
            layout.append([sg.Text("⚠️ Nenhum frete encontrado.", text_color="red", font=("Arial", 12))])
        else:
            layout.append([
                sg.Text("ID", size=(5, 1)),
                sg.Text("Origem", size=(15, 1)),
                sg.Text("Destino", size=(15, 1)),
                sg.Text("Status", size=(12, 1)),
                sg.Text("Prazo", size=(15, 1)),
                sg.Text("Ações", size=(12, 1)),
            ])

            for frete in lista_fretes:
                layout.append([
                    sg.Text(str(frete["id"]), size=(5, 1)),
                    sg.Text(frete["origem"], size=(15, 1)),
                    sg.Text(frete["destino"], size=(15, 1)),
                    sg.Text(frete["status"], size=(12, 1)),
                    sg.Text(str(frete["prazo_entrega"]), size=(15, 1)),
                    sg.Button("Atualizar Status", key=f"atualizar_{frete['id']}", size=(15, 1))
                ])

        layout.append([sg.Push(), sg.Button("VOLTAR", key="voltar", size=(15, 1), font=("Arial", 12)), sg.Push()])
        self.__window = sg.Window("Meus Fretes", layout, size=(850, 450), finalize=True, resizable=True)

        while True:
            evento, valores = self.__window.read()
            print("Evento:", evento)

            if evento in (sg.WINDOW_CLOSED, "voltar"):
                self.__window.close()
                return "voltar"
            elif evento.startswith("atualizar_"):
                id_frete = int(evento.split("_")[1])
                self.__window.close()
                return {"acao": "atualizar", "id": id_frete}
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------- #