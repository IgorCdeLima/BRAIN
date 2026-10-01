---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/seguranca
tarefa: T-0012
pesquisa:
confianca: alta
fontes: ["experimento da Seguranca em 2026-10-01 (python:3.13.15-slim, pillow 12.3.0), registrado em projetos/lab docs/seguranca/T-0012-ameacas.md (E4, E5, E6)"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.3.0; validacao de upload de imagem"
criado: 2026-10-01
decisao:
tags: [seguranca, upload, imagem, pillow, excecoes, dos, armadilha, cwe-755, cwe-409]
---
# Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500

## Conteudo proposto

Ao validar upload com o Pillow, o habito de cercar `Image.open`/`load` com `except OSError` (ou `except (OSError, UnidentifiedImageError)`) deixa passar excecoes que viram erro 500:

- `Image.DecompressionBombError` herda **direto de `Exception`**, nao de `OSError`; sai do proprio `Image.open` acima de ~179 MP (dobro do `MAX_IMAGE_PIXELS`).
- PNG malformado levanta **`SyntaxError`** ("broken PNG file") em parte dos casos.
- PNG com IHDR truncado levanta **`ValueError`** ("Truncated IHDR chunk"), que tambem nao herda de `OSError` (achado no fuzz do Revisor, VER-T0012-01).
- `UnidentifiedImageError` herda de `OSError` (essa o habito pega).

Receitas deterministicas para teste (conferidas em 2026-10-01, PNG RGB 64 x 64 gerado pelo Pillow): tamanho do chunk IDAT trocado por 0 -> `SyntaxError`; tamanho do chunk IHDR trocado por 12 -> `ValueError`. "CRC quebrado" **nao** serve: ver [[Teste de upload com Pillow - CRC do PNG nao e conferido e o ICC do PNG vai comprimido]].

Num fuzz de 1.800 arquivos mutados (600 por formato JPEG/PNG/WebP: troca de bytes, truncamento, insercao), as classes vistas foram `OSError`, `UnidentifiedImageError` e `SyntaxError`; varios JPEG/WebP mutados decodificaram sem erro.

**Controle:** tratar `DecompressionBombError` primeiro (mensagem de dimensao) e depois **qualquer `Exception`** como "arquivo corrompido", com mensagem fixa (sem o texto da excecao). Testar com fuzz de semente fixa via HTTP: status so 303/422.

**Custo do pior caso aceito (mesmo experimento):** um WebP RGBA de 89 KB com 7071 x 7071 px (50 MP) custa 879 MB de pico e 26 s para decodificar e regravar; o tamanho em bytes nao limita o custo. Limitar decodificacoes simultaneas e a memoria do container.

## Evidencia

Experimento da Seguranca em 2026-10-01 (`docker run python:3.13.15-slim`, `pillow==12.3.0`): `Image.DecompressionBombError.__mro__[1]` e `Exception`; contagem do fuzz e medicoes de memoria em `projetos/lab/docs/seguranca/T-0012-ameacas.md` (E4, E5, E6). O fuzz e amostra: nao prova que nao existam outras classes.

## Links confiaveis

- [Pillow: Image (docs no GitHub)](https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst): `MAX_IMAGE_PIXELS`, `DecompressionBombWarning`/`Error`.
- [CWE-755 (MITRE)](https://cwe.mitre.org/data/definitions/755.html): tratamento improprio de condicoes excepcionais.
- [CWE-409 (MITRE)](https://cwe.mitre.org/data/definitions/409.html): dados muito comprimidos (amplificacao).

## Por que e reaproveitavel

Qualquer validacao de imagem com Pillow; o mesmo raciocinio (conferir a hierarquia de excecoes da biblioteca, nao supor) vale para outros parsers.

## Relacionadas no Brain

- [[Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto]]
- [[CWE-20 entrada extrema gerando erro 500 se evita validando com Pydantic e handler global]]
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]

## Decisao do Bibliotecario
