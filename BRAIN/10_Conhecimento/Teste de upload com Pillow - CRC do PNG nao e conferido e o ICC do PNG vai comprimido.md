---
tipo: problema-solucao
status: ativo
origem: T-0012 (Revisor), curado pelo Bibliotecario
tarefa: T-0012
confianca: alta
fontes: ["experimento do Revisor em 2026-10-01 (python:3.13.15-slim, pillow 12.3.0), registrado em projetos/lab qualidade/bugs/BUG-T0012-01.md e BUG-T0012-02.md"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.3.0; testes de validacao de upload de imagem"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [seguranca, upload, imagem, pillow, testes, armadilha, png, icc]
---
# Teste de upload com Pillow - CRC do PNG nao e conferido e o ICC do PNG vai comprimido

## Sintoma

Casos de teste de validacao de imagem escritos a partir de premissas comuns passam ou falham pelo motivo errado: o "PNG corrompido" decodifica normalmente, ou a busca de bytes diz que o metadado sumiu quando ele esta intacto.

## Ambiente

Pillow 12.3.0, Python 3.13.15, testes de upload de PNG/JPEG/WebP.

## Causa raiz

Tres premissas que **nao valem**:

1. **"PNG com CRC quebrado da erro."** No IDAT nao: o Pillow ignora o CRC e decodifica. CRC quebrado no IHDR da `UnidentifiedImageError` (subclasse de `OSError`).
2. **"Procurar a string nos bytes do arquivo prova que o metadado sumiu."** Nao para o ICC no PNG: o chunk `iCCP` e comprimido com zlib, entao `b"<script>" in arquivo` da `False` mesmo com o perfil intacto. O mesmo vale para `zTXt` e `iTXt` comprimidos. No JPEG e no WebP o ICC fica literal.
3. **"As excecoes do Pillow sao `OSError`, `SyntaxError` e `DecompressionBombError`."** Tambem aparece `ValueError` ("Truncated IHDR chunk", `PngImagePlugin.chunk_IHDR`) com um byte trocado no cabecalho.

## Solucao

- Para `SyntaxError` ("broken PNG file") de forma deterministica, alterar o **tamanho** de um chunk (ex.: tamanho do IDAT = 0).
- Para o ICC do PNG, conferir o perfil lido de volta: `Image.open(f).info["icc_profile"]`.
- Tratar tambem `ValueError`: ver [[Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500]].

**Regra pratica:** receita de caso de teste proposta em criterio de aceite tem de ser executada antes de ir para o cartao; o resultado esperado (classe da excecao, presenca do dado) e conferido na versao da biblioteca.

## Como verificar que foi resolvido

Rodar a receita e conferir a classe da excecao e a presenca do dado na versao instalada do Pillow.

## O que nao funcionou

CRC quebrado no IDAT para provocar erro; `b"marcador" in arquivo` para provar ausencia de ICC no PNG.

## Links confiaveis

Os dominios estao na lista de fontes confiaveis, mas as paginas **nao foram abertas** pelo Revisor (a evidencia e o experimento); conferir antes de citar como fonte.

- [PNG Specification (W3C)](https://www.w3.org/TR/png-3/): chunks `iCCP` e `zTXt` comprimidos; CRC por chunk.
- [Pillow PngImagePlugin (GitHub)](https://github.com/python-pillow/Pillow/blob/main/src/PIL/PngImagePlugin.py)

## Relacionadas

- [[Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500]]: complementa a lista de excecoes.
- [[Pillow save padrao mantem o comentario do JPEG e o ICC do PNG ao regravar sem metadados]]: onde a conferencia do ICC se aplica.

## Origem

T-0012, BUG-T0012-01 (ICC no PNG) e BUG-T0012-02 (CRC, `SyntaxError`, `ValueError`) do lab. O principio (testar o teste antes de propor) vale para outros parsers.

## Decisao do Bibliotecario

Promovido (2026-10-01) como problema-solucao ativo; confianca alta pelo experimento reproduzido. Os links sao pistas ainda nao lidas.
