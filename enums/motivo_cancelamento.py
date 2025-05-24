from enum import Enum

class MotivoCancelamento(Enum):
    AVARIA_NO_VEICULO = "Avaria no Veículo"
    CONDICOES_CLIMATICAS = "Condições Climáticas"
    DESISTENCIA_DO_CLIENTE = "Desistência do Cliente"
    PROBLEMA_NOTA_FISCAL = "Problema com Nota Fiscal"
    FALTA_DE_DISPONIBILIDADE = "Falta de Disponibilidade"
    CARGA_INAPROPRIADA = "Carga Inapropriada"
    ROTAS_BLOQUEADAS = "Rotas Bloqueadas"
    CANCELAMENTO_OPERACIONAL = "Cancelamento Operacional"
    FALTA_DE_TEMPO_HABIL = "Falta de Tempo Habil"
    OUTRO = "Outro" 