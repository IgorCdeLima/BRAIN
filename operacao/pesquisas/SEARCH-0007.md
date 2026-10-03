---
tipo: pesquisa
id: SEARCH-0007
status: respondida
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0015
criado: 2026-10-03
pesquisado_por: pesquisador
pesquisado_em: 2026-10-03
catalogado_em:
notas: []
tags: [seguranca, cwe-1088, timeout, postgresql, psycopg, sqlalchemy, disponibilidade]
---
# SEARCH-0007 - CWE-1088 e timeouts de consulta no psycopg 3 / libpq / SQLAlchemy

## Pergunta

1. **Confirmar na documentacao oficial** o que ja foi medido: o parametro `options` da libpq (e a variavel `PGOPTIONS`) aceita `-c statement_timeout=<ms>`; o `statement_timeout` e contado no servidor; o erro que chega ao cliente e `QueryCanceled` (SQLSTATE 57014), subclasse de `OperationalError` no psycopg 3. Fontes: postgresql.org (libpq "Parameter Key Words", "Client Connection Defaults") e psycopg.org (errors).
2. **Pergunta aberta:** com psycopg 3 sincrono (SQLAlchemy 2, engine sincrono), existe controle **do lado do cliente** que encerre uma consulta numa conexao ja aberta quando o processo do PostgreSQL esta congelado mas o kernel do servidor continua fazendo ACK? Avaliar `keepalives`, `keepalives_idle`, `keepalives_interval`, `keepalives_count` e `tcp_user_timeout` da libpq (o kernel responde ao keepalive e faz ACK, entao provavelmente **nao** cobrem), timeout de leitura no socket, e `pool_timeout`/`pool_recycle` do SQLAlchemy. Se nao houver controle simples, dizer isso explicitamente.
3. Mitigacoes oficiais da CWE-1088 (Synchronous Access of Remote Resource without Timeout) na MITRE.

## Contexto

Revisao de seguranca da T-0015 (lab, SEC-T0015-03). O humano decidiu que a correcao entra na T-0015. Medido em 2026-10-03:

- Tabela bloqueada por outra transacao: sem timeout, `GET /` fica preso mais de 30 s. Com `PGOPTIONS="-c statement_timeout=5000"` (override de teste), responde 503 em 5,1 s. **Correcao definida para o Dev, nao depende desta pesquisa** (pergunta 1 so confirma as fontes).
- Container do Postgres pausado (`docker pause`): mesmo com `statement_timeout`, 5 requisicoes ficam presas (uma por conexao do pool) ate o corte de 40 s do curl. **Residual**, nao exigido na T-0015. A pergunta 2 decide se vira cartao proprio.

`connect_timeout: 3` (ja usado) so vale para abrir conexao.

## Ja buscado no Brain

- Busca por `1088`, `statement_timeout`, `keepalive`, `tcp_user_timeout`: nenhuma nota.
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]: cita "timeouts" de forma generica, sem psycopg/libpq.

---

## Resposta

- **Resumo (3 a 5 linhas):** (1) Confirmado: `options`/`PGOPTIONS` aceita `-c statement_timeout=<ms>`, contado no servidor, erro `QueryCanceled` (57014) subclasse de `OperationalError`. (2) Nao ha controle simples no cliente para servidor congelado com kernel dando ACK: keepalives e `tcp_user_timeout` dependem de ACK/kernel, `pool_timeout`/`pool_recycle` nao limitam consulta em curso. Decidir entre cartao proprio (limite na aplicacao, pooler/proxy, healthcheck) ou risco aceito no lab. (3) CWE-1088 na MITRE nao traz mitigacoes; a implicita e timeout em toda chamada remota.
- **Notas geradas no Inbox:** [[statement_timeout se passa em options da libpq e vira QueryCanceled no psycopg 3]], [[Nao ha controle simples no cliente para consulta presa em servidor Postgres congelado]], [[CWE-1088 chamada remota sincrona sem timeout trava o servico]]
- **Links confiaveis:** https://www.postgresql.org/docs/current/libpq-connect.html ; https://www.postgresql.org/docs/current/runtime-config-client.html ; https://www.postgresql.org/docs/current/libpq-envars.html ; https://www.psycopg.org/psycopg3/docs/api/errors.html ; https://docs.sqlalchemy.org/en/20/core/pooling.html ; https://cwe.mitre.org/data/definitions/1088.html
- **Sem resposta / limites:** a documentacao nao trata o caso "processo congelado, kernel ativo"; a conclusao sobre keepalives/`tcp_user_timeout` e inferencia da semantica documentada, nao teste (confianca baixa). Solucoes de nivel de aplicacao nao foram pesquisadas a fundo nem testadas.
- **Conteudo suspeito descartado:** nenhum.

## Dominios propostos

- docs.sqlalchemy.org, cwe.mitre.org, psycopg.org, postgresql.org: conferir se ja constam em `agentes/fontes-confiaveis.json`; se nao, incluir (fontes primarias para Dev e Seguranca).

## Catalogacao
