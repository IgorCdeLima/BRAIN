---
tipo: candidato
status: inbox
tipo_proposto: aprendizado
origem: agente/seguranca
tarefa: T-0012
pesquisa: SEARCH-0003
confianca: media
fontes: ["experimento da Seguranca em 2026-10-01 (osv-scanner 2.6.0, python:3.13.15-slim + pillow 12.3.0); projetos/lab qualidade/seguranca/SEC-T0012-02.md"]
verificado_em: 2026-10-01
valido_para: "osv-scanner 2.6.0; wheels manylinux com bibliotecas vendorizadas (auditwheel), ex.: Pillow 12.3.0"
criado: 2026-10-01
decisao:
tags: [seguranca, dependencias, varredura, osv-scanner, pip-audit, pillow, cwe-1395]
---
# osv-scanner de imagem nao ve bibliotecas nativas embutidas em wheels Python

## Conteudo proposto

Wheels manylinux trazem bibliotecas C proprias em `site-packages/<pacote>.libs/` (o Pillow 12.3.0 traz 18: libwebp, libjpeg-turbo, libpng16, lcms2, libtiff, openjpeg, freetype, harfbuzz, libavif...). Essas bibliotecas nao sao pacotes Debian nem PyPI, e por isso:

- o `pip-audit` so ve o pacote Python (`pillow`) e os avisos publicados para ele;
- o `osv-scanner scan image --all-packages` (2.6.0) lista o pacote Python e os pacotes do sistema, mas **nenhuma** biblioteca de `<pacote>.libs/`.

"Varredura limpa" nao cobre o codigo que de fato decodifica o dado nao confiavel. Controle: registrar as versoes (`PIL.features.version(...)`) e acompanhar as notas de versao do pacote e os avisos das bibliotecas de origem; atualizar o pacote quando sair wheel com biblioteca corrigida, mesmo sem aviso no `pip-audit`.

## Evidencia

Experimento de 2026-10-01: imagem `python:3.13.15-slim` + `pip install pillow==12.3.0`, `docker commit` e `osv-scanner scan image --all-packages --format json`: 90 pacotes vistos; relacionados: `pillow` (PyPI), `zlib` e `libzstd` (Debian). Nenhum dos 18 `.so` de `pillow.libs/`. Ver SEC-T0012-02 do lab. Fonte que resolva o acompanhamento: pedida no SEARCH-0003.

## Links confiaveis

- [OSV.dev](https://osv.dev/): base que o `osv-scanner` consulta.
- [Pillow PIL.features](https://pillow.readthedocs.io/en/stable/reference/features.html): `features.version("libjpeg")`, `"zlib"`, `"libtiff"`, `"webp"`, etc. informam a versao embutida na wheel instalada.
- [Politica de seguranca do Pillow](https://github.com/python-pillow/Pillow/security/policy): orienta manter o Pillow e suas bibliotecas C embutidas atualizados; avisos do proprio Pillow aparecem no GitHub Security.

## Por que e reaproveitavel

Vale para toda dependencia Python com extensao C e bibliotecas vendorizadas (Pillow, lxml, cryptography, numpy...), em qualquer projeto que confie no `pip-audit` + `osv-scanner`.

## Relacionadas no Brain

- [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]]: o mesmo ponto cego, uma camada abaixo.
- [[CWE-1395 dependencia vulneravel se evita com auditoria do arquivo travado e da camada do sistema da imagem]]
- [[osv-scanner sobre requirements.txt acusa versao antiga de dependencia indireta]]

## Decisao do Bibliotecario
