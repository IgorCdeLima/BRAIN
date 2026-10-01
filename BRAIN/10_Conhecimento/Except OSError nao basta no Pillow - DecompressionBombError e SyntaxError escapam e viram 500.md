---
tipo: problema-solucao
status: ativo
origem: T-0012 (Seguranca), curado pelo Bibliotecario
tarefa: T-0012
confianca: alta
fontes: ["experimento da Seguranca em 2026-10-01 (python:3.13.15-slim, pillow 12.3.0), registrado em projetos/lab docs/seguranca/T-0012-ameacas.md (E4, E5, E6)", "https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst", "https://cwe.mitre.org/data/definitions/755.html", "https://cwe.mitre.org/data/definitions/409.html"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.3.0; validacao de upload de imagem"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [seguranca, upload, imagem, pillow, excecoes, dos, armadilha, cwe-755, cwe-409]
---
# Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500

## Sintoma

Upload de imagem malformada ou gigante responde erro 500, mesmo com `Image.open`/`load` cercado por `except OSError` (ou `except (OSError, UnidentifiedImageError)`).

## Ambiente

Pillow 12.3.0, Python 3.13.15 (`python:3.13.15-slim`), validacao de upload.

## Causa raiz

Nem toda excecao do Pillow herda de `OSError`:

- `Image.DecompressionBombError` herda **direto de `Exception`**; sai do proprio `Image.open` acima de ~179 MP (dobro do `MAX_IMAGE_PIXELS`).
- PNG malformado levanta **`SyntaxError`** ("broken PNG file") em parte dos casos.
- PNG com IHDR truncado levanta **`ValueError`** ("Truncated IHDR chunk"), achado no fuzz do Revisor (VER-T0012-01).
- `UnidentifiedImageError` herda de `OSError` (essa o habito pega).

## Solucao

Tratar `DecompressionBombError` primeiro (mensagem de dimensao) e depois **qualquer `Exception`** como "arquivo corrompido", com mensagem fixa (sem o texto da excecao).

**Custo do pior caso aceito:** um WebP RGBA de 89 KB com 7071 x 7071 px (50 MP) custa 879 MB de pico e 26 s para decodificar e regravar; o tamanho em bytes nao limita o custo. Limitar decodificacoes simultaneas e a memoria do container.

## Como verificar que foi resolvido

Receitas deterministicas (PNG RGB 64 x 64 gerado pelo Pillow, conferidas em 2026-10-01): tamanho do chunk IDAT trocado por 0 -> `SyntaxError`; tamanho do chunk IHDR trocado por 12 -> `ValueError`. "CRC quebrado" **nao** serve: ver [[Teste de upload com Pillow - CRC do PNG nao e conferido e o ICC do PNG vai comprimido]].

Fuzz com semente fixa via HTTP: status so 303/422. No fuzz de 1.800 arquivos mutados (600 por JPEG/PNG/WebP) as classes vistas foram `OSError`, `UnidentifiedImageError` e `SyntaxError`; varios JPEG/WebP mutados decodificaram sem erro. O fuzz e amostra: nao prova que nao existam outras classes.

## O que nao funcionou

`except OSError` e `except (OSError, UnidentifiedImageError)`: deixam passar as tres excecoes acima.

## Links confiaveis

- [Pillow: Image (docs no GitHub)](https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst): `MAX_IMAGE_PIXELS`, `DecompressionBombWarning`/`Error`.
- [CWE-755 (MITRE)](https://cwe.mitre.org/data/definitions/755.html): tratamento improprio de condicoes excepcionais.
- [CWE-409 (MITRE)](https://cwe.mitre.org/data/definitions/409.html): dados muito comprimidos.

## Relacionadas

- [[Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto]]: origem do `DecompressionBombError` dentro do `open`.
- [[CWE-409 bomba de descompressao se evita com limite de pixels do Pillow tratado como erro e limite de bytes no upload]]: padrao geral.
- [[CWE-20 entrada extrema gerando erro 500 se evita validando com Pydantic e handler global]]: o 500 e o sintoma comum.
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: limite de memoria e concorrencia.

## Origem

T-0012 (analise de ameacas do lab); `DecompressionBombError` medido com `__mro__[1]` igual a `Exception`; contagens e memoria em `projetos/lab/docs/seguranca/T-0012-ameacas.md`. O raciocinio (conferir a hierarquia de excecoes da biblioteca, nao supor) vale para outros parsers.

## Decisao do Bibliotecario

Promovido (2026-10-01) como problema-solucao ativo. Complementa, sem duplicar, a nota do `Image.open`; a hierarquia de excecoes e o custo do pior caso sao conteudo novo.
