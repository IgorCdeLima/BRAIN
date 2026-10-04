---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/pesquisador
tarefa: T-0013
pesquisa: SEARCH-0008
confianca: media
fontes: [https://docs.sqlalchemy.org/en/20/core/engines.html, https://docs.sqlalchemy.org/en/20/core/exceptions.html, https://www.psycopg.org/psycopg3/docs/api/errors.html]
verificado_em: 2026-10-04
valido_para: SQLAlchemy 2.0 e psycopg 3
criado: 2026-10-04
decisao:
tags: [seguranca, logs, sqlalchemy, psycopg, cwe-778, cwe-532]
---
# SQLAlchemyError no log: registrar classe e sqlstate, nunca str(erro) inteiro

## Conteudo proposto

Ao capturar `sqlalchemy.exc.SQLAlchemyError` e responder generico ao cliente, registre no servidor so o que nao carrega dado do usuario:

```python
except SQLAlchemyError as erro:
    sqlstate = getattr(getattr(erro, "orig", None), "sqlstate", None)
    logger.error("erro de banco: %s sqlstate=%s", type(erro).__name__, sqlstate)
    # resposta 503 generica
```

- `erro.orig` e a excecao original do driver (documentado em `DBAPIError`); no psycopg 3, `sqlstate` e atributo de `psycopg.Error` (`str | None`; tambem em `erro.orig.diag.sqlstate`). Use `getattr` porque `orig` pode ser `None` e `sqlstate` pode ser `None` (erro sem resposta do servidor, como queda de conexao).
- A string de `StatementError`/`DBAPIError` inclui o SQL e os parametros do usuario. `create_engine(..., hide_parameters=True)` impede que os parametros sejam formatados nessa string e no log INFO do engine. Confirmado na doc oficial (frase: parametros nao aparecem no log INFO nem na representacao em string de `StatementError`).
- Mesmo com `hide_parameters=True`, `str(erro)` ainda inclui o texto do driver/servidor, que pode conter valores (ex.: o DETAIL de violacao de unicidade do PostgreSQL costuma citar o valor da chave). **Isto vem de conhecimento geral, nao foi confirmado na doc nesta pesquisa**: verificar com um teste antes de confiar. Por isso registrar classe + sqlstate, e nao `str(erro)`.
- Evite `logger.exception(...)` com traceback completo sem filtro: o traceback imprime a mensagem da excecao.
- Ligar `hide_parameters=True` e defesa em profundidade; nao substitui nao registrar `str(erro)`.

## Evidencia

Doc oficial do SQLAlchemy 2 (`hide_parameters`, atributos `statement`, `params`, `orig`) e do psycopg 3 (`Error.sqlstate`). A doc de excecoes do SQLAlchemy nao descreve literalmente o formato `[parameters: ...]` na mensagem; a premissa do SEC e coerente com `hide_parameters` mas o formato exato nao foi lido na fonte. Sugestao: teste curto que forca um erro com parametro conhecido e confere que o valor nao aparece no log.

## Links confiaveis

- [SQLAlchemy 2 - Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html): `hide_parameters` em `create_engine`.
- [SQLAlchemy 2 - Core Exceptions](https://docs.sqlalchemy.org/en/20/core/exceptions.html): `StatementError`/`DBAPIError`, atributos `statement`, `params`, `orig`.
- [psycopg 3 - errors](https://www.psycopg.org/psycopg3/docs/api/errors.html): `Error.sqlstate` e `diag.sqlstate`.

## Por que e reaproveitavel

Todo handler de erro de banco em FastAPI/SQLAlchemy precisa registrar sem vazar PII para o log.

## Relacionadas no Brain

- [[CWE-778 registro insuficiente se evita registrando erro de banco com classe e sqlstate no log do servidor]]
- [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]]

## Decisao do Bibliotecario

