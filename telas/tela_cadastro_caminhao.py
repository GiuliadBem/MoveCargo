import FreeSimpleGUI as sg

sg.theme("Reddit")

# Layout
layout = [
    [sg.Text("Cadastro de Caminhão")],
    [sg.Text("Placa"), sg.Input(key="placa"), sg.Text("Modelo"), sg.Input(key="modelo")],
    [sg.Text("Marca"), sg.Input(key="marca"), sg.Text("Ano"), sg.Input(key="ano")],
    [],
    [sg.Button("Cadastrar")]
]

# Janela
janela = sg.Window("Cadastro de Caminhão", layout)

# Ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == "Cadastrar":
        print("Caminhão cadastrado com sucesso")