---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/pesquisador
tarefa: pauta
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org, docs.sqlalchemy.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#2); SQLAlchemy 2.0
criado: 2026-09-30
decisao:
tags: [seguranca, cwe, cwe-89, sql-injection, sqlalchemy]
---
# CWE-89 SQL injection se evita com parametros vinculados do SQLAlchemy e nunca com f-string

## Conteudo proposto

**O que e:** entrada do usuario vira parte do texto da consulta SQL e altera a sua estrutura. 2o lugar no CWE Top 25 de 2025.

**Como aparece na nossa stack:**
- `session.execute(text(f"SELECT ... WHERE nome = '{nome}'"))` ou `.format()` / `%` em `text()`.
- `order_by(text(campo))` ou nome de coluna/tabela vindo do parametro da rota (parametros vinculados nao protegem identificadores).
- `filter(text(...))` com concatenacao.

**Controle:**
1. Usar a API do ORM/Core (`select(Modelo).where(Modelo.nome == nome)`), que vincula parametros sozinha.
2. Se precisar de SQL cru: `text("... WHERE nome = :nome")` com `params`/`bindparams`, nunca interpolando.
3. Identificadores dinamicos (ordenacao, coluna): allowlist fixa no codigo mapeando o valor recebido para a coluna.
4. Usuario do banco com o minimo de privilegio (defesa em profundidade).

**Como testar:** enviar `' OR '1'='1` e `'; --` nos campos e filtros; procurar por `text(f"` e `text("...%` no codigo (grep).

## Evidencia

Documentacao do `text()` confirma o uso de parametros nomeados (`:nome`, `bindparams`); cheat sheet OWASP consultado em 2026-09-30.

## Links confiaveis

- [CWE-89 (MITRE)](https://cwe.mitre.org/data/definitions/89.html): definicao oficial.
- [SQL Injection Prevention Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html): consultas parametrizadas e allowlist para identificadores.
- [SQLAlchemy text()](https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.text): como vincular parametros em SQL cru.

## Por que e reaproveitavel

Qualquer projeto com SQLAlchemy; item fixo do checklist de revisao.

## Relacionadas no Brain

- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario
