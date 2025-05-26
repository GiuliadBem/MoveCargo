import hashlib

from enums import status
from enums.status import Status
from modelos.notificacao import Notificacao
from modelos.pessoa import Pessoa
from datetime import datetime, timedelta

from telas.tela_notificacoes import TelaNotificacoes

class ControladorNotificacoes:
    def __init__(self, controlador_sistema):
        self.__sistema = controlador_sistema
        self.__tela_notificacoes = TelaNotificacoes()

    #---------------------------------------------------------------
    # Métodos
    #---------------------------------------------------------------

    def receber_notificacoes (self, pessoa: Pessoa):
        # Lista de fretes vinda do controlador de fretes
        lista_fretes = self.__sistema.controlador_frete.lista_fretes
        ctrl_caminhoneiro = self.__sistema.controlador_caminhoneiro
        ctrl_gerente = self.__sistema.controlador_gerente

        # Limpar notificações para teste
        #pessoa.limpar_notificacoes()

        # Gerente
        if (pessoa.usuario == "gerente"):
            for frete in lista_fretes:
                # Frete com prazo expirado
                if datetime.now() > frete.prazo_entrega and frete.status not in [Status.CONCLUIDO, Status.CANCELADO]:
                    notificacao = Notificacao(f"O caminhoneiro {frete.caminhoneiro.nome} (ID: {frete.caminhoneiro.id}) não cumpriu o prazo de entrega de seu frete atual.")
                    ctrl_gerente.notifica_gerente(notificacao)

                # Falta menos de 1 hora para o prazo
                tempo_restante = frete.prazo_entrega - datetime.now()
                if timedelta(0) < tempo_restante <= timedelta(hours=1) and frete.status not in [Status.CONCLUIDO, Status.CANCELADO]:
                    notificacao = Notificacao(f"Falta menos de uma hora para o prazo de entrega para o frete do caminhoneiro {frete.caminhoneiro.nome} (ID: {frete.caminhoneiro.id}).")
                    ctrl_gerente.notifica_gerente(notificacao)

        # Caminhoneiro
        else:
            for frete in lista_fretes:
                if frete.caminhoneiro.usuario == pessoa.usuario:
                    # Frete não iniciado
                    if frete.status == Status.NAO_INICIADO:
                        notificacao = Notificacao("Você tem um frete em status não iniciado.")
                        ctrl_caminhoneiro.notifica_caminhoneiro(frete.caminhoneiro.id, notificacao)

                    # Frete com prazo expirado
                    if datetime.now() > frete.prazo_entrega and frete.status not in [Status.CONCLUIDO, Status.CANCELADO]:
                        notificacao = Notificacao("Você não cumpriu o prazo de conclusão do frete a que está atribuido.")
                        ctrl_caminhoneiro.notifica_caminhoneiro(frete.caminhoneiro.id, notificacao)

                    # Falta menos de 1 hora para o prazo
                    tempo_restante = frete.prazo_entrega - datetime.now()
                    if timedelta(0) < tempo_restante <= timedelta(hours=1) and frete.status not in [Status.CONCLUIDO, Status.CANCELADO]:
                        notificacao = Notificacao("Falta menos de uma hora para o prazo de entrega do seu frete.")
                        ctrl_caminhoneiro.notifica_caminhoneiro(frete.caminhoneiro.id, notificacao)

    def listar_notificacoes_nao_lidas (self, pessoa: Pessoa):
        # Cria lista de notificações não lidas
        notificacoes = []
        for notificacao in pessoa.notificacoes:
            if not notificacao.lida:
                notificacoes.append(notificacao)

        # Retorna lista de notificações
        return notificacoes
    
    def listar_notificacoes (self, pessoa: Pessoa):
        ctrl_caminhoneiro = self.__sistema.controlador_caminhoneiro
        ctrl_gerente = self.__sistema.controlador_gerente
        notificacoes = []

        # Adicionar visualização das notificações.
        for notificacao in pessoa.notificacoes:
            notificacoes.append({
                'lida': notificacao.lida,
                'mensagem': notificacao.mensagem,
                'horario': notificacao.horario
            })
        
        # Exibir tela
        while True:
            botao = self.__tela_notificacoes.mostra_tela(notificacoes) # type: ignore
            match botao:
                case "Voltar": break
        
        # Marcar notificações como lidas
        if pessoa.usuario == "gerente":
            ctrl_gerente.marcar_notificacoes_como_lidas()
        else:
            ctrl_caminhoneiro.marcar_notificacoes_como_lidas(pessoa.id)