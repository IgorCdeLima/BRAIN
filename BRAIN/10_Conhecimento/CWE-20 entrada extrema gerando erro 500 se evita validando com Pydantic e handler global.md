---
tipo: padrao
status: ativo
origem: SEARCH-0001 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org, fastapi.tiangolo.com]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#18); FastAPI atual
criado: 2026-09-30
decisao: promovido
revisar_em: 2027-03-30
tags: [seguranca, cwe, cwe-20, cwe-209, validacao, erro-500]
---
# CWE-20 entrada extrema gerando erro 500 se evita validando com Pydantic e handler global

## Contexto

**O que e:** a entrada nao e validada (tipo, tamanho, faixa, formato) e o valor inesperado quebra o codigo ou passa adiante (CWE-20 Improper Input Validation). O erro 500 que expoe detalhes tambem e vazamento (ver [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]]).

**Como aparece na nossa stack:**
- Parametros de rota/query anotados como `str` sem limite, ou `dict`/`Any`.
- Numero enorme, negativo ou zero onde se espera positivo; texto com NUL, emoji, Unicode estranho; string vazia.
- Conversao manual (`int(x)`) sem tratar excecao, gerando 500.
- Validar so no front-end.

## Solucao

**Controle:**
1. Modelos Pydantic e `Query/Path/Field` com restricoes (`max_length`, `ge`, `le`, `pattern`, `Literal`/`Enum`).
2. Allowlist (definir o que e valido), sempre no servidor.
3. Validacao sintatica (formato) e semantica (regra de negocio).
4. Handler global (`@app.exception_handler(Exception)` e para `RequestValidationError`) devolvendo 4xx/500 generico e registrando o detalhe no log.

**Como testar:** fuzz simples: string de 1 MB, `-1`, `0`, `9999999999999999999`, `null`, tipo trocado, `\u0000`, JSON invalido; nenhuma resposta pode ser 500 com traceback.

## Evidencia

Cheat sheet de validacao de entrada (OWASP) e pagina de tratamento de erros do FastAPI consultados em 2026-09-30. Caso ja visto no lab (entrada extrema gerando 500).

## Links confiaveis

- [CWE-20 (MITRE)](https://cwe.mitre.org/data/definitions/20.html): definicao oficial.
- [Input Validation Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html): allowlist, validacao no servidor, sintatica e semantica.
- [FastAPI - Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/): como registrar handlers para `RequestValidationError` e excecoes.

## Por que e reaproveitavel

Base de quase todas as outras CWE de injecao; todo endpoint novo.

## Relacionadas no Brain

- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-09-30) como padrao ativo: fonte primaria (OWASP, FastAPI) lida pelo Pesquisador; sem duplicata no Brain. Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
