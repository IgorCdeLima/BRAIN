---
tipo: pesquisa
id: SEARCH-0001
status: catalogada
urgencia: nao-bloqueante
pedido_por: humano
tarefa: pauta
criado: 2026-09-30
pesquisado_por: pesquisador
pesquisado_em: 2026-09-30
catalogado_em: 2026-09-30
notas: ["[[Mapa das CWE relevantes para Python e FastAPI]]"]
tags: [seguranca, cwe, pauta]
---
# SEARCH-0001 - Catalogar as CWE mais relevantes para Python/FastAPI

## Pergunta

Quais CWE sao mais relevantes para uma aplicacao web Python (FastAPI + Starlette + Jinja2 + SQLAlchemy + PostgreSQL, rodando em Docker), e para cada uma: o que e, como aparece no nosso tipo de codigo, qual o controle e onde buscar referencia?

## Contexto

- Pauta do humano para o Brain (metodo Zettelkasten): a base de referencia do papel Seguranca.
- Ponto de partida sugerido: CWE Top 25 atual da MITRE e OWASP Top 10, filtrados para a nossa stack. Incluir as que ja apareceram no lab: upload sem limite de corpo (SEC-0001), tipo de arquivo pelo conteudo, traversal em `/uploads`, entrada extrema gerando erro 500.
- **Uma nota por CWE** no Inbox, titulo em forma de afirmacao (ex.: "CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado"), com: explicacao curta, exemplo no estilo FastAPI, controle recomendado, como testar e a secao **Links confiaveis** (MITRE CWE, OWASP Cheat Sheet correspondente).
- Uma nota de mapa (indice) listando as CWE catalogadas, para o Bibliotecario virar mapa em `20_Mapas`.
- Tamanho: comecar pelas 10 a 15 mais relevantes; as demais ficam como lista no mapa para pesquisas futuras.

## Ja buscado no Brain

- [[Fontes de referencia para analise de seguranca por CWE e dependencias]] (no Inbox): diz onde procurar, mas nao explica nenhuma CWE.
- [[Recusa previa por Content-Length esconde a validacao do upload]] e [[Upload de imagem valida tipo por magic bytes e serve por nome gerado]]: casos concretos da T-0003, sem ligacao com CWE.

---

## Resposta

<!-- Preenchido pelo Pesquisador. -->

- **Resumo (3 a 5 linhas):** Base: CWE Top 25 2025 (MITRE, publicado em 2025-12-15) e OWASP Top 10:2025, filtrados para a nossa stack. Foram catalogadas 14 CWE (uma nota cada, com o que e, como aparece em FastAPI/Jinja2/SQLAlchemy/Docker, controle, como testar e links) mais uma nota de mapa. Os casos do lab estao cobertos: upload (434), traversal em uploads (22), corpo sem limite (770) e entrada extrema/erro 500 (20 e 200). As CWE de memoria (C/C++) e as demais ficam listadas no mapa para pesquisas futuras.
- **Notas geradas no Inbox:** [[Mapa das CWE relevantes para Python e FastAPI]], [[CWE-79 XSS exige autoescape do Jinja2 ligado e nunca usar safe em dado do usuario]], [[CWE-89 SQL injection se evita com parametros vinculados do SQLAlchemy e nunca com f-string]], [[CWE-352 CSRF exige token ou cookie SameSite em rotas que mudam estado com cookie de sessao]], [[CWE-862 autorizacao ausente se evita checando permissao em cada rota com Depends]], [[CWE-639 IDOR se evita filtrando a consulta pelo dono do objeto]], [[CWE-22 path traversal se evita resolvendo o caminho e conferindo que fica dentro da pasta base]], [[CWE-78 command injection se evita com subprocess em lista e sem shell]], [[CWE-94 code injection se evita sem eval, exec e templates montados com entrada do usuario]], [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]], [[CWE-502 deserializacao de dado nao confiavel se evita com JSON em vez de pickle]], [[CWE-20 entrada extrema gerando erro 500 se evita validando com Pydantic e handler global]], [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]], [[CWE-918 SSRF se evita com allowlist de destinos e bloqueio de enderecos internos]], [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]
- **Links confiaveis:** cwe.mitre.org/top25 e /data/definitions/N; top10.owasp.org/2025; cheatsheetseries.owasp.org (File Upload, Input Validation, Denial of Service, IDOR, Error Handling, indice Top 10); docs.sqlalchemy.org, jinja.palletsprojects.com, fastapi.tiangolo.com, docs.python.org.
- **Sem resposta / limites:** (1) O indice de cheat sheets da OWASP ainda mapeia o Top 10 de 2021. (2) Abri o texto completo apenas de File Upload, Input Validation, Denial of Service, IDOR e Error Handling. As notas de command injection, code injection, deserializacao, SSRF e CSRF se apoiam no indice de cheat sheets e no conhecimento geral, sem ler o texto completo: ficam com aviso de "pista". (3) Nao confirmei se o `Jinja2Templates` do Starlette liga o autoescape por padrao: a nota de XSS pede essa conferencia. (4) URLs `cwe.mitre.org/data/definitions/N.html` seguem o padrao oficial, mas nao abri cada uma. (5) SSTI/Jinja2 sem fonte primaria dedicada.
- **Conteudo suspeito descartado:** nenhum.

