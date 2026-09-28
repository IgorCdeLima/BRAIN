---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, modelagem, diagramas]
---
# ADR-0008 Mermaid como padrão de diagramas

## Contexto

O agente de Engenharia de Software produzirá diagramas (UML, C4, ER). Eles precisam ser revisáveis no Git e legíveis por agentes.

## Decisão

- **Mermaid** é o padrão para todos os diagramas.
- PlantUML apenas se faltar algum recurso específico da UML.
- **Imagem nunca é a fonte de verdade** de um diagrama.
- O tipo de diagrama é proporcional ao tamanho da tarefa (contexto, casos de uso, atividades, classes, ER, sequência, estados, C4, implantação).

## Alternativas consideradas

| Alternativa | Prós | Contras |
|---|---|---|
| PlantUML | UML completa | Exige Java/servidor e plugin no Obsidian |
| Imagens (draw.io, PNG) | Visual livre | Diff ilegível; agentes não leem com confiabilidade |

## Consequências

- **Positivas:** diffs legíveis; renderiza nativamente no Obsidian e no GitHub; agentes escrevem e leem bem.
- **Negativas / riscos:** alguns detalhes de UML e layout são limitados no Mermaid.
