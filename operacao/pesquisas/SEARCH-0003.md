---
tipo: pesquisa
id: SEARCH-0003
status: nao-pesquisada
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0012
criado: 2026-10-01
pesquisado_por:
pesquisado_em:
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

- **Resumo (3 a 5 linhas):**
- **Notas geradas no Inbox:** [[ ]]
- **Links confiaveis:**
- **Sem resposta / limites:**
- **Conteudo suspeito descartado:**

## Dominios propostos

- 

## Catalogacao
