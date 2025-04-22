import FreeSimpleGUI as sg

class TelaCadastroCaminhoneiro:
    def __init__(self):
        sg.theme("LightGrey1")

    def __criar_layout(self, dados=None, modo_atualizacao=False):
        dados = dados or {}
        layout = [
            [sg.Text("CADASTRO DE CAMINHONEIRO", font=("Helvetica", 18, "bold"), justification='center', expand_x=True)],
            [sg.Column([
                [sg.Text("Nome completo*", size=(16, 1)), sg.Input(default_text=dados.get("nome", ""), key="nome")],
                [sg.Text("Email", size=(16, 1)), sg.Input(default_text=dados.get("email", ""), key="email")],
                [sg.Text("Data de Nascimento*", size=(16, 1)), sg.Input(default_text=dados.get("data_nascimento", ""), key="data_nascimento")],
                [sg.Text("Usuário*", size=(16, 1)),
                sg.Input(default_text=dados.get("usuario", ""), key="usuario", disabled=modo_atualizacao)],
                [sg.Checkbox("Possui MOPP", default=dados.get("possui_MOPP", False), key="possui_MOPP")]
            ]),
            sg.VerticalSeparator(),
            sg.Column([
                [sg.Text("CPF*", size=(16, 1)), sg.Input(default_text=dados.get("cpf", ""), key="cpf")],
                [sg.Text("CNH", size=(16, 1)), sg.Input(default_text=dados.get("num_cnh", ""), key="num_cnh")],
                [sg.Text("Telefone", size=(16, 1)), sg.Input(default_text=dados.get("telefone", ""), key="telefone")],
                [sg.Text("Senha*", size=(16, 1)),
                sg.Input(default_text=dados.get("senha", ""), key="senha", password_char="*", disabled=modo_atualizacao)],
            ])],
            [sg.HorizontalSeparator()],
            [sg.Button("CADASTRAR" if not modo_atualizacao else "ATUALIZAR", key="salvar", button_color=("white", "#3B2EFF"), size=(15, 1)),
            sg.Button("VOLTAR", key="voltar", button_color=("white", "#B0B0B0"), size=(15, 1))],
        ]
        return layout

    def __abrir_janela(self, dados=None, titulo="Cadastro", modo_atualizacao=False):
        layout = self.__criar_layout(dados, modo_atualizacao)
        return sg.Window(titulo, layout, finalize=True)

    def pega_dados_cadastro(self):
        """Janela para Cadastrar Novo Caminhoneiro"""
        window = self.__abrir_janela(titulo="Cadastrar Caminhoneiro")

        while True:
            evento, valores = window.read()

            if evento in (sg.WINDOW_CLOSED, "voltar"):
                break

            if evento == "salvar":
                campos_obrigatorios = ["nome", "cpf", "data_nascimento", "usuario", "senha"]
                for campo in campos_obrigatorios:
                    if not valores[campo]:
                        sg.popup_error(f"⚠️ O campo '{campo}' é obrigatório.")
                        break
                else:
                    window.close()
                    return valores

        window.close()
        return None

    def pega_dados_atualizacao(self, dados_antigos):
        """Janela para Atualizar Caminhoneiro"""
        window = self.__abrir_janela(dados=dados_antigos, titulo="Atualizar Caminhoneiro", modo_atualizacao=True)

        while True:
            evento, valores = window.read()

            if evento in (sg.WINDOW_CLOSED, "voltar"):
                break

            if evento == "salvar":
                campos_obrigatorios = ["nome", "cpf", "data_nascimento"]
                for campo in campos_obrigatorios:
                    if not valores[campo]:
                        sg.popup_error(f"⚠️ O campo '{campo}' é obrigatório.")
                        break
                else:
                    window.close()
                    return valores

        window.close()
        return None