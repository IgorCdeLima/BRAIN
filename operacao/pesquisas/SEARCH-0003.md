---
tipo: pesquisa
id: SEARCH-0003
status: respondida
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0012
criado: 2026-10-01
pesquisado_por: pesquisador
pesquisado_em: 2026-10-01
catalogado_em:
notas: []
tags: [seguranca, dependencias, pillow, imagem, cwe, cwe-409, cwe-212]
---
# SEARCH-0003 - Como acompanhar CVE das bibliotecas nativas embutidas em wheels (Pillow) e notas de CWE-409 e CWE-212

## Pergunta

1. Que fonte confiavel (e, se houver, que ferramenta) diz quais versoes de libwebp, libjpeg-turbo, libpng, lcms2, libtiff e openjpeg vem embutidas em cada wheel do Pillow e se alguma delas tem CVE conhecida? O `osv-scanner` tem algum modo que detecte bibliotecas em `site-packages/<pacote>.libs/` (auditwheel)?
2. Para as CWE-409 (bomba de descompressao / dados muito comprimidos) e CWE-212 (remocao incompleta de dados sensiveis antes de transferir, ex.: EXIF/GPS): qual e o controle recomendado na nossa stack (Python 3.13, Pillow 12.x) e como testa-lo?

## Contexto

- A T-0012 (analise de ameacas da T-0010 do lab) mediu que `osv-scanner scan image --all-packages` (2.6.0) ve `pillow 12.3.0` (PyPI) e os pacotes Debian, mas nenhuma das 18 bibliotecas de `pillow.libs/` (SEC-T0012-02 do lab). O `pip-audit` so ve avisos publicados para o proprio Pillow.
- A T-0010 vai decodificar uploads com o Pillow; as bibliotecas que decodificam sao justamente as embutidas.
- Formato esperado: notas no padrao "CWE-### ... se evita com ...", com "como testar" e links confiaveis (MITRE CWE, OWASP, notas de versao do Pillow no GitHub, OSV).

## Ja buscado no Brain

- Tag `seguranca`, `pillow`, `CWE-409`, `CWE-212`, `decompression`: ha [[Pillow Image.open ja recusa imagem acima do dobro de MAX_IMAGE_PIXELS antes da checagem de dimensao do projeto]] (comportamento do Pillow, sem a CWE) e [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]] (limites em geral). Nenhuma nota de CWE-409 nem de CWE-212.
- [[CWE-1395 dependencia vulneravel se evita com auditoria do arquivo travado e da camada do sistema da imagem]] e [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]] cobrem PyPI e Debian, nao bibliotecas vendorizadas em wheels.
- [[Fontes de referencia para analise de seguranca por CWE e dependencias]]: nenhuma fonte da lista cobre o item 1.

---

## Resposta

- **Resumo (3 a 5 linhas):** Item 1 (refeito): a documentacao do osv-scanner confirma que ele nao extrai `.so` nem `<pacote>.libs/` em imagens (C/C++ so em codigo-fonte). As versoes embutidas nas wheels Linux/macOS vem de `.github/dependencies.json` do repo do Pillow (na tag da release), lido por `wheels-dependencies.sh`; `PIL.features.version()` confere a instalada. CVE por biblioteca: cruzar a mao com OSV.dev. Item 2: CWE-409 e CWE-212 em notas proprias.
- **Notas geradas no Inbox:** [[Versoes das bibliotecas nativas de uma wheel do Pillow estao em dependencies.json da tag da release e se cruzam com OSV a mao]], [[CWE-409 bomba de descompressao se evita com limite de pixels do Pillow tratado como erro e limite de bytes no upload]], [[CWE-212 metadado sensivel em imagem se evita regravando os pixels sem EXIF, GPS e comentarios]]; links acrescentados em [[osv-scanner de imagem nao ve bibliotecas nativas embutidas em wheels Python]].
- **Links confiaveis:** https://github.com/python-pillow/Pillow/blob/main/.github/dependencies.json ; https://github.com/python-pillow/Pillow/blob/main/.github/workflows/wheels-dependencies.sh ; https://google.github.io/osv-scanner/supported-languages-and-lockfiles/ ; https://google.github.io/osv.dev/api/ ; https://pillow.readthedocs.io/en/stable/reference/features.html ; https://github.com/python-pillow/Pillow/security/policy ; https://cwe.mitre.org/data/definitions/409.html ; https://cwe.mitre.org/data/definitions/212.html
- **Sem resposta / limites:** nao existe ferramenta oficial que cruze as bibliotecas embutidas com CVE; o roteiro e manual. Confirmado em 2026-10-01: o `dependencies.json` da tag 12.3.0 bate com as versoes medidas na wheel real (SEC-T0012-02: libjpeg-turbo 3.1.4.1, libwebp 1.6.0, libpng 1.6.58, lcms2 2.19) e difere da `main`, entao a tag e obrigatoria. Nao rodei `PIL.features.version()` aqui (venv indisponivel; comparei com o registro da T-0012). Nao verifiquei a cobertura do ecossistema OSS-Fuzz do OSV para cada biblioteca. OWASP (Unrestricted File Upload) foi lido: cobre limite de tamanho e armazenamento seguro, mas nao cita remocao de metadados nem bomba de descompressao, entao nao serve de fonte para as CWE-212/409. Agregadores da busca extended foram descartados.
- **Conteudo suspeito descartado:** nenhum.

## Dominios propostos

- 

## Catalogacao
