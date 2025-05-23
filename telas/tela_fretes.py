import FreeSimpleGUI as sg

class TelaFrete:
    def __init__(self):
        sg.theme("Reddit")

    def mostrar_fretes(self, lista_fretes: list[dict], perfil: str = "gerente"):
        layout = []

        # Título com base no perfil
        titulo = "Meus Fretes" if perfil == "caminhoneiro" else "Fretes"
        layout.append([
            sg.Text(titulo, font=("Arial", 20), justification="center", expand_x=True)
        ])

        # Botão de adicionar apenas para gerente
        if perfil == "gerente":
            layout[0].append(
                sg.Button("➕", key="adicionar", button_color=("white", "#5F41D9"), size=(3, 1), font=("Arial", 14))
            )

        # Verifica se lista está vazia
        if not lista_fretes:
            layout.append([sg.Text("⚠️ Nenhum frete cadastrado.", text_color="red")])
        else:
            if perfil == "gerente":
                layout.append([
                    sg.Text("ID", size=(5, 1)),
                    #sg.Text("Carga", size=(12, 1)),
                    sg.Text("Caminhoneiro", size=(20, 1)),
                    sg.Text("Status", size=(15, 1)),
                    sg.Text("Prazo", size=(15, 1)),
                    sg.Text("Ações", size=(10, 1)),
                ])
                for frete in lista_fretes:
                    layout.append([
                        sg.Text(str(frete["id"]), size=(5, 1)),
                        #sg.Text(frete["carga"], size=(12, 1)),
                        sg.Text(frete["caminhoneiro"], size=(20, 1)),
                        sg.Text(frete["status"], size=(15, 1)),
                        sg.Text(frete["prazo_entrega"].strftime("%d/%m/%Y %H:%M") if frete["prazo_entrega"] else "Não definido", size=(15, 1)),
                        sg.Button("✎", key=f"editar_{frete['id']}", size=(3, 1)),
                        sg.Button("🗑", key=f"excluir_{frete['id']}", size=(3, 1))
                    ])
            else:
                layout.append([
                    sg.Text("ID", size=(5, 1)),
                    sg.Text("Origem", size=(15, 1)),
                    sg.Text("Destino", size=(15, 1)),
                    sg.Text("Status", size=(12, 1)),
                    sg.Text("Ações", size=(10, 1)),
                ])
                for frete in lista_fretes:
                    layout.append([
                        sg.Text(str(frete["id"]), size=(5, 1)),
                        sg.Text(frete["origem"], size=(15, 1)),
                        sg.Text(frete["destino"], size=(15, 1)),
                        sg.Text(frete["status"], size=(12, 1)),
                        sg.Button("✎", key=f"editar_{frete['id']}", size=(3, 1)),
                        sg.Button("🗑", key=f"excluir_{frete['id']}", size=(3, 1))
                    ])

        layout.append([
            sg.Push(),
            sg.Button("VOLTAR", key="voltar", size=(15, 1), font=("Arial", 12)),
            sg.Push()
        ])

        self.__window = sg.Window(titulo, layout, size=(800, 420), finalize=True, resizable=True)

        while True:
            evento, _ = self.__window.read()
            if evento in (sg.WINDOW_CLOSED, "voltar"):
                self.__window.close()
                return "voltar"
            elif evento == "adicionar" and perfil == "gerente":
                self.__window.close()
                return "cadastrar"
            elif evento.startswith("editar_"):
                return {"acao": "editar", "id": int(evento.split("_")[1])}
            elif evento.startswith("excluir_"):
                return {"acao": "excluir", "id": int(evento.split("_")[1])}

    def mostrar_mensagem(self, msg: str, titulo="Aviso"):
        sg.popup(msg, title=titulo)

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
                    sg.Text(frete["prazo_entrega"].strftime("%d/%m/%Y %H:%M") if frete["prazo_entrega"] else "Não definido", size=(15, 1)),
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
