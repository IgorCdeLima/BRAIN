---
tipo: padrao
status: ativo
origem: SEARCH-0001 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org, fastapi.tiangolo.com]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#20)
criado: 2026-09-30
decisao: promovido
revisar_em: 2027-03-30
tags: [seguranca, cwe, cwe-200, cwe-209, erros, logs]
---
# CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace

## Contexto

**O que e:** a aplicacao entrega dado sensivel a quem nao devia: stack trace, caminho de arquivo, versao, SQL, segredo, dado de outro usuario (CWE-200; o caso de mensagem de erro e o CWE-209).

**Como aparece na nossa stack:**
- Modo debug ligado (`debug=True`, `uvicorn --reload` em producao) devolvendo traceback.
- `HTTPException(detail=str(e))` repassando o texto da excecao (mensagem do driver do PostgreSQL com nome de tabela).
- Respostas de API devolvendo o objeto inteiro do ORM (campos internos como `senha_hash`) em vez de um `response_model` enxuto.
- Log/erro contendo token ou senha; `/docs` aberto sem necessidade; cabecalho `Server` com versao.

## Solucao

**Controle:**
1. Handler global de `Exception` que devolve mensagem generica e um id de correlacao, e registra o detalhe so no log do servidor.
2. `response_model` explicito (allowlist de campos) em toda rota.
3. Debug desligado fora do desenvolvimento; desativar `/docs` em producao se nao for publico.
4. Nunca logar segredos (regra global 4 do ambiente).

**Como testar:** provocar erro (id invalido, JSON quebrado, banco fora) e checar que a resposta nao traz traceback, caminho, SQL nem versao.

## Evidencia

Cheat sheet OWASP de tratamento de erros consultado em 2026-09-30: handler global, nada de stack trace/caminhos/versoes ao cliente, mensagem generica, detalhe no log.

## Links confiaveis

- [CWE-200 (MITRE)](https://cwe.mitre.org/data/definitions/200.html): definicao oficial.
- [Error Handling Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html): handler global e mensagens genericas.
- [FastAPI - Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/): exception handlers no FastAPI.

## Por que e reaproveitavel

Ajuda em revisao de qualquer API e na escrita de logs.

## Relacionadas no Brain

- [[CWE-20 entrada extrema gerando erro 500 se evita validando com Pydantic e handler global]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido (2026-09-30) como padrao ativo: cheat sheet OWASP de erros lido pelo Pesquisador; sem duplicata no Brain. Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
