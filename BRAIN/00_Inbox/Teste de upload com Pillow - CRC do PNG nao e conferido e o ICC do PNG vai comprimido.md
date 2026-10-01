---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/revisor
tarefa: T-0012
pesquisa:
confianca: alta
fontes: ["experimento do Revisor em 2026-10-01 (python:3.13.15-slim, pillow 12.3.0), registrado em projetos/lab qualidade/bugs/BUG-T0012-01.md e BUG-T0012-02.md"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.3.0; testes de validacao de upload de imagem"
criado: 2026-10-01
decisao:
tags: [seguranca, upload, imagem, pillow, testes, armadilha, png, icc]
---
# Teste de upload com Pillow - CRC do PNG nao e conferido e o ICC do PNG vai comprimido

## Conteudo proposto

Tres premissas comuns ao escrever testes de validacao de imagem com Pillow que **nao valem** (Pillow 12.3.0):

1. **"PNG com CRC quebrado da erro."** Nao no IDAT: o Pillow ignora o CRC e decodifica a imagem. CRC quebrado no IHDR da `UnidentifiedImageError` (subclasse de `OSError`). Para provocar `SyntaxError` ("broken PNG file") de forma deterministica, alterar o **tamanho** de um chunk (ex.: tamanho do IDAT = 0).
2. **"Procurar a string nos bytes do arquivo prova que o metadado sumiu."** Nao para o ICC no PNG: o chunk `iCCP` e comprimido com zlib, entao `b"<script>" in arquivo` da `False` mesmo com o perfil intacto. Conferir o perfil lido de volta (`Image.open(f).info["icc_profile"]`). O mesmo vale para `zTXt` e `iTXt` comprimido. No JPEG e no WebP o ICC fica literal.
3. **"As excecoes do Pillow sao `OSError`, `SyntaxError` e `DecompressionBombError`."** Tambem aparece `ValueError` ("Truncated IHDR chunk", `PngImagePlugin.chunk_IHDR`) com um byte trocado no cabecalho. Complementa [[Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500]].

**Regra pratica:** receita de caso de teste proposta em criterio de aceite tem de ser executada antes de ir para o cartao; o resultado esperado (classe da excecao, presenca do dado) e conferido na versao da biblioteca.

## Evidencia

Reproducoes completas em `projetos/lab qualidade/bugs/BUG-T0012-01.md` (ICC no PNG) e `BUG-T0012-02.md` (CRC, `SyntaxError`, `ValueError`), 2026-10-01.

## Links confiaveis

Dominios da lista de fontes confiaveis, mas as paginas **nao foram abertas** nesta revisao (a evidencia e o experimento); conferir antes de curar.

- [PNG Specification (W3C)](https://www.w3.org/TR/png-3/): chunks `iCCP` e `zTXt` comprimidos; CRC por chunk.
- [Pillow PngImagePlugin (GitHub)](https://github.com/python-pillow/Pillow/blob/main/src/PIL/PngImagePlugin.py)

## Por que e reaproveitavel

Qualquer teste de upload que valide formato ou remocao de metadados com Pillow; o principio (testar o teste antes de propor) vale para outros parsers.

## Relacionadas no Brain

- [[Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500]]
- [[Pillow save padrao mantem o comentario do JPEG e o ICC do PNG ao regravar sem metadados]]

## Decisao do Bibliotecario
