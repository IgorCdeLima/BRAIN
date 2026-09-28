---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, conhecimento]
---
# ADR-0010 Hierarquia de conhecimento

## Contexto

Pesquisas externas repetidas custam tempo e tokens, mas confiar cegamente no Brain ou no conhecimento próprio do modelo gera erros, principalmente em fatos voláteis.

## Decisão

Ordem de consulta:

0. Contexto da tarefa, documentação do projeto e bugs abertos relacionados.
1. Brain — citar a nota usada; nota antiga ou de baixa confiança é pista, não verdade.
2. Classificar a dúvida: conceito estável → conhecimento próprio; fato volátil (versão, API, preço) → pesquisa externa obrigatória; outra especialidade → consultar especialista (somente leitura).
3. Pesquisa externa → resultado em `00_Inbox` (quarentena).
4. Registro: propor ao Bibliotecário apenas o que é reaproveitável e validado, incluindo resultados negativos.

## Consequências

- **Positivas:** menos pesquisa redundante sem aumentar alucinação em fatos voláteis.
- **Negativas / riscos:** depende de metadados de validade bem preenchidos.
