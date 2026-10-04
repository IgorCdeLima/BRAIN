---
tipo: padrao
status: ativo
origem: SEARCH-0008 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0008
tarefa: T-0013
confianca: media
fontes: [https://docs.sqlalchemy.org/en/20/core/engines.html, https://docs.sqlalchemy.org/en/20/core/exceptions.html, https://www.psycopg.org/psycopg3/docs/api/errors.html]
verificado_em: 2026-10-04
valido_para: SQLAlchemy 2.0 e psycopg 3
criado: 2026-10-04
decisao: promovido
revisar_em: 2027-04-04
tags: [seguranca, logs, sqlalchemy, psycopg, cwe-778, cwe-532]
---
# SQLAlchemyError no log: registrar classe e sqlstate, nunca str(erro) inteiro

## Contexto

Handler que captura `sqlalchemy.exc.SQLAlchemyError` e responde generico ao cliente (ver [[CWE-778 registro insuficiente se evita registrando erro de banco com classe e sqlstate no log do servidor]]).

## Problema

Registrar `str(erro)` pode levar dado do usuario ao log: a string de `StatementError`/`DBAPIError` inclui o SQL e os parametros, e o texto do servidor pode citar valores (ex.: DETAIL de violacao de unicidade do PostgreSQL).

## Solucao

Registrar so o que nao carrega dado do usuario:

```python
except SQLAlchemyError as erro:
    sqlstate = getattr(getattr(erro, "orig", None), "sqlstate", None)
    logger.error("erro de banco: %s sqlstate=%s", type(erro).__name__, sqlstate)
    # resposta 503 generica
```

- `erro.orig` e a excecao original do driver (documentado em `DBAPIError`). No psycopg 3, `sqlstate` e atributo de `psycopg.Error` (`str | None`; tambem em `erro.orig.diag.sqlstate`). Use `getattr`: `orig` pode ser `None` e `sqlstate` pode ser `None` (erro sem resposta do servidor, como queda de conexao).
- `create_engine(..., hide_parameters=True)` impede que os parametros apareçam na string de `StatementError` e no log INFO do engine (confirmado na doc oficial). E defesa em profundidade; nao substitui evitar `str(erro)`.
- Mesmo com `hide_parameters=True`, `str(erro)` ainda inclui o texto do driver/servidor. **Isto e conhecimento geral, nao confirmado na doc**: confirmar com teste antes de confiar.
- Evite `logger.exception(...)` com traceback sem filtro: o traceback imprime a mensagem da excecao.

## Trade-offs

- **Ganha:** log util para operacao (classe + sqlstate identificam timeout, integridade, conexao) sem PII.
- **Perde:** menos detalhe para depurar; para investigar um caso, reproduzir com dados de teste.

## Evidencia

Doc oficial do SQLAlchemy 2 (`hide_parameters`, atributos `statement`, `params`, `orig`) e do psycopg 3 (`Error.sqlstate`). A doc nao descreve literalmente o formato `[parameters: ...]` da mensagem. **Teste pendente:** forcar um erro com parametro conhecido e conferir que o valor nao aparece no log.

## Links confiaveis

- [SQLAlchemy 2 - Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html): `hide_parameters`.
- [SQLAlchemy 2 - Core Exceptions](https://docs.sqlalchemy.org/en/20/core/exceptions.html): `StatementError`/`DBAPIError`, `statement`, `params`, `orig`.
- [psycopg 3 - errors](https://www.psycopg.org/psycopg3/docs/api/errors.html): `Error.sqlstate` e `diag.sqlstate`.

## Quando NAO usar

Em depuracao local com dados de teste, o traceback completo e aceitavel. Fora disso, nao.

## Relacionadas

- [[CWE-778 registro insuficiente se evita registrando erro de banco com classe e sqlstate no log do servidor]]: a fraqueza que este padrao resolve.
- [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]]: mensagem generica ao cliente.
- [[Commit ambiguo - se a conexao cai no COMMIT, conferir a linha antes de apagar o arquivo]]: usa o `sqlstate` para decidir o que fazer.

## Decisao do Bibliotecario

Promovido a padrao em `10_Conhecimento` (2026-10-04). Sem duplicata. Lacuna declarada (teste do formato da mensagem) mantida visivel na Evidencia; confianca `media` ate o teste.
