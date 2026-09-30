---
tipo: padrao
status: ativo
origem: SEARCH-0001 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#25)
criado: 2026-09-30
decisao: promovido
revisar_em: 2027-03-30
tags: [seguranca, cwe, cwe-770, dos, limites]
---
# CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit

## Contexto

**O que e:** a aplicacao aloca memoria, disco, CPU ou conexoes sem teto, e uma requisicao (ou muitas) esgota o recurso (negacao de servico).

**Como aparece na nossa stack:**
- Upload lido inteiro em memoria (`await file.read()`) sem limite (foi o SEC-0001).
- Listagens sem paginacao; parametro `limit` sem maximo.
- Campos de texto/JSON sem `max_length`; corpo JSON gigante ou muito aninhado.
- Sem timeout em chamadas externas e sem limite de conexoes/pool.
- Sem rate limit em login e endpoints caros.

## Solucao

**Controle:**
1. Limite de tamanho do corpo aplicado ao ler (por blocos) e tambem no proxy reverso.
2. `max_length`/`le`/`ge` nos modelos Pydantic e `Query(le=100)` em paginacao.
3. Timeouts de leitura/conexao (servidor e cliente HTTP), pool de conexoes com teto.
4. Rate limiting por IP/usuario (proxy ou middleware).
5. Limites de memoria/CPU do container no Docker.

**Como testar:** corpo acima do limite (com e sem `Content-Length`), `limit=10000000`, campo com 10 MB, muitas requisicoes em sequencia; esperar 413/422/429 e memoria estavel.

## Evidencia

Cheat sheet OWASP de Denial of Service consultado em 2026-09-30: limite de tamanho de requisicao, restricoes de upload, rate limiting, timeouts e validacao de entrada que controla alocacao.

## Links confiaveis

- [CWE-770 (MITRE)](https://cwe.mitre.org/data/definitions/770.html): definicao oficial.
- [Denial of Service Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html): controles de camada de aplicacao.

## Por que e reaproveitavel

Complementa upload e validacao de entrada em todo servico web.

## Relacionadas no Brain

- [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]
- [[CWE-20 entrada extrema gerando erro 500 se evita validando com Pydantic e handler global]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-09-30) como padrao ativo: cheat sheet OWASP de DoS lido; liga-se a [[Recusa previa por Content-Length esconde a validacao do upload]] (caso SEC-0001). Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
