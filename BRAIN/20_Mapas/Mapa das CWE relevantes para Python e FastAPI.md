---
tipo: mapa
status: ativo
origem: SEARCH-0001 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0001
fontes: [cwe.mitre.org, owasp.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (publicado em 2025-12-15); OWASP Top 10:2025
criado: 2026-09-30
tags: [seguranca, cwe, mapa, indice]
---
# Mapa das CWE relevantes para Python e FastAPI

## Visao geral

Porta de entrada da Seguranca e do Revisor para escolher o que checar. Filtro: CWE Top 25 de 2025 aplicavel a FastAPI + Starlette + Jinja2 + SQLAlchemy + PostgreSQL em Docker, mais casos do lab. As notas marcadas `rascunho` (CSRF, XSS, command injection, code injection, deserializacao, SSRF) ainda pedem conferencia em fonte primaria; ver a decisao no fim de cada uma.

## Notas principais

### Catalogadas (uma nota cada)

| CWE | Top 25 2025 | Nota |
|---|---|---|
| CWE-79 XSS | #1 | [[CWE-79 XSS exige autoescape do Jinja2 ligado e nunca usar safe em dado do usuario]] |
| CWE-89 SQL injection | #2 | [[CWE-89 SQL injection se evita com parametros vinculados do SQLAlchemy e nunca com f-string]] |
| CWE-352 CSRF | #3 | [[CWE-352 CSRF exige token ou cookie SameSite em rotas que mudam estado com cookie de sessao]] |
| CWE-862 (+863, 306) autorizacao | #4 (#17, #21) | [[CWE-862 autorizacao ausente se evita checando permissao em cada rota com Depends]] |
| CWE-22 path traversal | #6 | [[CWE-22 path traversal se evita resolvendo o caminho e conferindo que fica dentro da pasta base]] |
| CWE-78 (+77) command injection | #9 (#23) | [[CWE-78 command injection se evita com subprocess em lista e sem shell]] |
| CWE-94 code injection | #10 | [[CWE-94 code injection se evita sem eval, exec e templates montados com entrada do usuario]] |
| CWE-434 upload | #12 | [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]] |
| CWE-502 deserializacao | #15 | [[CWE-502 deserializacao de dado nao confiavel se evita com JSON em vez de pickle]] |
| CWE-20 validacao de entrada | #18 | [[CWE-20 entrada extrema gerando erro 500 se evita validando com Pydantic e handler global]] |
| CWE-200 (+209) vazamento | #20 | [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]] |
| CWE-918 SSRF | #22 | [[CWE-918 SSRF se evita com allowlist de destinos e bloqueio de enderecos internos]] |
| CWE-639 IDOR | #24 | [[CWE-639 IDOR se evita filtrando a consulta pelo dono do objeto]] |
| CWE-770 recursos sem limite | #25 | [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]] |

### Dependencias, imagem e hardening (SEARCH-0002 e SEARCH-0003, fora do Top 25)

| CWE | Nota |
|---|---|
| CWE-1395 dependencia vulneravel | [[CWE-1395 dependencia vulneravel se evita com auditoria do arquivo travado e da camada do sistema da imagem]]; caso pratico: [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]] |
| CWE-829 origem nao confiavel (sem versao/hash) | [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]] |
| CWE-250 container como root | [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]] |
| CWE-1021 clickjacking (rascunho) | [[CWE-1021 clickjacking se evita com CSP frame-ancestors e X-Frame-Options em middleware do Starlette]] |
| CWE-250 reforco (setuid e capabilities) | [[USER sem privilegio nao basta - no-new-privileges e cap_drop ALL fecham a escalada por setuid]]; volume antigo: [[Volume antigo com dono root exige chown unico ao trocar o container para usuario sem privilegio]] |
| CWE-409 bomba de descompressao | [[CWE-409 bomba de descompressao se evita com limite de pixels do Pillow tratado como erro e limite de bytes no upload]]; excecoes: [[Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500]] |
| CWE-212 metadado sensivel em imagem | [[CWE-212 metadado sensivel em imagem se evita regravando os pixels sem EXIF, GPS e comentarios]]; detalhes: [[Pillow save padrao mantem o comentario do JPEG e o ICC do PNG ao regravar sem metadados]]; testes: [[Teste de upload com Pillow - CRC do PNG nao e conferido e o ICC do PNG vai comprimido]] |
| Bibliotecas nativas de wheels (ponto cego do scanner) | [[osv-scanner de imagem nao ve bibliotecas nativas embutidas em wheels Python]]; roteiro: [[Versoes das bibliotecas nativas de uma wheel do Pillow estao em dependencies.json da tag da release e se cruzam com OSV a mao]] |

Automacao no lab: [[ruff e pip-audit em Docker Compose com servicos lint e audit no estagio dev]].

## Perguntas em aberto

### Fica para pesquisas futuras

- CWE-284 Improper Access Control (#19): categoria ampla, coberta por 862/863/639.
- CWE-863 Incorrect Authorization (#17) e CWE-306 (#21): citadas na nota de CWE-862; podem ganhar nota propria.
- CWE de memoria em C/C++ (787, 416, 125, 120, 121, 122, 476): baixa relevancia em Python puro; relevantes para extensoes nativas (ex.: Pillow, drivers) e se resolvem atualizando dependencias (ver [[osv-scanner sobre requirements.txt acusa versao antiga de dependencia indireta]]).
- Fora do Top 25 mas relevantes: cookies/sessao (CWE-614, 1004, 384), armazenamento de senha (CWE-916, 256), segredos no codigo (CWE-798), redirecionamento aberto (CWE-601), XXE (CWE-611), CORS (CWE-942).
- Varredura da imagem (`osv-scanner scan image`) e `uv pip compile --generate-hashes`: sem fonte primaria confirmada (SEARCH-0002).

## Evidencia

Lista completa conferida na pagina oficial do CWE Top 25 2025 (MITRE) e categorias do OWASP Top 10:2025 (A01 Broken Access Control ... A10 Mishandling of Exceptional Conditions) em 2026-09-30.

## Links confiaveis

- [CWE Top 25 2025 (MITRE)](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html): ranking oficial.
- [OWASP Top 10:2025](https://top10.owasp.org/2025): categorias vigentes (dominio novo, ver SEARCH-0001).
- [Indice de cheat sheets por Top 10 (OWASP)](https://cheatsheetseries.owasp.org/IndexTopTen.html): cheat sheets por categoria (mapeado ao Top 10 2021; conferir nomes ao usar).

## Por que e reaproveitavel

Porta de entrada da Seguranca e do Revisor para escolher o que checar.

## Relacionadas no Brain

- [[Fontes de referencia para analise de seguranca por CWE e dependencias]]

## Decisao do Bibliotecario

Promovido a mapa em `20_Mapas` (2026-09-30). Sem mapa anterior sobre o tema. Notas filhas: ver a tabela acima.
