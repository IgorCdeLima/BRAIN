---
tipo: aprendizado
status: ativo
origem: T-0006 (Engenheiro, retrospectiva T-0003 a T-0005), curado pelo Bibliotecario
tarefa: T-0006
confianca: media
fontes: ["operacao/tarefas/T-0003.md (Entrega da rodada 1)", "projetos/lab: SEC-0001, VER-0006", "projetos/lab: docs/retrospectivas/T-0006 retrospectiva T-0003 a T-0005.md"]
verificado_em: 2026-09-30
valido_para: "Fluxo de tarefa v3, papel Dev"
revisar_em: 2027-03-30
criado: 2026-09-30
decisao: promovido
tags: [retrospectiva, fluxo, dev, entrega, proposta-n4]
---
# Lacuna declarada pelo Dev em criterio de aceite precisa de destino antes da revisao

## O que aconteceu

Na T-0003 o Dev listou "requisicao chunked sem Content-Length" como NAO verificado e entregou. O Revisor confirmou o problema (SEC-0001) e a tarefa voltou para correcao (VER-0006 reprovado). A lacuna estava honesta, mas sem destino.

## O que aprendemos

Declarar a lacuna nao basta quando ela toca um criterio de aceite. Mas bloquear toda lacuna foi descartado: incentivaria esconder lacunas, e a declaracao honesta foi o que permitiu ao Revisor ir direto ao ponto.

## O que muda a partir de agora

**Proposta ao humano (M3, area N4; pendente):** separar as lacunas da Entrega em dois tipos.

- **Toca criterio de aceite ou verificacao obrigatoria** (ex.: limite de upload numa tarefa de upload, `seguranca: sim`): antes de `revisao`, o Dev ou fecha a lacuna, ou a registra em "Passos do humano" com o motivo (o humano decide se segue assim).
- **Demais lacunas:** continuam so declaradas, como hoje.

Vale para toda Entrega do Dev e, por analogia, para o Designer e o Engenheiro.

## Origem

Cartao T-0003 e SEC-0001 (historico: "a lacuna ja estava declarada pelo Dev"). Retrospectiva no projeto: `projetos/lab/docs/retrospectivas/T-0006 retrospectiva T-0003 a T-0005.md`.

## Relacionadas no Brain

- [[Regra de fluxo sem portao no lancador nao e seguida]]: outra falha de fluxo da mesma retrospectiva.
- [[T-0002 mostrou que regra de entrada ambigua vira bug e que o Revisor precisa testar extremos]]: retrospectiva anterior com o mesmo tipo de proposta N4.

## Decisao do Bibliotecario

Promovido a `10_Conhecimento` (2026-09-30): licao com evidencia rastreavel; a mudanca de fluxo segue como proposta ao humano (N4), sem edicao minha.
