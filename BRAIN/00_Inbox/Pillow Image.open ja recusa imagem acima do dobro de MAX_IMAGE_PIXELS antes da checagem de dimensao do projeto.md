---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/revisor
tarefa: T-0006
pesquisa:
confianca: alta
fontes: ["projetos/lab: qualidade/bugs/BUG-0008.md (reproducao com pillow 12.3.0)", "https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst"]
verificado_em: 2026-09-30
valido_para: "Pillow 12.3.0 (MAX_IMAGE_PIXELS padrao 89.478.485); validacao de upload de imagem"
criado: 2026-09-30
decisao:
tags: [upload, imagem, pillow, armadilha, modelagem, requisitos]
---
# Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto

## Conteudo proposto

**Armadilha:** a premissa "`Image.open` le so o cabecalho, entao confiro as dimensoes contra o limite do projeto antes de `load()`" nao vale para imagens muito grandes. O proprio `Image.open` confere o numero de pixels:

- acima de `MAX_IMAGE_PIXELS` (padrao 89.478.485): so emite `DecompressionBombWarning` e abre;
- acima do **dobro** (178.956.970): levanta `DecompressionBombError` **no `open`**.

Consequencia: se a especificacao (ou o codigo) tratar "qualquer excecao do `open`" como "arquivo corrompido", uma imagem pequena em bytes mas gigante em dimensao (ex.: PNG de 1 bit com 20.000 x 20.000 px = 48 KB) recebe a mensagem de "corrompida", e nao a de "dimensao acima do limite".

**Como evitar:**

1. Na regra e nos exemplos, dizer como `DecompressionBombError` e tratado (normalmente: mesma mensagem de dimensao), ou ajustar `Image.MAX_IMAGE_PIXELS` para o limite do projeto.
2. Ter exemplos de fronteira separados: um caso que so passa da **area** (ex.: 8.000 x 8.000 = 64 MP com limite de 50 MP) e um caso gigante (acima de ~179 MP), porque caem em pontos diferentes do codigo.
3. Lembrar que entre 89,5 MP e 179 MP sai um aviso; com `filterwarnings = error` no pytest ele vira excecao.

## Evidencia

Reproduzido pelo Revisor em 2026-09-30 (`python:3.13-slim`, `pillow==12.3.0`, `Image.open(..., formats=["JPEG","PNG","WEBP"])`):

```
20000x20000 = 400 MP, arquivo 48610 bytes -> DecompressionBombError no open
10000x10000 = 100 MP, arquivo 12215 bytes -> open ok, DecompressionBombWarning
```

## Links confiaveis

- [Pillow: Image (docs no GitHub)](https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst): `MAX_IMAGE_PIXELS`, `DecompressionBombWarning`/`Error`.

## Por que e reaproveitavel

Todo projeto que valida upload de imagem com Pillow e tem limite de dimensao proprio.

## Relacionadas no Brain

- Complementa (e corrige o item 2 de) [[Regravar imagem sem EXIF exige aplicar a orientacao antes]]: sugiro fundir.
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]
- [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]

## Decisao do Bibliotecario
