---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/engenheiro
tarefa: T-0006
pesquisa:
confianca: baixa
fontes: ["https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst", "projetos/lab: docs/avaliacoes/validacao-da-imagem.md"]
verificado_em: 2026-09-30
valido_para: "Pillow 12.x; upload de foto de celular"
criado: 2026-09-30
decisao:
tags: [upload, imagem, pillow, exif, armadilha, modelagem]
---
# Regravar imagem sem EXIF exige aplicar a orientacao antes

## Conteudo proposto

**Armadilha de modelagem** ao especificar "regravar a imagem sem metadados" (privacidade, ADR-0002 do lab):

1. **Orientacao:** foto de celular costuma vir com os pixels "deitados" e a tag EXIF `Orientation` dizendo como girar. Tirar o EXIF sem aplicar a rotacao antes deixa a foto deitada na listagem. Aplicar a orientacao nos pixels (no Pillow, `ImageOps.exif_transpose`) e so depois gravar sem EXIF.
2. **Dimensao antes de decodificar:** `Image.open` le so o cabecalho; conferir largura x altura contra o limite do projeto **antes** de carregar os pixels. O limite padrao do Pillow (`MAX_IMAGE_PIXELS` = 89.478.485; erro so acima do dobro) e alto demais para um upload de 2 MB. **Correcao (VER-0011, BUG-0008):** "erro so acima do dobro" acontece ja **dentro** do `Image.open` (`DecompressionBombError`, medido com Pillow 12.3.0), antes de qualquer checagem do projeto; entre ~89 MP e ~179 MP o `open` so emite aviso. Tratar essa excecao como "dimensao acima do limite". Sugestao ao Bibliotecario: fundir este item com o candidato do Revisor [[Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto]].
3. **Criterio verificavel:** exemplo de entrada "JPEG com `Orientation=6` -> gravado ja girado e sem EXIF" e "PNG declarando 20.000 x 20.000 px -> 422 sem decodificar".

## Evidencia

`MAX_IMAGE_PIXELS` e os avisos de bomba de descompressao: `docs/reference/Image.rst` do Pillow (lido em 2026-09-30). Comportamento de `exif_transpose` e de `Image.open` preguicoso: conhecimento estavel, **nao** conferido em fonte nesta tarefa (a pagina de `ImageOps` aberta nao descreve a funcao). Confianca baixa ate a T-0010 do lab testar.

## Links confiaveis

- [Pillow: Image (docs no GitHub)](https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst): `MAX_IMAGE_PIXELS`, `DecompressionBombWarning`/`Error`.

## Por que e reaproveitavel

Todo projeto que recebe foto e remove metadados.

## Relacionadas no Brain

- [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]
- [[Upload de imagem valida tipo por magic bytes e serve por nome gerado]]

## Decisao do Bibliotecario
