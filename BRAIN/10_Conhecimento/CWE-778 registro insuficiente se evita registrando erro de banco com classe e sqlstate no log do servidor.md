---
tipo: padrao
status: ativo
origem: SEARCH-0008 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0008
tarefa: T-0013
confianca: media
fontes: [https://cwe.mitre.org/data/definitions/778.html, https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html]
verificado_em: 2026-10-04
valido_para: CWE 4.20 (pagina de 2026-04-30)
criado: 2026-10-04
decisao: promovido
revisar_em: 2027-04-04
tags: [seguranca, cwe, cwe-778, logs, fastapi, sqlalchemy]
---
# CWE-778 registro insuficiente se evita registrando erro de banco com classe e sqlstate no log do servidor

## Contexto

**O que e:** evento relevante para seguranca ocorre e o produto nao o registra, ou registra sem os detalhes que permitiriam investigar depois.

**Como aparece na nossa stack (FastAPI + SQLAlchemy 2 + uvicorn):** `except SQLAlchemyError` que devolve 503 generico ao cliente e **nao escreve nada no log**. O cliente nao ve o erro (correto, ver [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]]), mas o operador tambem nao: queda de banco, tabela travada ou ataque que force erro passam em silencio.

## Solucao

**Controle:** todo handler que traduz excecao em resposta generica registra antes, no servidor, com `logger.error` (ou `logger.exception` quando o traceback for filtrado):

- classe da excecao (`type(erro).__name__`) e, para erro de banco, o `sqlstate` (receita em [[SQLAlchemyError no log: registrar classe e sqlstate, nunca str(erro) inteiro]]);
- rota/metodo e um id de correlacao, se houver;
- nunca senha, token, PII nem string de conexao (lista de exclusao do OWASP).

**Como testar:** provocar a falha (parar o banco ou travar a tabela), chamar a rota e conferir com `caplog` (pytest) que: a resposta e generica **e** existe registro de nivel ERROR com a classe/sqlstate **e** o registro nao contem o valor enviado pelo usuario.

## Trade-offs

- **Ganha:** falha de banco e ataque que force erro ficam visiveis ao operador.
- **Perde:** mais volume de log (pode pedir limite de taxa) e disciplina para nao registrar dado do usuario.

## Evidencia

MITRE descreve a fraqueza e a mitigacao (registrar sucessos e falhas relevantes, niveis de log adequados). OWASP lista erros de sistema e de conectividade como eventos a registrar e dados a nunca registrar. A aplicacao ao handler de SQLAlchemy e inferencia nossa a partir do SEC-T0013-01, ainda nao testada (por isso `confianca: media`).

## Links confiaveis

- [MITRE CWE-778](https://cwe.mitre.org/data/definitions/778.html): definicao e mitigacoes.
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html): quais eventos registrar e quais dados excluir.

## Quando NAO usar

Erro esperado e de alta frequencia (ex.: validacao de formulario) nao precisa de ERROR: registre em nivel menor ou conte em metrica, para nao afogar o log.

## Relacionadas

- [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]]: lado do cliente (resposta generica); esta nota cobre o lado do log.
- [[SQLAlchemyError no log: registrar classe e sqlstate, nunca str(erro) inteiro]]: receita concreta de codigo.
- [[Mapa das CWE relevantes para Python e FastAPI]]: indice das CWE.

## Decisao do Bibliotecario

Promovido a padrao em `10_Conhecimento` (2026-10-04), no formato das demais notas CWE; incluido no mapa. Sem duplicata (a CWE-200 cobre so o cliente). Fontes sao MITRE e OWASP, dominios confiaveis.
