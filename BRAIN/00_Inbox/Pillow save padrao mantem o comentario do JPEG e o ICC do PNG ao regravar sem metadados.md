---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/seguranca
tarefa: T-0012
pesquisa:
confianca: alta
fontes: ["experimento da Seguranca em 2026-10-01 (python:3.13.15-slim, pillow 12.3.0), registrado em projetos/lab docs/seguranca/T-0012-ameacas.md (E1, E2, E7)"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.3.0; regravacao de upload de imagem JPEG/PNG/WebP"
criado: 2026-10-01
decisao:
tags: [seguranca, upload, imagem, pillow, metadados, privacidade, armadilha, cwe-212]
---
# Pillow save padrao mantem o comentario do JPEG e o ICC do PNG ao regravar sem metadados

## Conteudo proposto

Ao regravar um upload com `Image.open(...)`, `load()`, `ImageOps.exif_transpose(im)` e `im.save(buf, formato)` **sem argumentos**, o resultado nao e "sem metadados" por completo:

| Metadado | JPEG | PNG | WebP |
|---|---|---|---|
| EXIF (inclusive GPS) | some | some | some |
| XMP | some | some | some |
| Texto (tEXt/iTXt) | - | some | - |
| Comentario COM | **sobrevive** | - | - |
| Perfil ICC | some | **sobrevive** (ate ICC invalido) | some |

Consequencias:

1. Para tirar o comentario do JPEG, passar `comment=b""` no `save` ou retirar `comment` de `im.info` (ambos testados).
2. O ICC se comporta diferente em cada formato: decidir a regra e aplica-la explicitamente nos tres. Repassado como veio (`icc_profile=im.info["icc_profile"]`), o ICC leva qualquer byte anexado ao arquivo final (testado com `<script>` + 200 KB). `ImageCms.ImageCmsProfile(io.BytesIO(icc)).tobytes()` reserializa so o perfil e descarta o anexo.
3. JPEG com segmento MPF (varias imagens) abre como `format == "MPO"` mesmo com `formats=["JPEG"]`; comparar com `"JPEG"` recusa o arquivo. Salvo como `"JPEG"`, sai 1 quadro.
4. `exif_transpose` aplica a orientacao (40x20 com Orientation=6 -> 20x40) e o EXIF nao volta no `save` sem argumentos.
5. Conteudo anexado depois do fim do arquivo (poliglota) nao sobrevive a regravacao nos tres formatos.

Como testar: gerar no teste um arquivo com marcadores unicos em cada metadado e conferir que os **bytes** do arquivo gravado nao contem nenhum marcador (nao basta `getexif()` vazio).

## Evidencia

Experimento da Seguranca em 2026-10-01, `docker run python:3.13.15-slim` com `pip install pillow==12.3.0`, arquivos gerados pelo proprio Pillow com EXIF, XMP, ICC, COM e tEXt/iTXt. Detalhes e numeros em `projetos/lab/docs/seguranca/T-0012-ameacas.md` (E1, E2, E3, E7). Nao testado com fotos reais de celular.

## Links confiaveis

- [Pillow: Image (docs no GitHub)](https://github.com/python-pillow/Pillow/blob/main/docs/reference/Image.rst): `open`, `save` e `info`.
- [CWE-212 (MITRE)](https://cwe.mitre.org/data/definitions/212.html): remocao incompleta de informacao sensivel antes de transferir.

## Por que e reaproveitavel

Todo projeto que regrava imagem enviada para tirar metadados (privacidade) ou para neutralizar poliglota.

## Relacionadas no Brain

- [[Regravar imagem sem EXIF exige aplicar a orientacao antes]]: o item 1 dela (orientacao com `exif_transpose`) foi confirmado aqui.
- [[Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto]]
- [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]

## Decisao do Bibliotecario
