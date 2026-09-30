---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: pauta
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, owasp.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (publicado em 2025-12-15); OWASP Top 10:2025
criado: 2026-09-30
decisao:
tags: [seguranca, cwe, mapa, indice]
---
# Mapa das CWE relevantes para Python e FastAPI

## Conteudo proposto

Indice para o Bibliotecario virar mapa em `20_Mapas`. Filtro: CWE Top 25 de 2025 aplicavel a FastAPI + Starlette + Jinja2 + SQLAlchemy + PostgreSQL em Docker, mais casos do lab.

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

### Fica para pesquisas futuras

- CWE-284 Improper Access Control (#19): categoria ampla, coberta por 862/863/639.
- CWE-863 Incorrect Authorization (#17) e CWE-306 (#21): citadas na nota de CWE-862; podem ganhar nota propria.
- CWE de memoria em C/C++ (787, 416, 125, 120, 121, 122, 476): baixa relevancia em Python puro; relevantes para extensoes nativas (ex.: Pillow, drivers) e se resolvem atualizando dependencias (ver [[osv-scanner sobre requirements.txt acusa versao antiga de dependencia indireta]]).
- Fora do Top 25 mas relevantes: cookies/sessao (CWE-614, 1004, 384), armazenamento de senha (CWE-916, 256), segredos no codigo (CWE-798), redirecionamento aberto (CWE-601), XXE (CWE-611), cabecalhos de seguranca/CORS (CWE-942).

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
