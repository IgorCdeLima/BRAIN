---
tipo: problema-solucao
status: ativo
origem: T-0006 (Revisor, BUG-0008 do lab), curado pelo Bibliotecario
tarefa: T-0006
confianca: alta
fontes: ["projetos/lab: qualidade/bugs/BUG-0008.md (reproducao com pillow 12.3.0)", "https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst"]
verificado_em: 2026-09-30
valido_para: "Pillow 12.3.0 (MAX_IMAGE_PIXELS padrao 89.478.485); validacao de upload de imagem"
revisar_em: 2027-03-30
criado: 2026-09-30
decisao: promovido
tags: [upload, imagem, pillow, armadilha, modelagem, requisitos]
---
# Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto

## Sintoma

Uma imagem pequena em bytes mas gigante em dimensao (ex.: PNG de 1 bit com 20.000 x 20.000 px = 48 KB) recebe a mensagem de "arquivo corrompido" em vez de "dimensao acima do limite", porque a excecao sai do `Image.open`, antes da checagem de dimensao do projeto.

## Ambiente

Pillow 12.3.0 (`python:3.13-slim`), `Image.open(..., formats=["JPEG","PNG","WEBP"])`. `MAX_IMAGE_PIXELS` padrao = 89.478.485.

## Causa raiz

A premissa "`Image.open` le so o cabecalho, entao confiro as dimensoes antes de `load()`" nao vale para imagens muito grandes: o proprio `open` confere o numero de pixels.

- acima de `MAX_IMAGE_PIXELS`: so emite `DecompressionBombWarning` e abre;
- acima do **dobro** (178.956.970): levanta `DecompressionBombError` **no `open`**.

Se a especificacao ou o codigo tratar "qualquer excecao do `open`" como "corrompido", a mensagem sai errada.

## Solucao

1. Na regra e nos exemplos, dizer como `DecompressionBombError` e tratado (normalmente: mesma mensagem de dimensao), ou ajustar `Image.MAX_IMAGE_PIXELS` para o limite do projeto.
2. Exemplos de fronteira separados: um caso que so passa da **area** (ex.: 8.000 x 8.000 = 64 MP com limite de 50 MP) e um caso gigante (acima de ~179 MP), porque caem em pontos diferentes do codigo.
3. Entre 89,5 MP e 179 MP sai um aviso; com `filterwarnings = error` no pytest ele vira excecao.

## Como verificar que foi resolvido

Reproduzido pelo Revisor em 2026-09-30:

```
20000x20000 = 400 MP, arquivo 48610 bytes -> DecompressionBombError no open
10000x10000 = 100 MP, arquivo 12215 bytes -> open ok, DecompressionBombWarning
```

Os dois casos de fronteira do item 2 devem ter teste proprio.

## O que nao funcionou

Confiar que `Image.open` e preguicoso e que so `load()` decodifica (a premissa do ADR/avaliacao de validacao de imagem do lab).

## Origem

T-0006 do lab, verificacao VER-0011 e BUG-0008. Corrige o item 2 do candidato "Regravar imagem sem EXIF exige aplicar a orientacao" (ver [[Upload de imagem valida tipo por magic bytes e serve por nome gerado]]).

## Links confiaveis

- [Pillow: Image (docs no GitHub)](https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst): `MAX_IMAGE_PIXELS`, `DecompressionBombWarning`/`Error`.

## Relacionadas no Brain

- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: o limite de dimensao e um limite de recurso.
- [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]: a validacao de upload em que a armadilha aparece.
- [[Upload de imagem valida tipo por magic bytes e serve por nome gerado]]: mesma validacao, etapa de tipo.
- [[Checklist de entradas extremas precisa de itens proprios para upload]]: os casos extremos que pegam esta armadilha.

## Decisao do Bibliotecario

Promovido a `10_Conhecimento` (2026-09-30): reproduzido com numeros pelo Revisor. O candidato "Regravar imagem..." sugeriu fundir; o item de dimensao dele ficou aqui, e o restante (EXIF) foi devolvido por falta de fonte.
