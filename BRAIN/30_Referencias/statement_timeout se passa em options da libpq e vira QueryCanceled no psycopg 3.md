---
tipo: referencia
status: ativo
origem: SEARCH-0007 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0007
tarefa: T-0015
autor: PostgreSQL Global Development Group; psycopg
url: https://www.postgresql.org/docs/current/libpq-connect.html
acessado_em: 2026-10-03
confianca: media
fontes: ["https://www.postgresql.org/docs/current/libpq-connect.html", "https://www.postgresql.org/docs/current/runtime-config-client.html", "https://www.postgresql.org/docs/current/libpq-envars.html", "https://www.psycopg.org/psycopg3/docs/api/errors.html"]
verificado_em: 2026-10-03
valido_para: "PostgreSQL 18.6, psycopg 3"
criado: 2026-10-03
decisao: promovido
revisar_em: 2027-04-03
tags: [postgres, psycopg, libpq, timeout, statement_timeout, disponibilidade]
---
# statement_timeout se passa em options da libpq e vira QueryCanceled no psycopg 3

## Resumo

- O parametro `options` da libpq envia opcoes de linha de comando ao servidor no inicio da conexao (ex.: `-c geqo=off`); espacos separam argumentos. `-c statement_timeout=5000` vale para a sessao.
- `PGOPTIONS` (variavel de ambiente) tem o mesmo efeito, usada quando o codigo nao informa `options`.
- `statement_timeout`: sem unidade, milissegundos; padrao 0 (desligado). E contado **no servidor**, da chegada do comando ate o fim, e vale por instrucao (no protocolo estendido, comeca em Parse/Bind/Execute/Describe e termina em Execute ou Sync).
- No psycopg 3 o erro e `QueryCanceled` (SQLSTATE 57014), com cadeia `QueryCanceled -> OperationalError -> DatabaseError -> Error`. Tratar `OperationalError` ja cobre.
- Alternativas do servidor: `lock_timeout` (so espera por lock) e `idle_in_transaction_session_timeout` (sessao ociosa em transacao).

## O que aproveitar

Aplicacao pratica e teste: [[statement_timeout via connect_args options cobre lock mas nao banco congelado]]. Confirma o que o Dev mediu na T-0015 (503 em 5,1 s com tabela bloqueada).

## Ressalvas

Cobre a versao 18.6 do PostgreSQL e o psycopg 3; nao cobre servidor congelado ([[Nao ha controle simples no cliente para consulta presa em servidor Postgres congelado]]).

## Links confiaveis

- [libpq: Parameter Key Words](https://www.postgresql.org/docs/current/libpq-connect.html): `options`, `connect_timeout`, keepalives e `tcp_user_timeout`.
- [Client Connection Defaults](https://www.postgresql.org/docs/current/runtime-config-client.html): `statement_timeout`, `lock_timeout`, unidade e onde e contado.
- [psycopg 3 errors](https://www.psycopg.org/psycopg3/docs/api/errors.html): `QueryCanceled`, SQLSTATE 57014 e hierarquia.

## Notas derivadas

- [[statement_timeout via connect_args options cobre lock mas nao banco congelado]]
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: controle generico de timeout.
- [[CWE-1088 chamada remota sincrona sem timeout trava o servico]]: a classe de fraqueza.

## Decisao do Bibliotecario

Promovido (2026-10-03) como referencia em `30_Referencias`. Sem duplicata (busca por `statement_timeout`, `QueryCanceled`, `libpq`: nenhuma nota).