## Dominios propostos

<!-- Dominios novos para agentes/fontes-confiaveis.json, com o motivo. O humano decide. -->

- `top10.owasp.org`: o OWASP Top 10:2025 passou a viver la (`owasp.org/Top10/2025` redireciona com 308).
- `community.owasp.org`: `owasp.org/www-community/...` (ex.: Path Traversal) redireciona para la.
- `jinja.palletsprojects.com`: documentacao oficial do Jinja2 (autoescape); a stack usa Jinja2 e nao esta na lista.
- `cwe.mitre.org` e `cheatsheetseries.owasp.org` ja estao na lista.

## Catalogacao

<!-- Preenchido pelo Bibliotecario: decisao e notas finais. -->

**Decisao (2026-09-30): promovidos os 15 candidatos.** Links confiaveis preservados em cada nota.

- Mapa: [[Mapa das CWE relevantes para Python e FastAPI]] (`20_Mapas`).
- Padroes ativos (`10_Conhecimento`, fonte primaria lida): [[CWE-20 entrada extrema gerando erro 500 se evita validando com Pydantic e handler global]], [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]], [[CWE-22 path traversal se evita resolvendo o caminho e conferindo que fica dentro da pasta base]], [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]], [[CWE-639 IDOR se evita filtrando a consulta pelo dono do objeto]], [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]], [[CWE-862 autorizacao ausente se evita checando permissao em cada rota com Depends]], [[CWE-89 SQL injection se evita com parametros vinculados do SQLAlchemy e nunca com f-string]].
- Rascunhos (`status: rascunho`, pendentes de conferencia em fonte primaria, conforme os limites do Pesquisador): [[CWE-79 XSS exige autoescape do Jinja2 ligado e nunca usar safe em dado do usuario]] (autoescape do `Jinja2Templates`), [[CWE-352 CSRF exige token ou cookie SameSite em rotas que mudam estado com cookie de sessao]], [[CWE-78 command injection se evita com subprocess em lista e sem shell]], [[CWE-94 code injection se evita sem eval, exec e templates montados com entrada do usuario]], [[CWE-502 deserializacao de dado nao confiavel se evita com JSON em vez de pickle]], [[CWE-918 SSRF se evita com allowlist de destinos e bloqueio de enderecos internos]].
- Dominios propostos (`top10.owasp.org`, `community.owasp.org`, `jinja.palletsprojects.com`): decisao do humano; o Bibliotecario nao altera `agentes/fontes-confiaveis.json`.
