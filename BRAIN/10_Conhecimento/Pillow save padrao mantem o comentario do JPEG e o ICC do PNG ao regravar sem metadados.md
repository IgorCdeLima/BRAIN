---
tipo: problema-solucao
status: ativo
origem: T-0012 (Seguranca), curado pelo Bibliotecario; incorpora o item de orientacao do candidato da T-0006 (Engenheiro)
tarefa: T-0012
confianca: alta
fontes: ["experimento da Seguranca em 2026-10-01 (python:3.13.15-slim, pillow 12.3.0), registrado em projetos/lab docs/seguranca/T-0012-ameacas.md (E1, E2, E3, E7)", "https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst", "https://cwe.mitre.org/data/definitions/212.html"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.3.0; regravacao de upload de imagem JPEG/PNG/WebP"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [seguranca, upload, imagem, pillow, metadados, privacidade, armadilha, cwe-212, exif]
---
# Pillow save padrao mantem o comentario do JPEG e o ICC do PNG ao regravar sem metadados

## Sintoma

Upload regravado com `Image.open(...)`, `load()`, `ImageOps.exif_transpose(im)` e `im.save(buf, formato)` **sem argumentos** nao fica "sem metadados" por completo: o comentario do JPEG e o ICC do PNG continuam no arquivo servido.

## Ambiente

Pillow 12.3.0, Python 3.13.15, regravacao de JPEG/PNG/WebP. Arquivos de teste gerados pelo proprio Pillow; **nao** testado com fotos reais de celular.

## Causa raiz

O `save` padrao descarta uns metadados e repassa outros, e cada formato se comporta de um jeito:

| Metadado | JPEG | PNG | WebP |
|---|---|---|---|
| EXIF (inclusive GPS) | some | some | some |
| XMP | some | some | some |
| Texto (tEXt/iTXt) | - | some | - |
| Comentario COM | **sobrevive** | - | - |
| Perfil ICC | some | **sobrevive** (ate ICC invalido) | some |

## Solucao

1. **Orientacao primeiro:** foto de celular vem com pixels "deitados" e a tag EXIF `Orientation`. Aplicar `ImageOps.exif_transpose` **antes** de gravar sem EXIF, senao a foto fica deitada. Confirmado: 40x20 com Orientation=6 -> 20x40, e o EXIF nao volta no `save` sem argumentos.
2. Comentario do JPEG: passar `comment=b""` no `save` ou retirar `comment` de `im.info` (ambos testados).
3. ICC: decidir a regra e aplica-la explicitamente nos tres formatos. Repassado como veio (`icc_profile=im.info["icc_profile"]`), o ICC leva qualquer byte anexado ao arquivo final (testado com `<script>` + 200 KB). `ImageCms.ImageCmsProfile(io.BytesIO(icc)).tobytes()` reserializa so o perfil e descarta o anexo.
4. JPEG com segmento MPF (varias imagens) abre como `format == "MPO"` mesmo com `formats=["JPEG"]`; comparar com `"JPEG"` recusa o arquivo. Salvo como `"JPEG"`, sai 1 quadro.
5. Conteudo anexado depois do fim do arquivo (poliglota) nao sobrevive a regravacao nos tres formatos.

## Como verificar que foi resolvido

Gerar no teste um arquivo com marcadores unicos em cada metadado e conferir que os **bytes** do arquivo gravado nao contem nenhum marcador (`getexif()` vazio nao basta). Cuidado com o ICC do PNG, que vai comprimido: [[Teste de upload com Pillow - CRC do PNG nao e conferido e o ICC do PNG vai comprimido]].

## O que nao funcionou

Confiar em `save()` sem argumentos como sinonimo de "sem metadados".

## Links confiaveis

- [Pillow: Image (docs no GitHub)](https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst): `open`, `save` e `info`.
- [CWE-212 (MITRE)](https://cwe.mitre.org/data/definitions/212.html): remocao incompleta de informacao sensivel antes de transferir.

## Relacionadas

- [[CWE-212 metadado sensivel em imagem se evita regravando os pixels sem EXIF, GPS e comentarios]]: o padrao geral que esta nota detalha.
- [[Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto]]: limite de dimensao antes de decodificar.
- [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]
- [[Regravar imagem sem EXIF exige aplicar a orientacao antes]]: candidato original da T-0006 (arquivado; seu item de orientacao foi confirmado aqui).

## Origem

Experimento da Seguranca na T-0012 (detalhes em `projetos/lab/docs/seguranca/T-0012-ameacas.md`, E1, E2, E3, E7).

## Decisao do Bibliotecario

Promovido (2026-10-01) como problema-solucao ativo. O item 1 (orientacao) funde o candidato da T-0006, que ficara pendente de teste; o experimento da Seguranca o confirmou.
