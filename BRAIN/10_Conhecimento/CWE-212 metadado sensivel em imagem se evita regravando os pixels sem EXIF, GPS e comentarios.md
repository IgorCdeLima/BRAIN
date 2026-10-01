---
tipo: padrao
status: ativo
origem: SEARCH-0003 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0012
pesquisa: SEARCH-0003
confianca: media
fontes: ["https://cwe.mitre.org/data/definitions/212.html", "https://pillow.readthedocs.io/en/stable/reference/Image.html"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.x"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [seguranca, cwe, cwe-212, pillow, exif, privacidade]
---
# CWE-212 metadado sensivel em imagem se evita regravando os pixels sem EXIF, GPS e comentarios

## Contexto

CWE-212: o produto guarda ou serve um recurso sem remover dado sensivel. O exemplo classico em imagem e EXIF com GPS, modelo da camera e data. Vale para todo projeto que armazena ou exibe imagens enviadas por usuarios.

## Problema

Servir o arquivo exatamente como foi enviado entrega ao proximo visitante a localizacao e os dados do aparelho de quem enviou.

## Solucao

Nao servir o arquivo enviado: regravar so os pixels num arquivo novo e servir o novo. A MITRE recomenda sanitizacao automatizada antes de armazenar ou transferir.

Cuidados da stack (Pillow), ja medidos em outras notas:

- aplicar a orientacao EXIF antes de descartar o EXIF;
- o `save` padrao ainda pode manter o comentario do JPEG e o ICC do PNG.

Detalhes: [[Pillow save padrao mantem o comentario do JPEG e o ICC do PNG ao regravar sem metadados]].

**Como testar:** enviar JPEG com EXIF/GPS conhecido, baixar o resultado servido e conferir que `getexif()` vem vazio e que `exiftool` ou busca de bytes nao acha GPS nem comentario. Atencao: no PNG, `zTXt`/`iCCP` vao comprimidos, entao busca de bytes nao basta ([[Teste de upload com Pillow - CRC do PNG nao e conferido e o ICC do PNG vai comprimido]]).

## Trade-offs

- **Ganha:** privacidade do usuario e neutralizacao de conteudo anexado.
- **Perde:** perfil de cor e metadados legitimos; custo de decodificar e regravar.

## Quando NAO usar

Quando o metadado e o proprio produto (ex.: galeria de fotografia que exibe EXIF de proposito, com consentimento).

## Links confiaveis

- [MITRE CWE-212](https://cwe.mitre.org/data/definitions/212.html): definicao e mitigacoes.
- [Pillow Image module](https://pillow.readthedocs.io/en/stable/reference/Image.html): `getexif()` para inspecionar o resultado.

## Relacionadas

- [[Pillow save padrao mantem o comentario do JPEG e o ICC do PNG ao regravar sem metadados]]: o que sobra apos regravar.
- [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]: mesmo fluxo de upload.
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-10-01) como padrao ativo, confianca media (fonte MITRE lida pelo Pesquisador; teste sugerido nao rodado nesta nota). Indexado no mapa de CWE.
