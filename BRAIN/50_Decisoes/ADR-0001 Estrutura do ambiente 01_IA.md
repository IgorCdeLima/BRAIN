---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente]
---
# ADR-0001 Estrutura do ambiente 01_IA

## Contexto

O ambiente precisa abrigar conhecimento (Obsidian), definições de agentes, estado operacional e projetos de código, que têm naturezas e ritmos de mudança diferentes. As sessões de trabalho acontecem em `01_IA`, não dentro do Vault.

## Decisão

- `D:\01_IA` é a raiz do ambiente e do repositório Git principal.
- `BRAIN/` é o Vault Obsidian: somente conhecimento.
- `agentes/` guarda as definições executáveis; `operacao/` guarda tarefas, logs e qualidade; `projetos/` guarda cada projeto como repositório próprio (ignorado pelo repo principal).

## Alternativas consideradas

| Alternativa | Prós | Contras |
|---|---|---|
| Vault na raiz `01_IA` | Tudo visível no Obsidian | Código e `node_modules` deixam o Obsidian lento e poluem busca e grafo |
| Tudo dentro do `BRAIN` | Uma pasta só | Mistura conhecimento com dados operacionais de alta rotatividade; conflitos de escrita |

## Consequências

- **Positivas:** Brain limpo e rápido; operação com muitas escritas fica fora do Vault.
- **Negativas / riscos:** tarefas e logs não aparecem no Obsidian (o painel futuro cobre isso).
