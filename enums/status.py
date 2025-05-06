from enum import Enum

class Status(Enum):
    NAO_INICIADO = "Não Iniciado"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"
    SUSPENSO = "Suspenso"
    CANCELADO = "Cancelado"