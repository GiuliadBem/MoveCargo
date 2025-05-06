from datetime import date
from validadores import validador_cpf
import FreeSimpleGUI as sg

class TelaCadastroCaminhoneiro:
    def __init__(self):
        sg.theme("LightGrey1")

    def __criar_layout(self, dados=None, modo_atualizacao=False, campos_editaveis=None):
        dados = dados or {}
        campos_editaveis = campos_editaveis or []

        def campo_habilitado(campo):
            return not modo_atualizacao or campo in campos_editaveis

        layout = [
            [sg.Text("CADASTRO DE CAMINHONEIRO " if not modo_atualizacao else "ATUALIZAÇÃO DE CAMINHONEIRO", font=("Helvetica", 18, "bold"), justification='center', expand_x=True)],
            [sg.Column([
                [sg.Text("Nome completo*", size=(16, 1)), 
                 sg.Input(default_text=dados.get("nome", ""), key="nome", disabled=not campo_habilitado("nome"))],
                [sg.Text("Email", size=(16, 1)), 
                 sg.Input(default_text=dados.get("email", ""), key="email", disabled=not campo_habilitado("email"))],
                [sg.Text("Data de Nascimento*", size=(16, 1)),
                 sg.Input(default_text=dados.get("data_nascimento", ""), key="data_nascimento", size=(20,1), disabled=not campo_habilitado("data_nascimento")),
                 sg.CalendarButton("Selecionar", 
                                target="data_nascimento", 
                                key="cal_data_nascimento",
                                format="%Y-%m-%d",
                                disabled=not campo_habilitado("data_nascimento"))],
                [sg.Text("Usuário*", size=(16, 1)),
                 sg.Input(default_text=dados.get("usuario", ""), key="usuario", disabled=not campo_habilitado("usuario"))],
                [sg.Checkbox("Possui MOPP", default=dados.get("possui_MOPP", False), key="possui_MOPP", disabled=not campo_habilitado("possui_MOPP"))]
            ]),
            sg.VerticalSeparator(),
            sg.Column([
                [sg.Text("CPF*", size=(16, 1)), 
                 sg.Input(default_text=dados.get("cpf", ""), key="cpf", disabled=not campo_habilitado("cpf"))],
                [sg.Text("CNH", size=(16, 1)), 
                 sg.Input(default_text=dados.get("num_cnh", ""), key="num_cnh", disabled=not campo_habilitado("num_cnh"))],
                [sg.Text("Telefone", size=(16, 1)), 
                 sg.Input(default_text=dados.get("telefone", ""), key="telefone", disabled=not campo_habilitado("telefone"))],
                [sg.Text("Senha*", size=(16, 1)),
                 sg.Input(default_text=dados.get("senha", ""), key="senha", password_char="*", disabled=not campo_habilitado("senha"))],
            ])],
            [sg.HorizontalSeparator()],
            [sg.Button("CADASTRAR" if not modo_atualizacao else "ATUALIZAR", key="salvar", button_color=("white", "#3B2EFF"), size=(15, 1)),
             sg.Button("VOLTAR", key="voltar", button_color=("white", "#B0B0B0"), size=(15, 1))],
        ]
        return layout

    def __abrir_janela(self, dados=None, titulo="Cadastro", modo_atualizacao=False, campos_editaveis=None):
        layout = self.__criar_layout(dados, modo_atualizacao, campos_editaveis)
        return sg.Window(titulo, layout, finalize=True)

    def pega_dados_cadastro(self):
        #Janela para Cadastrar Novo Caminhoneiro
        window = self.__abrir_janela(titulo="Cadastrar Caminhoneiro")

        while True:
            evento, valores = window.read()

            if evento in (sg.WINDOW_CLOSED, "voltar"):
                break

            if evento == "salvar":
                campos_obrigatorios = ["nome", "cpf", "data_nascimento", "usuario", "senha"]
                for campo in campos_obrigatorios:
                    if not valores[campo]:
                        sg.popup_error(f"O campo '{campo}' é obrigatório.")
                        break
                    elif not validador_cpf.validar_cpf(valores["cpf"]):
                        sg.popup_error("CPF inválido. Verifique se está no padrão '000.000.000-00'.")
                        break
                else:
                    window.close()
                    return valores

        window.close()
        return None

    def pega_dados_atualizacao(self, dados_antigos, campos_editaveis=None):
        #Janela para Atualizar Caminhoneiro
        window = self.__abrir_janela(dados=dados_antigos, titulo="Atualizar Caminhoneiro",
                                     modo_atualizacao=True, campos_editaveis=campos_editaveis)

        while True:
            evento, valores = window.read()

            if evento in (sg.WINDOW_CLOSED, "voltar"):
                break

            if evento == "salvar":
                campos_obrigatorios = ["nome", "cpf", "data_nascimento"]
                for campo in campos_obrigatorios:
                    if campo in campos_editaveis and not valores[campo]:
                        sg.popup_error(f"O campo '{campo}' é obrigatório.")
                        break
                    elif not validador_cpf.validar_cpf(valores["cpf"]):
                        sg.popup_error("CPF inválido. Verifique se está no padrão '000.000.000-00'.")
                        break
                else:
                    window.close()
                    return valores

        window.close()
        return None
