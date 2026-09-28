---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, orca]
---
# ADR-0005 Orca como plataforma de execução

## Contexto

A equipe de agentes precisa de isolamento entre tarefas paralelas, acompanhamento do estado, delegação e revisão de diffs.

## Decisão

Adotar o **Orca** (onorca.dev, MIT, v1.4.215 instalada) como plataforma de execução:

- Um worktree Git por tarefa.
- Orquestração (runs, tasks, dispatches, mensagens, pontos de decisão) quando for ativada — é recurso experimental.
- Agentes: Claude Code como padrão; outros modelos (ex.: revisores) quando disponíveis.
- Implantação em fases: 1 executor + Bibliotecário → revisor → coordenador → automações.

## Alternativas consideradas

| Alternativa | Prós | Contras |
|---|---|---|
| Só subagentes do Claude Code | Menos peças | Sem painel, sem worktrees gerenciados, sem múltiplos fornecedores |

## Consequências

- **Positivas:** resolve conflitos de arquivos, estado das tarefas, visibilidade e revisão.
- **Negativas / riscos:** por padrão o Orca inicia agentes em modo sem permissões (bypass) — ver [[ADR-0006 Modelo de permissoes]]; orquestração experimental pode mudar; Brain não é gerenciado pelo Orca.
