---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, brain, zettelkasten]
---
# ADR-0007 Brain com Zettelkasten e curadoria única

## Contexto

Vários agentes vão consultar e gerar conhecimento. Sem regras, o Brain vira um acúmulo de fragmentos duplicados, desatualizados ou contaminados por pesquisa não verificada.

## Decisão

- Princípios do **Zettelkasten apenas para o conhecimento**: notas atômicas, título como afirmação, síntese com palavras próprias, links explícitos, separação entre referência (o que a fonte diz) e conhecimento (o que concluímos), mapas (MOCs) emergentes.
- **Não aplicar**: IDs sequenciais de Luhmann, proibição de pastas, Zettelkasten para documentação de projeto, atomização sem curadoria.
- **Um único escritor**: o Bibliotecário escreve fora de `00_Inbox`; os demais propõem candidatos.
- **Quarentena**: pesquisa externa entra em `00_Inbox` como não confiável.
- Metadados de confiança: `confianca`, `fontes`, `verificado_em`, `valido_para`, `revisar_em`.

## Consequências

- **Positivas:** notas pequenas e bem tituladas são ideais para consulta por agentes; erros não se propagam sem curadoria.
- **Negativas / riscos:** o Bibliotecário pode virar gargalo; exige revisão periódica.
