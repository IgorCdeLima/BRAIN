---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, documentacao]
---
# ADR-0002 Documentação oficial fica no projeto

## Contexto

O Brain poderia concentrar toda a documentação, mas a documentação de um projeto precisa evoluir junto com o código e estar disponível para quem trabalha no repositório.

## Decisão

- A documentação oficial de um projeto (requisitos, modelos UML/C4/ER, ADRs do projeto, qualidade) vive **sempre** dentro do projeto: `projetos/<nome>/docs` e `projetos/<nome>/qualidade`.
- O Brain pode ter notas **sobre** o projeto (`40_Projetos`) para pesquisa futura: visão geral, link, aprendizados reaproveitáveis.

## Alternativas consideradas

| Alternativa | Prós | Contras |
|---|---|---|
| Documentação no Brain | Tudo no Obsidian | Descola da versão do código; agentes em worktrees não a veem versionada junto |

## Consequências

- **Positivas:** docs versionadas com o código (docs-as-code); cada projeto é autocontido.
- **Negativas / riscos:** aprendizados precisam ser promovidos explicitamente ao Brain, ou se perdem.
