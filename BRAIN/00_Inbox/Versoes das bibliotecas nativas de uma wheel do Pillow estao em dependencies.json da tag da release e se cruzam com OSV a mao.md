---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/pesquisador
tarefa: T-0012
pesquisa: SEARCH-0003
confianca: media
fontes: ["https://github.com/python-pillow/Pillow/blob/main/.github/dependencies.json", "https://github.com/python-pillow/Pillow/blob/main/.github/workflows/wheels-dependencies.sh", "https://google.github.io/osv-scanner/supported-languages-and-lockfiles/", "https://github.com/python-pillow/pillow-wheels"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.x (arquivo lido na branch main; conferir na tag da versao instalada); osv-scanner 2.x"
criado: 2026-10-01
decisao:
tags: [seguranca, dependencias, pillow, osv-scanner, cwe-1395]
---
# Versoes das bibliotecas nativas de uma wheel do Pillow estao em dependencies.json da tag da release e se cruzam com OSV a mao

## Conteudo proposto

Para saber quais bibliotecas C uma wheel do Pillow embute e se tem CVE:

1. Versao instalada: `PIL.features.version("libjpeg")` (e `zlib`, `libtiff`, `webp`, `freetype2`, `littlecms2`...), confere o que a wheel de fato tem.
2. Versao pretendida pelo projeto: o script de build das wheels Linux/macOS (`.github/workflows/wheels-dependencies.sh`) le as versoes de `.github/dependencies.json` do repositorio do Pillow. Abra esse arquivo **na tag da versao instalada** (ex.: `.../blob/12.3.0/.github/dependencies.json`), nao na `main`: em 2026-10-01 a `main` tinha libjpeg-turbo 3.2.0, libtiff 4.7.2 e harfbuzz 14.4.0, enquanto a tag 12.3.0 tem 3.1.4.1, 4.7.1 e 14.2.1. Lista: brotli, bzip2, freetype, fribidi, harfbuzz, libjpeg-turbo, lcms2, libavif, libimagequant, libpng, libwebp, libxcb, openjpeg, libtiff, xz, zlib-ng, zstd. O repositorio `pillow-wheels` foi arquivado em 2024-10-08 e migrou para o repo principal.
3. CVE: a API do OSV (`POST https://api.osv.dev/v1/query`, ou `/v1/querybatch`) aceita pacote + versao; para bibliotecas C o ecossistema e `OSS-Fuzz` (exemplo da propria documentacao: `{"package":{"name":"libwebp","ecosystem":"OSS-Fuzz"},"version":"1.2.3"}`). Nao verifiquei a cobertura de cada biblioteca; confira tambem os avisos dos projetos de origem. Nao ha automacao oficial conhecida.

Limite: a documentacao do osv-scanner lista para imagens so gerenciadores de pacote (apk, dpkg), binarios Go/Rust, uber JARs, node modules e wheels Python; extracao de C/C++ vale so para codigo-fonte (conan.lock, submodulos, dependencias vendorizadas). Nao ha extrator de `.so` nem de `<pacote>.libs/`. Isso confirma, pela documentacao, o ponto cego medido na T-0012.

## Evidencia

Leitura de `wheels-dependencies.sh` (usa `_get_ver` sobre `dependencies.json`) e da pagina de artefatos suportados do osv-scanner em 2026-10-01. A pagina de politica de seguranca do Pillow manda manter Pillow e bibliotecas embutidas atualizadas. Conferido contra a wheel real da T-0012 (SEC-T0012-02, `pillow-12.3.0-cp313-manylinux`): libjpeg-turbo 3.1.4.1, libwebp 1.6.0, libpng16 1.6.58 e lcms2 2.19 batem com o `dependencies.json` da tag 12.3.0 (e nao com o da `main`). Conferencia feita por comparacao de documentos; nao rodei `features.version` nesta maquina (venv indisponivel).

## Links confiaveis

- [dependencies.json do Pillow](https://github.com/python-pillow/Pillow/blob/main/.github/dependencies.json): versoes das bibliotecas que entram nas wheels (trocar `main` pela tag).
- [wheels-dependencies.sh](https://github.com/python-pillow/Pillow/blob/main/.github/workflows/wheels-dependencies.sh): prova que as wheels Linux/macOS usam esse arquivo.
- [API do OSV](https://google.github.io/osv.dev/api/): consulta por pacote/versao ou commit, inclusive ecossistema OSS-Fuzz.
- [osv-scanner: artefatos suportados](https://google.github.io/osv-scanner/supported-languages-and-lockfiles/): o que o scanner extrai de imagens e de C/C++.

## Por que e reaproveitavel

Mesmo roteiro serve para outras wheels com bibliotecas vendorizadas (lxml, cryptography...), trocando o repositorio de origem.

## Relacionadas no Brain

- [[osv-scanner de imagem nao ve bibliotecas nativas embutidas em wheels Python]]
- [[CWE-1395 dependencia vulneravel se evita com auditoria do arquivo travado e da camada do sistema da imagem]]

## Decisao do Bibliotecario
