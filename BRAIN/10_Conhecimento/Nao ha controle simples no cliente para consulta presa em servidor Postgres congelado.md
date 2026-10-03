---
tipo: problema-solucao
status: ativo
origem: SEARCH-0007 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0007
tarefa: T-0015
confianca: baixa
fontes: ["https://www.postgresql.org/docs/current/libpq-connect.html", "https://docs.sqlalchemy.org/en/20/core/pooling.html", "medicao T-0015 (lab)"]
verificado_em: 2026-10-03
valido_para: "PostgreSQL 18.6, libpq, SQLAlchemy 2 com psycopg 3 sincrono"
criado: 2026-10-03
decisao: promovido
revisar_em: 2026-12-03
tags: [postgres, libpq, sqlalchemy, timeout, keepalive, disponibilidade]
---
# Nao ha controle simples no cliente para consulta presa em servidor Postgres congelado

> Confianca **baixa**: a parte "nao cobre" e inferencia da semantica documentada, nao teste. Tratar como pista a verificar antes de decidir sobre o risco.

## Sintoma

Processo do Postgres parado (ex.: `docker pause`), com o kernel do host ainda respondendo ACK. Mesmo com `statement_timeout`, uma requisicao por conexao do pool fica presa (na T-0015: 5 requisicoes presas ate o corte de 40 s do curl).

## Ambiente

PostgreSQL 18.6, libpq, SQLAlchemy 2 com psycopg 3 sincrono.

## Causa raiz

Nenhum parametro documentado cobre o caso diretamente:

- `keepalives*`: o keepalive e respondido pelo kernel do servidor, que continua vivo; a conexao nao e dada como morta (inferencia).
- `tcp_user_timeout` (ms): corta quando dados enviados ficam **sem ACK**; com o kernel dando ACK, nao dispara (inferencia).
- `connect_timeout`: so vale ao abrir conexao.
- SQLAlchemy `pool_timeout`: so a espera por conexao livre; `pool_recycle`: so troca conexao velha no proximo checkout. Nenhum limita consulta em conexao ja entregue.
- `statement_timeout` e do servidor: servidor congelado nao o executa.

## Solucao

Nao ha solucao simples. Saidas possiveis, **nao testadas**, a avaliar em cartao proprio: limite no nivel da aplicacao (worker/thread com prazo e descarte da conexao), proxy ou pooler na frente com timeout proprio, ou healthcheck que tira o servico do ar. Se o residual (ate `pool_size` requisicoes presas) e aceitavel num lab, registrar como risco aceito.

## Como verificar que foi resolvido

Pausar o container do banco (`docker pause`) e medir quantas requisicoes ficam presas e por quanto tempo, com e sem a saida adotada.

## O que nao funcionou

`statement_timeout`, `connect_timeout`, `pool_timeout`, `pool_recycle`: cobrem outros cenarios ([[statement_timeout via connect_args options cobre lock mas nao banco congelado]]).

## Relacionadas

- [[statement_timeout se passa em options da libpq e vira QueryCanceled no psycopg 3]]: o que o `statement_timeout` cobre.
- [[CWE-1088 chamada remota sincrona sem timeout trava o servico]]: a classe de fraqueza.
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]

## Links confiaveis

- [libpq: Parameter Key Words](https://www.postgresql.org/docs/current/libpq-connect.html): `keepalives_*` e `tcp_user_timeout`.
- [SQLAlchemy: Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html): `pool_timeout` e `pool_recycle` e seus limites.

## Origem

SEARCH-0007 (pergunta 2) e medicao da T-0015 (lab).

## Decisao do Bibliotecario

Promovido (2026-10-03) com `confianca: baixa` e revisao em 2 meses, porque registra um resultado negativo util (evita procurar o parametro que nao existe). A inferencia precisa de teste antes de virar certeza.
