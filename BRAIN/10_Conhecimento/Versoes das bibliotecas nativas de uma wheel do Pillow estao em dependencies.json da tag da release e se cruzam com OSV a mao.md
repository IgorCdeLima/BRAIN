---
tipo: problema-solucao
status: ativo
origem: SEARCH-0003 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0012
pesquisa: SEARCH-0003
confianca: media
fontes: ["https://github.com/python-pillow/Pillow/blob/main/.github/dependencies.json", "https://github.com/python-pillow/Pillow/blob/main/.github/workflows/wheels-dependencies.sh", "https://google.github.io/osv-scanner/supported-languages-and-lockfiles/", "https://google.github.io/osv.dev/api/", "https://github.com/python-pillow/pillow-wheels"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.x (arquivo lido na branch main; conferir na tag da versao instalada); osv-scanner 2.x"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [seguranca, dependencias, pillow, osv-scanner, cwe-1395]
---
# Versoes das bibliotecas nativas de uma wheel do Pillow estao em dependencies.json da tag da release e se cruzam com OSV a mao

## Sintoma

Precisa-se saber quais bibliotecas C uma wheel do Pillow embute e se alguma tem CVE, mas nem o `pip-audit` nem o `osv-scanner scan image` listam essas bibliotecas ([[osv-scanner de imagem nao ve bibliotecas nativas embutidas em wheels Python]]).

## Ambiente

Pillow 12.x (wheel manylinux/macOS), osv-scanner 2.x.

## Causa raiz

As bibliotecas vao vendorizadas (auditwheel) em `pillow.libs/`, fora dos gerenciadores de pacote. A documentacao do osv-scanner lista para imagens so gerenciadores de pacote (apk, dpkg), binarios Go/Rust, uber JARs, node modules e wheels Python; C/C++ so em codigo-fonte. Nao ha extrator de `.so` nem de `<pacote>.libs/`.

## Solucao

Roteiro manual:

1. **Versao instalada:** `PIL.features.version("libjpeg")` (e `zlib`, `libtiff`, `webp`, `freetype2`, `littlecms2`...) confere o que a wheel de fato tem.
2. **Versao pretendida pelo projeto:** o script `.github/workflows/wheels-dependencies.sh` le as versoes de `.github/dependencies.json` do repositorio do Pillow. Abra o arquivo **na tag da versao instalada** (ex.: `.../blob/12.3.0/.github/dependencies.json`), nao na `main`: em 2026-10-01 a `main` tinha libjpeg-turbo 3.2.0, libtiff 4.7.2 e harfbuzz 14.4.0, enquanto a tag 12.3.0 tem 3.1.4.1, 4.7.1 e 14.2.1. Lista: brotli, bzip2, freetype, fribidi, harfbuzz, libjpeg-turbo, lcms2, libavif, libimagequant, libpng, libwebp, libxcb, openjpeg, libtiff, xz, zlib-ng, zstd. O repositorio `pillow-wheels` foi arquivado em 2024-10-08 e migrou para o repo principal.
3. **CVE:** a API do OSV (`POST https://api.osv.dev/v1/query`, ou `/v1/querybatch`) aceita pacote + versao; para bibliotecas C o ecossistema e `OSS-Fuzz` (exemplo da documentacao: `{"package":{"name":"libwebp","ecosystem":"OSS-Fuzz"},"version":"1.2.3"}`). A cobertura de cada biblioteca nao foi verificada; conferir tambem os avisos dos projetos de origem. Nao ha automacao oficial conhecida.

## Como verificar que foi resolvido

Comparar `features.version()` da wheel instalada com o `dependencies.json` da tag. Ja conferido por comparacao de documentos contra a wheel real da T-0012 (`pillow-12.3.0-cp313-manylinux`, SEC-T0012-02): libjpeg-turbo 3.1.4.1, libwebp 1.6.0, libpng16 1.6.58 e lcms2 2.19 batem com a tag 12.3.0 e nao com a `main`. **Limite:** `features.version` ainda nao foi rodado numa wheel instalada (pedido COORD-0014 pendente); por isso confianca media.

## O que nao funcionou

Ler o `dependencies.json` da `main` (versoes diferentes da wheel instalada); esperar que o osv-scanner de imagem detecte as bibliotecas.

## Links confiaveis

- [dependencies.json do Pillow](https://github.com/python-pillow/Pillow/blob/main/.github/dependencies.json): trocar `main` pela tag.
- [wheels-dependencies.sh](https://github.com/python-pillow/Pillow/blob/main/.github/workflows/wheels-dependencies.sh): mostra que as wheels Linux/macOS usam esse arquivo.
- [API do OSV](https://google.github.io/osv.dev/api/): consulta por pacote/versao ou commit, inclusive OSS-Fuzz.
- [osv-scanner: artefatos suportados](https://google.github.io/osv-scanner/supported-languages-and-lockfiles/): o que o scanner extrai de imagens e de C/C++.

## Relacionadas

- [[osv-scanner de imagem nao ve bibliotecas nativas embutidas em wheels Python]]: o ponto cego que este roteiro contorna.
- [[CWE-1395 dependencia vulneravel se evita com auditoria do arquivo travado e da camada do sistema da imagem]]: o controle geral.

## Origem

SEARCH-0003 (pedido da Seguranca na T-0012). O mesmo roteiro serve para outras wheels com bibliotecas vendorizadas (lxml, cryptography...), trocando o repositorio de origem.

## Decisao do Bibliotecario

Promovido (2026-10-01) como problema-solucao ativo, confianca media: fontes oficiais lidas, mas a conferencia por `features.version()` esta pendente (COORD-0014). Reavaliar a confianca quando o pedido for atendido.
