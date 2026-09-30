---
tipo: problema-solucao
status: ativo
origem: T-0002 (curado pelo Bibliotecário a partir do candidato "Parser de valor monetário pt-BR")
confianca: alta
fontes: ["projetos/lab: T-0002, BUG-0003 a BUG-0005"]
verificado_em: 2026-09-29
valido_para: projetos com Docker Compose cuja imagem copia o código (COPY) em vez de montar volume
criado: 2026-09-29
tags: [docker, pytest, ambiente, armadilha]
decisao: promovido
---
# Imagem Docker que embute o código exige build antes de rodar pytest

## Sintoma

Depois de editar o código, `docker compose run --rm app pytest` roda a suíte antiga e o resultado não reflete a correção.

## Ambiente

Docker Compose com imagem da aplicação que copia o código no build (projeto `lab`).

## Causa raiz

O código está dentro da imagem; sem novo build, o contêiner usa a versão anterior.

## Solução

Rodar `docker compose build app` antes de `docker compose run --rm app pytest`.

## Como verificar que foi resolvido

O teste novo (ou a correção) aparece na execução; um teste que deveria falhar falha.

## O que não funcionou

Rodar só `run --rm app pytest` após editar.

## Origem

T-0002 do `lab`. Vale para Dev e Revisor ao verificar correções. Relacionada: [[Valor em reais com ponto de milhar sem virgula e ambiguo - nao converta direto para Decimal]] (bugs cuja verificação depende disso).

## Decisão do Bibliotecário

Criada em 2026-09-29 a partir do candidato do parser monetário. Sem fonte externa: é comportamento do próprio projeto.
