---
tipo: padrao
status: ativo
origem: SEARCH-0003 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0012
pesquisa: SEARCH-0003
confianca: media
fontes: ["https://cwe.mitre.org/data/definitions/409.html", "https://pillow.readthedocs.io/en/stable/reference/Image.html"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.x, Python 3.13"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [seguranca, cwe, cwe-409, pillow, upload, dos]
---
# CWE-409 bomba de descompressao se evita com limite de pixels do Pillow tratado como erro e limite de bytes no upload

## Contexto

CWE-409 (dados muito comprimidos): arquivo pequeno que expande para volume enorme e esgota CPU/memoria. Em imagem e a "decompression bomb". Vale para qualquer upload de imagem (ou arquivo comprimido) em projetos Python.

## Problema

O limite de bytes do upload nao limita o custo: um WebP de 89 KB pode exigir centenas de MB de memoria para decodificar ([[Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500]]).

## Solucao

1. Limite de bytes do corpo do upload antes de abrir a imagem.
2. Manter `Image.MAX_IMAGE_PIXELS` ligado (nunca `None`). O Pillow emite `DecompressionBombWarning` acima do limite e levanta `DecompressionBombError` acima do dobro.
3. Converter o aviso em erro: `warnings.simplefilter("error", Image.DecompressionBombWarning)`, ou checar `im.size` apos `Image.open` (le so o cabecalho) e recusar antes de `load()`.
4. Capturar `DecompressionBombError` (nao herda de `OSError`) e responder 4xx, nao 500.
5. Timeout e limite de memoria do processo/container como ultima barreira.

**Como testar:** gerar um PNG de poucos KB com dimensoes acima do dobro do limite e conferir resposta 4xx; gerar um entre 1x e 2x o limite e conferir que o projeto recusa (aviso virou erro).

## Trade-offs

- **Ganha:** protege CPU e memoria contra arquivo pequeno e caro.
- **Perde:** recusa imagens legitimas muito grandes; o limite padrao do Pillow e alto, entao o projeto deve definir o proprio.

## Quando NAO usar

Servicos internos de processamento de imagens enormes (ex.: cartografia), onde o limite deve ser outro e o isolamento de recursos e obrigatorio.

## Links confiaveis

- [MITRE CWE-409](https://cwe.mitre.org/data/definitions/409.html): definicao e mitigacoes (limite de tamanho antes do processamento, monitorar expansao, timeouts).
- [Pillow Image module](https://pillow.readthedocs.io/en/stable/reference/Image.html): `MAX_IMAGE_PIXELS`, aviso e erro de bomba de descompressao.

## Relacionadas

- [[Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto]]: comportamento medido do `open`.
- [[Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500]]: o erro nao e `OSError`.
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: limites gerais.
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-10-01) como padrao ativo, confianca media (fontes oficiais; comportamento do Pillow ja confirmado em notas com experimento). Indexado no mapa de CWE.
