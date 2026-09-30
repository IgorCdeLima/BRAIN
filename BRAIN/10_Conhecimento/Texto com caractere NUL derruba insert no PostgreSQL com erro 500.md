---
tipo: problema-solucao
status: ativo
origem: T-0002, BUG-0004 (curado pelo Bibliotecário a partir do candidato "Parser de valor monetário pt-BR")
confianca: alta
fontes: ["projetos/lab: qualidade/bugs/BUG-0004.md"]
verificado_em: 2026-09-29
valido_para: PostgreSQL + psycopg 3, colunas de texto (varchar/text)
revisar_em: 2027-03-29
criado: 2026-09-29
tags: [postgresql, validacao, psycopg, armadilha]
decisao: promovido
---
# Texto com caractere NUL derruba insert no PostgreSQL com erro 500

## Sintoma

Um campo de texto com `\x00` faz o insert falhar com `psycopg.DataError`, e a API responde 500.

## Ambiente

Aplicação FastAPI com PostgreSQL via psycopg 3 (projeto `lab`, T-0002).

## Causa raiz

O PostgreSQL recusa NUL em `varchar`/`text`. A validação só olhava tamanho e vazio, então a entrada chegava ao banco.

## Solução

Recusar caracteres de controle (`[\x00-\x1f\x7f]`) em campos de texto na validação, com resposta 422.

## Como verificar que foi resolvido

Enviar um texto contendo `\x00` e obter 422 (não 500); incluir o caso na suíte.

## O que não funcionou

Validar apenas tamanho e vazio.

## Origem

BUG-0004 do `lab`. Relacionada: [[Valor em reais com ponto de milhar sem virgula e ambiguo - nao converta direto para Decimal]] (mesma família: validação que deixa passar entrada que quebra depois).

## Decisão do Bibliotecário

Criada em 2026-09-29 a partir do candidato do parser monetário, que misturava várias ideias. Sem fonte externa: a evidência é o bug reproduzido no `lab`.
