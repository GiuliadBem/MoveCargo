# Regras de Transição de Status dos Fretes

## Visão Geral

Este documento descreve as regras de transição de status implementadas no sistema de fretes MoveCargo.

## Status Disponíveis

- **NAO_INICIADO**: Frete criado mas ainda não iniciado
- **EM_ANDAMENTO**: Frete em execução
- **SUSPENSO**: Frete temporariamente pausado
- **CONCLUIDO**: Frete finalizado com sucesso
- **CANCELADO**: Frete cancelado

## Regras de Transição

### Transições Permitidas

| Status Atual | Próximos Status Possíveis      | Observações                                                   |
| ------------ | ------------------------------ | ------------------------------------------------------------- |
| NAO_INICIADO | EM_ANDAMENTO, CANCELADO        | Só pode ser iniciado ou cancelado antes de começar            |
| EM_ANDAMENTO | SUSPENSO, CONCLUIDO, CANCELADO | Pode ser suspenso, concluído ou cancelado durante o andamento |
| SUSPENSO     | EM_ANDAMENTO, CANCELADO        | Pode voltar para andamento ou ser cancelado                   |
| CONCLUIDO    | -                              | Status final, não pode ser alterado                           |
| CANCELADO    | -                              | Status final, não pode ser alterado                           |

### Fluxos Típicos

#### Fluxo Normal

```
NAO_INICIADO → EM_ANDAMENTO → CONCLUIDO
```

#### Fluxo com Suspensão

```
NAO_INICIADO → EM_ANDAMENTO → SUSPENSO → EM_ANDAMENTO → CONCLUIDO
```

#### Fluxo de Cancelamento

```
NAO_INICIADO → CANCELADO
EM_ANDAMENTO → CANCELADO
SUSPENSO → CANCELADO
```

## Validações Implementadas

### 1. Validação de Transição

- Sistema verifica se a transição solicitada é permitida
- Mensagem de erro clara quando transição é inválida

### 2. Validação de Estado Final

- Status CONCLUIDO e CANCELADO são finais
- Não permitem alterações posteriores

### 3. Validação de Prazo

- Caminhoneiros não podem atualizar fretes com prazo expirado
- Gerentes podem atualizar mesmo com prazo expirado

### 4. Validação de Permissões

- Caminhoneiros só podem atualizar seus próprios fretes
- Gerentes podem atualizar qualquer frete

## Interface do Usuário

### Para Caminhoneiros

- Mostra apenas status válidos para transição
- Botão de atualização desabilitado para fretes não atualizáveis
- Mensagens de erro específicas

### Para Gerentes

- Mostra apenas status válidos para transição
- Permite atualizações mesmo com prazo expirado
- Acesso a todos os fretes

## Implementação Técnica

### Métodos Principais

- `transicao_status_valida()`: Valida se transição é permitida
- `obter_status_validos()`: Retorna lista de status válidos
- `validar_atualizacao_status()`: Validação completa da atualização

### Localização no Código

- **Controlador**: `controladores/controlador_frete.py`
- **Interface**: `telas/tela_cadastro_frete.py`
- **Enums**: `enums/status.py`

## Exemplos de Uso

### Exemplo 1: Frete Normal

```python
# Frete criado
frete.status = Status.NAO_INICIADO

# Caminhoneiro inicia o frete
frete.status = Status.EM_ANDAMENTO  # ✅ Válido

# Caminhoneiro conclui o frete
frete.status = Status.CONCLUIDO     # ✅ Válido
```

### Exemplo 2: Frete Suspenso

```python
# Frete em andamento
frete.status = Status.EM_ANDAMENTO

# Gerente suspende o frete
frete.status = Status.SUSPENSO      # ✅ Válido

# Frete retoma
frete.status = Status.EM_ANDAMENTO  # ✅ Válido
```

### Exemplo 3: Transição Inválida

```python
# Frete concluído
frete.status = Status.CONCLUIDO

# Tentativa de alterar status
frete.status = Status.EM_ANDAMENTO  # ❌ Inválido - Status final
```

## Manutenção

### Adicionando Novos Status

1. Adicionar novo status em `enums/status.py`
2. Atualizar regras de transição em `transicao_status_valida()`
3. Atualizar validações em `validar_atualizacao_status()`

### Modificando Regras

1. Alterar dicionário `transicoes_permitidas`
2. Atualizar validações conforme necessário
3. Testar todas as transições afetadas
