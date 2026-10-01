---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/pesquisador
tarefa: T-0012
pesquisa: SEARCH-0003
confianca: media
fontes: ["https://cwe.mitre.org/data/definitions/212.html", "https://pillow.readthedocs.io/en/stable/reference/Image.html"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.x"
criado: 2026-10-01
decisao:
tags: [seguranca, cwe-212, pillow, exif, privacidade]
---
# CWE-212 metadado sensivel em imagem se evita regravando os pixels sem EXIF, GPS e comentarios

## Conteudo proposto

CWE-212: o produto guarda ou serve um recurso sem remover dado sensivel. O exemplo classico em imagem e EXIF com GPS, modelo da camera e data.

Controle: nao servir o arquivo enviado; regravar so os pixels num arquivo novo e servir o novo. Detalhes da stack ja estao nas notas abaixo: aplicar a orientacao EXIF antes de descartar o EXIF, e conferir que o `save` padrao do Pillow ainda pode manter comentario do JPEG e ICC do PNG.

Como testar: enviar JPEG com EXIF/GPS conhecido, baixar o resultado servido e conferir que `getexif()` vem vazio e que `exiftool`/busca de bytes nao acha GPS nem comentario.

## Evidencia

MITRE CWE-212 cita metadados EXIF de imagens e recomenda sanitizacao automatizada antes de armazenar ou transferir. O Pillow expoe `getexif()` para inspecao.

## Links confiaveis

- [MITRE CWE-212](https://cwe.mitre.org/data/definitions/212.html): definicao e mitigacoes.
- [Pillow Image module](https://pillow.readthedocs.io/en/stable/reference/Image.html): `getexif()` para inspecionar o resultado.

## Por que e reaproveitavel

Todo projeto que armazena ou exibe imagens enviadas por usuarios.

## Relacionadas no Brain

- [[Regravar imagem sem EXIF exige aplicar a orientacao antes]]
- [[Pillow save padrao mantem o comentario do JPEG e o ICC do PNG ao regravar sem metadados]]

## Decisao do Bibliotecario
