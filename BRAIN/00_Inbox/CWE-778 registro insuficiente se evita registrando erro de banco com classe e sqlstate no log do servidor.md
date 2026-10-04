---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0013
pesquisa: SEARCH-0008
confianca: media
fontes: [https://cwe.mitre.org/data/definitions/778.html, https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html]
verificado_em: 2026-10-04
valido_para: CWE 4.20 (pagina de 2026-04-30)
criado: 2026-10-04
decisao:
tags: [seguranca, cwe-778, logs, fastapi, sqlalchemy]
---
# CWE-778 registro insuficiente se evita registrando erro de banco com classe e sqlstate no log do servidor

## Conteudo proposto

**O que e:** evento relevante para seguranca ocorre e o produto nao o registra, ou registra sem os detalhes que permitiriam investigar depois.

**Como aparece na nossa stack (FastAPI + SQLAlchemy 2 + uvicorn):** `except SQLAlchemyError` que devolve 503 generico ao cliente e **nao escreve nada no log**. O cliente nao ve o erro (bom, ver [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]]), mas o operador tambem nao: queda de banco, tabela travada ou ataque que force erro passam em silencio.

**Controle:** todo handler que traduz excecao em resposta generica registra antes, no servidor, com `logger.error`/`logger.exception` conforme o caso:
- classe da excecao (`type(erro).__name__`) e, para erro de banco, o `sqlstate` (ver [[SQLAlchemyError no log: registrar classe e sqlstate, nunca str(erro) inteiro]]);
- rota/metodo e um id de correlacao, se houver;
- sem senha, token, PII, string de conexao (lista de exclusao do OWASP).

**Como testar:** provocar a falha (parar o banco ou travar a tabela), chamar a rota e conferir com `caplog` (pytest) que: resposta e generica E existe um registro de nivel ERROR com a classe/sqlstate E o registro nao contem o valor enviado pelo usuario.

## Evidencia

MITRE descreve a fraqueza e a mitigacao (registrar sucessos e falhas relevantes, niveis de log adequados em producao). OWASP lista erros de sistema e de conectividade como eventos a registrar e dados a nunca registrar. A aplicacao ao handler de SQLAlchemy e inferencia nossa a partir do SEC-T0013-01, ainda nao testada.

## Links confiaveis

- [MITRE CWE-778](https://cwe.mitre.org/data/definitions/778.html): definicao e mitigacoes.
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html): quais eventos registrar e quais dados excluir.

## Por que e reaproveitavel

Qualquer handler global de erro em projetos FastAPI do lab: generico para fora, registrado para dentro.

## Relacionadas no Brain

- [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]]

## Decisao do Bibliotecario

