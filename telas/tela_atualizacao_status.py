import FreeSimpleGUI as sg

class TelaAtualizacaoStatus:
    def __init__(self):
        sg.theme("Reddit")

    def mostrar_fretes_para_atualizacao(self, lista_fretes: list[dict], perfil: str = "gerente"):
        layout = []

        # Título com base no perfil
        titulo = "Meus Fretes" if perfil == "caminhoneiro" else "Atualizar Status dos Fretes"
        layout.append([
            sg.Text(titulo, font=("Arial", 20), expand_x=True)
        ])

        # Verifica se lista está vazia
        if not lista_fretes:
            layout.append([sg.Text("⚠️ Nenhum frete encontrado.", text_color="red", font=("Arial", 12))])
        else:
            # Cabeçalho
            if perfil == "gerente":
                layout.append([
                    sg.Text("ID", size=(5, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Caminhoneiro", size=(15, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Origem", size=(10, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Destino", size=(10, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Status", size=(10, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Prazo", size=(10, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Ações", size=(10, 1), justification='right', font=('Arial', 12, 'bold')),
                ])
            else:
                layout.append([
                    sg.Text("ID", size=(5, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Origem", size=(15, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Destino", size=(15, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Status", size=(10, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Prazo", size=(10, 1), justification='center', font=('Arial', 12, 'bold')),
                    sg.Text("Ações", size=(10, 1), justification='right', font=('Arial', 12, 'bold')),
                ])
            layout.append([sg.HorizontalSeparator()])

            # Lista de fretes
            for frete in lista_fretes:
                if perfil == "gerente":
                    layout.append([
                        sg.Text(str(frete["id"]), size=(5, 1), justification='center'),
                        sg.Text(frete["caminhoneiro"], size=(15, 1), justification='center'),
                        sg.Text(frete["origem"], size=(10, 1), justification='center'),
                        sg.Text(frete["destino"], size=(10, 1), justification='center'),
                        sg.Text(frete["status"], size=(10, 1), justification='center'),
                        sg.Text(frete["prazo_entrega"].strftime("%d/%m/%Y %H:%M") if frete["prazo_entrega"] else "Não definido", size=(15, 1), justification='center'),
                        sg.Text("", size=(8, 1), justification='center'),
                        sg.Button("Atualizar", key=f"atualizar_{frete['id']}", size=(10, 1))
                    ])
                else:
                    # Para o caminhoneiro, o botão só fica habilitado se o frete puder ser atualizado
                    button_disabled = not frete.get("pode_atualizar", True)
                    button_color = ('gray', 'lightgray') if button_disabled else None
                    
                    layout.append([
                        sg.Text(str(frete["id"]), size=(5, 1), justification='center'),
                        sg.Text(frete["origem"], size=(10, 1), justification='center'),
                        sg.Text(frete["destino"], size=(10, 1), justification='center'),
                        sg.Text(frete["status"], size=(10, 1), justification='center'),
                        sg.Text(frete["prazo_entrega"].strftime("%d/%m/%Y %H:%M") if frete["prazo_entrega"] else "Não definido", size=(15, 1), justification='center'),
                        sg.Text("", size=(8, 1), justification='center'),
                        sg.Button("Atualizar", key=f"atualizar_{frete['id']}", size=(10, 1), 
                                 disabled=button_disabled, button_color=button_color)
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
            elif evento.startswith("atualizar_"):
                id_frete = int(evento.split("_")[1])
                self.__window.close()
                return {"acao": "atualizar", "id": id_frete} 