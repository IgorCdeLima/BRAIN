---
tipo: padrao
status: ativo
origem: agente/dev (candidato da tarefa T-0002, curado pelo Bibliotecário)
confianca: media
fontes: ["projetos/lab: T-0002 (34 testes passando em 0,53 s)"]
verificado_em: 2026-09-29
valido_para: FastAPI + SQLAlchemy 2 + PostgreSQL 18 em Docker Compose (projeto lab)
criado: 2026-09-29
tags: [pytest, fastapi, sqlalchemy, testes]
decisao: promovido
---
# Testes com banco separado e rollback por teste funcionam no FastAPI com SQLAlchemy

## Contexto

Projeto FastAPI com banco relacional, onde os testes não podem misturar dados com os da aplicação. No piloto 1 os testes usavam o banco da aplicação.

## Problema

Testes que escrevem no banco real sujam os dados da aplicação e deixam um teste interferir no outro.

## Solução

- O `conftest` cria um banco separado, `<POSTGRES_DB>_test`.
- Cada teste roda numa transação que sofre rollback ao final.
- A dependência `get_session` do FastAPI é substituída via `app.dependency_overrides` pela sessão dessa transação.

Evidência (T-0002): 34 testes passaram com `docker compose run --rm app pytest`; a aplicação subiu depois e o banco dela ficou intacto. O cliente de teste usou `httpx2`, ver [[TestClient do Starlette 1.x prefere httpx2 a httpx]].

## Trade-offs

- **Ganha:** isolamento total, testes rápidos, sem limpeza manual.
- **Perde:** o `now()` do PostgreSQL passa a valer igual para todo o teste ([[Com rollback por teste now() do PostgreSQL da o mesmo horario a todos os registros]]); commit real e concorrência não são exercitados.

## Quando NÃO usar

Testes que precisam de commits reais (transações concorrentes, ações pós-commit).

## Relacionadas

- [[Com rollback por teste now() do PostgreSQL da o mesmo horario a todos os registros]]: armadilha deste padrão.
- [[TestClient do Starlette 1.x prefere httpx2 a httpx]]: cliente usado nos testes.

## Decisão do Bibliotecário

**Promovido** em 2026-09-29. Sem duplicata. Confiança média: uma só execução, sem fonte externa. Título mantido como afirmação.
