import FreeSimpleGUI as sg

class TelaCaminhoneiro:
    def __init__(self):
        sg.theme("Reddit")

    def mostrar_caminhoneiros(self, lista_caminhoneiros: list[dict]):
        layout = []

        # Título e botão +
        topo = [
            sg.Text("Caminhoneiros", font=("Arial", 20), expand_x=True),
            sg.Button("➕", key="adicionar", button_color=("white", "#5F41D9"), size=(3, 1), font=("Arial", 14))
        ]
        layout.append(topo)

        if not lista_caminhoneiros:
            layout.append([sg.Text("⚠️ Nenhum caminhoneiro cadastrado.", text_color="red", font=("Arial", 12))])
        else:
            layout.append([
                sg.Text("ID", size=(5, 1)),
                sg.Text("Usuário", size=(20, 1)),
                sg.Text("MOPP", size=(8, 1)),
                sg.Text("Frete", size=(12, 1)),
                sg.Text("Ações", size=(12, 1)),
            ])

            for caminhoneiro in lista_caminhoneiros:
                layout.append([
                    sg.Text(str(caminhoneiro["id"]), size=(5, 1)),
                    sg.Text(caminhoneiro["nome"], size=(20, 1)),
                    sg.Text(caminhoneiro["MOPP"], size=(8, 1)),
                    sg.Text("-", size=(12, 1)),  # frete atual se houver
                    sg.Button("✎", key=f"editar_{caminhoneiro['id']}", size=(3, 1)),
                    sg.Button("🗑", key=f"excluir_{caminhoneiro['id']}", size=(3, 1))
                ])

        layout.append([sg.Push(), sg.Button("VOLTAR", key="voltar", size=(15, 1), font=("Arial", 12)), sg.Push()])
        self.__window = sg.Window("Lista de Caminhoneiros", layout, size=(750, 420), finalize=True, resizable=True)

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
                id_caminhoneiro = int(evento.split("_")[1])
                acao = {"acao": "editar", "id": id_caminhoneiro}
                self.__window.close()
                return acao
            elif evento.startswith("excluir_"):
                id_caminhoneiro = int(evento.split("_")[1])
                acao = {"acao": "excluir", "id": id_caminhoneiro}
                self.__window.close()
                return acao
    
    def confirmar_exclusao(self, nome_caminhoneiro):
        resposta = sg.popup_yes_no(f"Tem certeza que deseja excluir o caminhoneiro '{nome_caminhoneiro}'?",
                                    title="Confirmar Exclusão")
        return resposta == "Yes"
    
    def mostrar_mensagem(self, mensagem: str, titulo: str = "Aviso"):
        sg.popup(mensagem, title=titulo, font=("Arial", 12))
  