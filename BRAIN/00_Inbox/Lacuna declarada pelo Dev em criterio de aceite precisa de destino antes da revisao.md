---
tipo: candidato
status: inbox
tipo_proposto: aprendizado
origem: agente/engenheiro
tarefa: T-0006
pesquisa:
confianca: media
fontes: ["operacao/tarefas/T-0003.md (Entrega da rodada 1)", "projetos/lab: SEC-0001, VER-0006"]
verificado_em: 2026-09-30
valido_para: "Fluxo de tarefa v3, papel Dev"
criado: 2026-09-30
decisao:
tags: [retrospectiva, fluxo, dev, entrega, proposta-n4]
---
# Lacuna declarada pelo Dev em criterio de aceite precisa de destino antes da revisao

## Conteudo proposto

Na T-0003 o Dev listou "requisicao chunked sem Content-Length" como NAO verificado e entregou. O Revisor confirmou o problema (SEC-0001) e a tarefa voltou para correcao. A lacuna estava honesta, mas sem destino.

**Proposta ao humano (M3, area N4):** separar as lacunas da Entrega em dois tipos.

- **Toca criterio de aceite ou verificacao obrigatoria** (ex.: limite de upload numa tarefa de upload, `seguranca: sim`): antes de `revisao`, o Dev ou fecha a lacuna, ou a registra em "Passos do humano" com o motivo (o humano decide se segue assim).
- **Demais lacunas:** continuam so declaradas, como hoje.

Bloquear toda lacuna foi descartado: incentivaria esconder lacunas, e a declaracao honesta e o que permitiu ao Revisor ir direto ao ponto.

## Evidencia

Cartao T-0003 (Entrega da rodada 1: "NAO verificado: ... requisicao chunked sem Content-Length"), SEC-0001 (historico: "a lacuna ja estava declarada pelo Dev"), VER-0006 reprovado.

## Links confiaveis

- Retrospectiva no projeto: `projetos/lab/docs/retrospectivas/T-0006 retrospectiva T-0003 a T-0005.md`.

## Por que e reaproveitavel

Vale para toda Entrega do Dev e, por analogia, para o Designer e o Engenheiro.

## Relacionadas no Brain

- [[Regra de fluxo sem portao no lancador nao e seguida]]

## Decisao do Bibliotecario
