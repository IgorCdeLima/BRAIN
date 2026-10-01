---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/pesquisador
tarefa: T-0012
pesquisa: SEARCH-0003
confianca: media
fontes: ["https://cwe.mitre.org/data/definitions/409.html", "https://pillow.readthedocs.io/en/stable/reference/Image.html"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.x, Python 3.13"
criado: 2026-10-01
decisao:
tags: [seguranca, cwe-409, pillow, upload, dos]
---
# CWE-409 bomba de descompressao se evita com limite de pixels do Pillow tratado como erro e limite de bytes no upload

## Conteudo proposto

CWE-409 (dados muito comprimidos): arquivo pequeno que expande para volume enorme e esgota CPU/memoria. Em imagem, e a "decompression bomb".

Controles na nossa stack:

1. Limite de bytes do corpo do upload antes de abrir a imagem.
2. Manter `Image.MAX_IMAGE_PIXELS` ligado (nunca `None`). O Pillow emite `DecompressionBombWarning` acima do limite e levanta `DecompressionBombError` acima do dobro.
3. Converter o aviso em erro: `warnings.simplefilter("error", Image.DecompressionBombWarning)`, ou checar `im.size` apos `Image.open` (le so o cabecalho) e recusar antes de `load()`.
4. Capturar `DecompressionBombError` (nao herda de `OSError`) e responder 4xx, nao 500.
5. Timeout e limite de memoria do processo/container como ultima barreira.

Como testar: gerar um PNG de poucos KB com dimensoes acima do dobro do limite e conferir resposta 4xx; gerar um entre 1x e 2x o limite e conferir que o projeto recusa (aviso virou erro).

## Evidencia

MITRE CWE-409 lista como mitigacoes: limite de tamanho antes do processamento, monitorar taxa de expansao, timeouts, validar tamanho de saida. A documentacao do Pillow descreve o limite de pixels e o aviso/erro.

## Links confiaveis

- [MITRE CWE-409](https://cwe.mitre.org/data/definitions/409.html): definicao e mitigacoes.
- [Pillow Image module](https://pillow.readthedocs.io/en/stable/reference/Image.html): `MAX_IMAGE_PIXELS`, aviso e erro de bomba de descompressao.

## Por que e reaproveitavel

Qualquer upload de imagem (ou arquivo comprimido) em projetos Python.

## Relacionadas no Brain

- [[Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto]]
- [[Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500]]
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]

## Decisao do Bibliotecario
