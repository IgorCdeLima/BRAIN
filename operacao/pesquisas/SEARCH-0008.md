---
tipo: pesquisa
id: SEARCH-0008
status: catalogada
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0013
criado: 2026-10-04
pesquisado_por: pesquisador
pesquisado_em: 2026-10-04
catalogado_em: 2026-10-04
notas: ["CWE-778 registro insuficiente se evita registrando erro de banco com classe e sqlstate no log do servidor", "SQLAlchemyError no log: registrar classe e sqlstate, nunca str(erro) inteiro"]
tags: [seguranca, cwe-778, logs, sqlalchemy, fastapi]
---
# SEARCH-0008 - CWE-778 registro insuficiente: o que registrar de erro de banco sem vazar dado

## Pergunta

1. Nota de referencia da **CWE-778 (Insufficient Logging)** para a stack do lab: o que e, como aparece em FastAPI + SQLAlchemy 2 + uvicorn, controle e como testar (no formato das notas `CWE-...` de `10_Conhecimento`).
2. Ao capturar `sqlalchemy.exc.SQLAlchemyError` e devolver mensagem generica ao cliente, o que registrar no log do servidor **sem** vazar dados do usuario? Confirmar na documentacao oficial do SQLAlchemy 2: a mensagem da excecao inclui `[parameters: ...]`; `create_engine(hide_parameters=True)` esconde os parametros da mensagem e do log; como ler o `sqlstate` do psycopg 3 (`erro.orig.sqlstate`).

## Contexto

Revisao de seguranca da T-0013 (lab), `SEC-T0013-01`: `except SQLAlchemyError` em `app/main.py` vira 503 sem nenhum registro. A recomendacao e registrar classe e `sqlstate`, sem `str(erro)` inteiro. Premissa usada no SEC (a confirmar): a mensagem do SQLAlchemy traz os parametros, e `hide_parameters=True` os oculta. Fontes ja lidas: MITRE CWE-778 e OWASP Logging Cheat Sheet (2026-10-04).

## Ja buscado no Brain

- Tag `seguranca`, termos "CWE-778", "logging", "log", "hide_parameters": nenhuma nota da CWE-778.
- [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]]: cobre o lado do cliente (mensagem generica) e cita "detalhe no log", mas nao diz o que registrar nem como evitar dado pessoal no log.

---

## Resposta

- **Resumo (3 a 5 linhas):** CWE-778 aplicada ao handler de SQLAlchemyError: responder generico ao cliente mas registrar no servidor classe e sqlstate. `hide_parameters=True` confirmado na doc oficial como ocultando parametros do log INFO e da string de StatementError. sqlstate se le em `erro.orig.sqlstate` (psycopg 3, pode ser None). Ressalva: a premissa do SEC sobre `[parameters: ...]` na mensagem nao foi lida literalmente na doc, e o texto do servidor em `str(erro)` ainda pode conter valores; recomendado teste.
- **Notas geradas no Inbox:** [[CWE-778 registro insuficiente se evita registrando erro de banco com classe e sqlstate no log do servidor]], [[SQLAlchemyError no log: registrar classe e sqlstate, nunca str(erro) inteiro]]
- **Links confiaveis:** MITRE CWE-778; OWASP Logging Cheat Sheet; docs SQLAlchemy 2 (engines, exceptions); docs psycopg 3 (errors).
- **Sem resposta / limites:** formato exato `[parameters: ...]` e o conteudo do DETAIL do PostgreSQL em `str(erro)` nao confirmados em fonte primaria; fica como teste a fazer.
- **Conteudo suspeito descartado:** nenhum.

## Dominios propostos

- 

## Catalogacao

- **Decisao:** promovidas as duas notas (2026-10-04), como padrao em `10_Conhecimento`.
- **Notas finais:** [[CWE-778 registro insuficiente se evita registrando erro de banco com classe e sqlstate no log do servidor]], [[SQLAlchemyError no log: registrar classe e sqlstate, nunca str(erro) inteiro]]. A CWE-778 entrou no [[Mapa das CWE relevantes para Python e FastAPI]]. Links confiaveis preservados nas duas notas.
- **Pendencia:** teste do formato da mensagem do SQLAlchemy com parametro conhecido (confianca fica `media` ate la).
