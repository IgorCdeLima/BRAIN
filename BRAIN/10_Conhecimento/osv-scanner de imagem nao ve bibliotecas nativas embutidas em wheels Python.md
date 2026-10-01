---
tipo: aprendizado
status: ativo
origem: T-0012 (Seguranca) e SEARCH-0003 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0012
pesquisa: SEARCH-0003
confianca: media
fontes: ["experimento da Seguranca em 2026-10-01 (osv-scanner 2.6.0, python:3.13.15-slim + pillow 12.3.0); projetos/lab qualidade/seguranca/SEC-T0012-02.md", "https://google.github.io/osv-scanner/supported-languages-and-lockfiles/", "https://pillow.readthedocs.io/en/stable/reference/features.html", "https://github.com/python-pillow/Pillow/security/policy"]
verificado_em: 2026-10-01
valido_para: "osv-scanner 2.6.0; wheels manylinux com bibliotecas vendorizadas (auditwheel), ex.: Pillow 12.3.0"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [seguranca, dependencias, varredura, osv-scanner, pip-audit, pillow, cwe-1395]
---
# osv-scanner de imagem nao ve bibliotecas nativas embutidas em wheels Python

## O que aconteceu

Wheels manylinux trazem bibliotecas C proprias em `site-packages/<pacote>.libs/` (o Pillow 12.3.0 traz 18: libwebp, libjpeg-turbo, libpng16, lcms2, libtiff, openjpeg, freetype, harfbuzz, libavif...). Na T-0012, `docker commit` de `python:3.13.15-slim` + `pip install pillow==12.3.0` e `osv-scanner scan image --all-packages --format json` viram 90 pacotes: `pillow` (PyPI), `zlib` e `libzstd` (Debian), e **nenhum** dos 18 `.so` de `pillow.libs/` (SEC-T0012-02 do lab).

## O que aprendemos

Essas bibliotecas nao sao pacotes Debian nem PyPI, por isso:

- o `pip-audit` so ve o pacote Python (`pillow`) e os avisos publicados para ele;
- o `osv-scanner scan image --all-packages` (2.6.0) nao lista nada de `<pacote>.libs/`; a documentacao confirma que imagens nao tem extrator de `.so`/`.libs`.

"Varredura limpa" nao cobre o codigo que de fato decodifica o dado nao confiavel. Vale para toda dependencia Python com extensao C e bibliotecas vendorizadas (Pillow, lxml, cryptography, numpy...).

## O que muda a partir de agora

- Registrar as versoes embutidas (`PIL.features.version(...)`) e acompanhar as notas de versao do pacote e os avisos das bibliotecas de origem.
- Atualizar o pacote quando sair wheel com biblioteca corrigida, mesmo sem aviso no `pip-audit`.
- Roteiro passo a passo: [[Versoes das bibliotecas nativas de uma wheel do Pillow estao em dependencies.json da tag da release e se cruzam com OSV a mao]].

## Links confiaveis

- [osv-scanner: artefatos suportados](https://google.github.io/osv-scanner/supported-languages-and-lockfiles/)
- [OSV.dev](https://osv.dev/): base que o `osv-scanner` consulta.
- [Pillow PIL.features](https://pillow.readthedocs.io/en/stable/reference/features.html): `features.version("libjpeg")` etc.
- [Politica de seguranca do Pillow](https://github.com/python-pillow/Pillow/security/policy): manter Pillow e bibliotecas C embutidas atualizados; avisos no GitHub Security.

## Relacionadas

- [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]]: o mesmo ponto cego, uma camada abaixo.
- [[CWE-1395 dependencia vulneravel se evita com auditoria do arquivo travado e da camada do sistema da imagem]]
- [[osv-scanner sobre requirements.txt acusa versao antiga de dependencia indireta]]

## Origem

T-0012 (SEC-T0012-02 do lab) e SEARCH-0003.

## Decisao do Bibliotecario

Promovido (2026-10-01) como aprendizado ativo. Medicao propria, confirmada pela documentacao do osv-scanner; confianca media por ser uma versao de ferramenta (2.6.0) e uma wheel.
