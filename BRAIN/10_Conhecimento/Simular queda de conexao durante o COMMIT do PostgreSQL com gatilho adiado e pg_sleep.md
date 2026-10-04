---
tipo: experimento
status: ativo
categoria: teste
linguagem: bash, SQL (PostgreSQL)
origem: agente/seguranca
tarefa: T-0013
confianca: media
fontes: ["https://www.postgresql.org/docs/current/sql-createtrigger.html", "https://www.postgresql.org/docs/current/functions-admin.html"]
verificado_em: 2026-10-04
valido_para: PostgreSQL 16+ em container (imagem oficial), cliente psycopg 3 / SQLAlchemy 2
ultimo_uso: 2026-10-04
criado: 2026-10-04
decisao: promovido
tags: [experimento, postgresql, commit, transacao, teste, seguranca]
---
# Simular queda de conexao durante o COMMIT do PostgreSQL com gatilho adiado e pg_sleep

## Objetivo

Reproduzir ao vivo (sem monkeypatch) o que a aplicacao faz quando a conexao cai **no meio do COMMIT**: com erro que traz SQLSTATE (backend encerrado pelo servidor) e sem SQLSTATE (conexao cortada). Serve para conferir limpeza de recursos fora do banco (arquivo gravado antes do commit, mensagem enviada etc.).

## Quando usar

- Codigo que trata "commit ambiguo" ou apaga/cria algo fora do banco conforme o resultado do commit.
- Criterio de aceite do tipo "sem arquivo orfao / sem linha apontando para arquivo inexistente".
- NAO usar em banco compartilhado: o passo (b) derruba o servidor inteiro (recuperacao de crash).

## Por que este metodo e nao outro

- Monkeypatch so prova o ramo do codigo, nao o erro real do driver (classe, `sqlstate`, estado da sessao depois).
- `docker pause` no banco congela o COMMIT para sempre (o `statement_timeout` e do servidor) e nao gera erro.
- Um `CONSTRAINT TRIGGER ... DEFERRABLE INITIALLY DEFERRED` roda **dentro do COMMIT**: o `pg_sleep` abre uma janela de segundos em que a conexao esta no COMMIT, facil de acertar com outro comando.

## Ambiente

Validado com PostgreSQL da imagem oficial em Docker Compose, app Python com SQLAlchemy 2 + psycopg 3, 2026-10-04.

## Como rodar

Sempre contra um projeto Compose proprio e descartavel (`-p <projeto-isolado>`), nunca o banco do humano.

```bash
# parametros
P=<projeto-isolado>; TABELA=<tabela>; URL=<url-do-post>
psql(){ docker compose -p $P exec -T db sh -c "psql -qtA -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\" -c \"$1\""; }

psql "CREATE OR REPLACE FUNCTION exp_dorme() RETURNS trigger LANGUAGE plpgsql AS \\\$\\\$ BEGIN PERFORM pg_sleep(6); RETURN NULL; END \\\$\\\$;"
psql "CREATE CONSTRAINT TRIGGER exp_commit AFTER INSERT ON $TABELA DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION exp_dorme();"

# (a) erro COM sqlstate (57P01 admin_shutdown): servidor desfaz a transacao
( curl -s -o /dev/null -w '%{http_code}\n' <dados do POST> $URL ) & sleep 2
psql "select pg_terminate_backend(pid) from pg_stat_activity where query like 'COMMIT%' and pid<>pg_backend_pid()"; wait

# (b) conexao cortada SEM sqlstate: kill -9 do backend (o servidor entra em recuperacao por ~1-3 s)
( curl -s -o /dev/null -w '%{http_code}\n' <dados do POST> $URL ) & sleep 2
PID=$(psql "select pid from pg_stat_activity where query like 'COMMIT%' and pid<>pg_backend_pid()")
docker compose -p $P exec -T db kill -9 $PID; wait

# limpeza obrigatoria
psql "DROP TRIGGER exp_commit ON $TABELA; DROP FUNCTION exp_dorme();"
```

## Script

O proprio bloco acima (sem script separado).

## Como interpretar

- Depois de cada caso: contar as linhas inseridas e os recursos externos (ex.: arquivos na pasta de uploads) e ler o log do app.
- (a) a linha **nao** existe; o app deve tratar como falha definitiva (desfazer o efeito externo).
- (b) a linha **nao** existe (o COMMIT nao terminou), mas o cliente nao sabe: o app ve `OperationalError` sem `sqlstate`. Se ele confere numa conexao nova, essa conferencia costuma falhar (servidor em recuperacao), e um app prudente mantem o efeito externo e registra aviso.

## Limites e cuidados

- Nao reproduz o caso "COMMIT gravado e confirmacao perdida" (o gatilho roda antes da gravacao). Esse ramo continua so por monkeypatch.
- (b) derruba todas as conexoes do servidor; usar so em banco isolado.
- `query like 'COMMIT%'` supoe que so a requisicao de teste esta em COMMIT.

## Historico de uso

| Data | Tarefa e registro | Contexto e motivo do uso | Resultado | Script mudou? |
|---|---|---|---|---|
| 2026-10-04 | T-0013 (lab), revisao de seguranca (cartao, secao Revisao de seguranca) | Conferir o P3 (commit ambiguo com imagem gravada antes) | (a) 503, sem linha, arquivo apagado; (b) 503, sem linha, arquivo mantido como orfao e `log.warning` | nao |

## Versoes anteriores

## Relacionadas no Brain

- [[Commit ambiguo - se a conexao cai no COMMIT, conferir a linha antes de apagar o arquivo]] : o padrao que este experimento testa.
- [[statement_timeout se passa em options da libpq e vira QueryCanceled no psycopg 3]]: outro erro com sqlstate (57014) tratado como definitivo.

## Decisao do Bibliotecario

Promovido a experimento ativo em `10_Conhecimento` (2026-10-04). Script generalizado conferido: parametros no topo (`P`, `TABELA`, `URL`), sem dados do projeto nem segredos; roda so em projeto Compose isolado e descartavel (aviso de que o caso b derruba o servidor esta em "Limites e cuidados"). Ligado ao padrao que ele sustenta. Historico de uso ja tem a linha da T-0013.
