---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0015
pesquisa: SEARCH-0007
confianca: media
fontes: [postgresql.org/docs/current/libpq-connect, postgresql.org/docs/current/runtime-config-client, postgresql.org/docs/current/libpq-envars, psycopg.org/psycopg3/docs/api/errors]
verificado_em: 2026-10-03
valido_para: PostgreSQL 18.6, psycopg 3
criado: 2026-10-03
decisao:
tags: [postgres, psycopg, libpq, timeout, statement_timeout, disponibilidade]
---
# statement_timeout se passa em options da libpq e vira QueryCanceled no psycopg 3

## Conteudo proposto

- O parametro `options` da libpq envia opcoes de linha de comando ao servidor no inicio da conexao (ex.: `-c geqo=off`); espacos separam argumentos. `-c statement_timeout=5000` vale para a sessao.
- `PGOPTIONS` (variavel de ambiente) tem o mesmo efeito do parametro `options`, usada quando o codigo nao informa um valor.
- `statement_timeout`: sem unidade, e milissegundos; padrao 0 (desligado). E contado **no servidor**, da chegada do comando ate o fim, e vale por instrucao (no protocolo estendido, comeca em Parse/Bind/Execute/Describe e termina em Execute ou Sync).
- No psycopg 3 o erro e `QueryCanceled` (SQLSTATE 57014), com cadeia `QueryCanceled -> OperationalError -> DatabaseError -> Error`. Tratar `OperationalError` ja cobre.
- Alternativas do servidor: `lock_timeout` (so espera por lock) e `idle_in_transaction_session_timeout` (sessao ociosa em transacao).

## Evidencia

Documentacao oficial do PostgreSQL 18.6 e do psycopg 3, lida em 2026-10-03. Confirma o que o Dev mediu na T-0015 (503 em 5,1 s com tabela bloqueada).

## Links confiaveis

- [libpq: Parameter Key Words](https://www.postgresql.org/docs/current/libpq-connect.html): semantica de `options`, `connect_timeout`, keepalives e `tcp_user_timeout`.
- [Client Connection Defaults](https://www.postgresql.org/docs/current/runtime-config-client.html): `statement_timeout`, `lock_timeout`, unidade e onde e contado.
- [psycopg 3 errors](https://www.psycopg.org/psycopg3/docs/api/errors.html): `QueryCanceled`, SQLSTATE 57014 e hierarquia.

## Por que e reaproveitavel

Qualquer servico Python com Postgres que precise limitar consulta lenta ou bloqueada.

## Relacionadas no Brain

- [[Candidato - statement_timeout via connect_args options cobre lock mas nao banco congelado]]
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]

## Decisao do Bibliotecario
