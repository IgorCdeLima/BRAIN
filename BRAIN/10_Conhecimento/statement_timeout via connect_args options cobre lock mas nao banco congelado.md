---
tipo: problema-solucao
status: ativo
origem: T-0015 (Dev), curado pelo Bibliotecario
tarefa: T-0015
confianca: media
fontes: ["lab tests/test_banco_fora.py (T-0015)", "https://www.postgresql.org/docs/current/runtime-config-client.html"]
verificado_em: 2026-10-03
valido_para: "psycopg 3 + SQLAlchemy 2 + PostgreSQL 18"
criado: 2026-10-03
decisao: promovido
revisar_em: 2027-04-03
tags: [postgres, sqlalchemy, timeout, disponibilidade, seguranca, teste]
---
# statement_timeout via connect_args options cobre lock mas nao banco congelado

## Sintoma

Com a tabela bloqueada por outra transacao, `GET /` fica preso mais de 30 s mesmo com `connect_timeout` configurado. Com o container do Postgres pausado, requisicoes ficam presas ate o corte do cliente.

## Ambiente

psycopg 3 + SQLAlchemy 2 (sincrono) + PostgreSQL 18, FastAPI (lab, T-0015).

## Causa raiz

Premissa errada da correcao anterior: `connect_timeout` so vale para **abrir** conexao; consulta em conexao ja aberta do pool ficava sem limite.

## Solucao

```python
create_engine(url, connect_args={"connect_timeout": 3, "options": "-c statement_timeout=5000"})
```

Toda consulta que espera mais de 5 s vira `QueryCanceled` (subclasse de `OperationalError`). Se o app ja trata `OperationalError` como 503, nao precisa de codigo novo ([[Pagina de 503 que consulta o banco vira 500 justamente quando o servidor esta sobrecarregado]]). Detalhes de `options`, `PGOPTIONS` e do erro: [[statement_timeout se passa em options da libpq e vira QueryCanceled no psycopg 3]].

**Limite:** nao cobre servidor congelado (processo parado, kernel ainda responde ACK): ate `pool_size` requisicoes ficam presas. Ver [[Nao ha controle simples no cliente para consulta presa em servidor Postgres congelado]].

## Como verificar que foi resolvido

Teste automatico sem sleep longo: uma conexao do teste segura `LOCK TABLE produto IN ACCESS EXCLUSIVE MODE` numa transacao aberta; o engine real do app, com `statement_timeout` de 500 ms (por variavel de ambiente), devolve 503 em ~0,5 s. Reiniciar o `_engine` global com monkeypatch e apontar `POSTGRES_DB` ao banco de teste. Manual: tabela bloqueada, `GET /` 503 em 5,11 s (antes, mais de 30 s). 3 testes novos em `tests/test_banco_fora.py` passam.

## O que nao funcionou

Confiar so em `connect_timeout`. Nao houve leitura de documentacao oficial pelo Dev; a confirmacao das fontes veio do SEARCH-0007.

## Relacionadas

- [[CWE-1088 chamada remota sincrona sem timeout trava o servico]]: a classe de fraqueza.
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: o controle de timeout generico.

## Origem

T-0015 (lab), Dev; confirmacao documental no SEARCH-0007.

## Decisao do Bibliotecario

Promovido (2026-10-03) com confianca media (medido no lab; fonte oficial confirmada no SEARCH-0007). Sem duplicata.
