---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/pesquisador
tarefa: T-0015
pesquisa: SEARCH-0007
confianca: baixa
fontes: [postgresql.org/docs/current/libpq-connect, docs.sqlalchemy.org/en/20/core/pooling]
verificado_em: 2026-10-03
valido_para: PostgreSQL 18.6, libpq, SQLAlchemy 2 com psycopg 3 sincrono
criado: 2026-10-03
decisao:
tags: [postgres, libpq, sqlalchemy, timeout, keepalive, disponibilidade]
---
# Nao ha controle simples no cliente para consulta presa em servidor Postgres congelado

## Conteudo proposto

Cenario: processo do Postgres parado (ex.: `docker pause`), mas o kernel do host continua respondendo ACK. Conclusao da pesquisa: **nenhum parametro documentado cobre isso de forma direta.**

- `keepalives`, `keepalives_idle`, `keepalives_interval`, `keepalives_count`: o keepalive e respondido pelo kernel do servidor, que continua vivo. A conexao nao e dada como morta. (Inferencia a partir da documentacao, nao teste.)
- `tcp_user_timeout` (ms): corta quando dados enviados ficam **sem ACK**. Com o kernel dando ACK, nao dispara. (Inferencia.)
- `connect_timeout`: so vale ao abrir conexao.
- SQLAlchemy `pool_timeout`: so a espera por conexao livre no pool. `pool_recycle`: so troca conexao velha no proximo checkout. Nenhum limita consulta em conexao ja entregue.
- `statement_timeout` e do servidor: servidor congelado nao o executa.

Saidas possiveis, **nao testadas aqui**, a avaliar num cartao proprio: limite no nivel da aplicacao (worker/thread com prazo e descarte da conexao), proxy/pooler na frente com timeout proprio, ou healthcheck que tira o servico do ar. Se o residual (ate `pool_size` requisicoes presas) e aceitavel num lab, registrar como risco aceito.

## Evidencia

Leitura da documentacao oficial (links). A parte "nao cobre" e dedução da semantica documentada; a documentacao nao trata o caso de processo congelado com kernel ativo. Medicao da T-0015 (5 requisicoes presas ate 40 s com container pausado) e consistente.

## Links confiaveis

- [libpq: Parameter Key Words](https://www.postgresql.org/docs/current/libpq-connect.html): definicao de keepalives_* e `tcp_user_timeout` (dados sem ACK).
- [SQLAlchemy: Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html): `pool_timeout` e `pool_recycle` e seus limites.

## Por que e reaproveitavel

Decide se "servidor de banco travado" exige cartao proprio ou risco aceito em qualquer app com pool de conexoes.

## Relacionadas no Brain

- [[Candidato - statement_timeout via connect_args options cobre lock mas nao banco congelado]]
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]

## Decisao do Bibliotecario
