---
tipo: aprendizado
status: ativo
origem: T-0013 (Dev), curado pelo Bibliotecario
tarefa: T-0013
confianca: alta
fontes: ["lab: operacao/tarefas/T-0013.md (roteiro P5)"]
verificado_em: 2026-10-04
valido_para: lab (FastAPI lifespan + Compose restart unless-stopped)
criado: 2026-10-04
decisao: promovido
tags: [compose, restart, lifespan, postgres]
---
# Subida do app com tabela travada falha com log claro e reinicia sem laco apertado

## O que aconteceu

`criar_tabelas` roda `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`, que pede lock exclusivo. Com `LOCK TABLE produto` segurado por outra sessao (40 s), o app falhou com `QueryCanceled` (`statement_timeout` de 5 s) e "Application startup failed. Exiting."; o `restart: unless-stopped` o subiu de novo (3 reinicios) e ele ficou no ar assim que o lock saiu. O Docker espaca os reinicios (backoff): nao ha laco apertado, e o log tem o SQL e o erro.

Com `DB_STATEMENT_TIMEOUT_MS` invalido (`abc`, `99999999999`) o valor cai para 5000 e o app sobe normal.

## O que aprendemos

- O `statement_timeout` tambem protege a subida: o lifespan nao fica preso para sempre num lock (ver [[statement_timeout se passa em options da libpq e vira QueryCanceled no psycopg 3]]).
- Falha no lifespan + `restart: unless-stopped` e um retry natural, com backoff do Docker e log claro; nao e preciso retry proprio so por isso.
- Limite: contra servidor Postgres **congelado** o timeout do cliente nao ajuda ([[Nao ha controle simples no cliente para consulta presa em servidor Postgres congelado]]).

## O que muda a partir de agora

Nenhuma regra nova. Quem avaliar um retry no lifespan deve partir daqui: o comportamento atual ja e aceitavel com lock temporario. Roteiro para repetir: `psql` em segundo plano com `BEGIN; LOCK TABLE <tabela> IN ACCESS EXCLUSIVE MODE; SELECT pg_sleep(40);`, `docker compose restart app`, `docker inspect ... RestartCount`.

## Origem

T-0013 (lab), pendencia P5 herdada da T-0015, executada pelo Dev em 2026-10-04.
