---
tipo: problema-solucao
status: ativo
origem: T-0007 (Dev), curado pelo Bibliotecario
tarefa: T-0007
confianca: alta
fontes: ["https://starlette.dev/middleware/", "projetos/lab: tests/test_cabecalhos.py (8 casos)"]
verificado_em: 2026-09-30
valido_para: "FastAPI/Starlette da imagem do lab (Python 3.13)"
revisar_em: 2027-03-30
criado: 2026-09-30
decisao: promovido
tags: [seguranca, cabecalhos, fastapi, starlette, middleware]
---
# FastAPI add_middleware com middleware ASGI puro cobre respostas de erro de outros middlewares

## Sintoma

Duvida ao colocar cabecalhos de seguranca em todas as respostas: o middleware alcanca tambem as respostas 411/413 geradas por outro middleware, e nao duplica cabecalho que a rota ja enviou?

## Ambiente

FastAPI/Starlette da imagem do lab (Python 3.13). Middleware ASGI puro que usa `MutableHeaders(scope=msg)` em `http.response.start`.

## Causa raiz

A ordem da pilha: o **ultimo** middleware adicionado com `app.add_middleware` fica o **mais externo**. Registrado depois de um `@app.middleware("http")` que responde 411/413, ele enxerga essas respostas.

## Solucao

- Registrar o middleware de cabecalhos **depois** dos demais (fica por fora).
- Usar atribuicao (`cab[nome] = valor`), nao `append`: substitui e evita cabecalho duplicado (ex.: `X-Content-Type-Options` que a rota ja enviava).
- Cobre 404, 405, 422, 303 e `FileResponse`.
- Nao cobre o 500 de excecao nao tratada: ver [[Middleware do FastAPI nao cobre a resposta 500 do ServerErrorMiddleware]].
- Com `default-src 'self'` e CSS em `<style>` inline e preciso `style-src 'self' 'unsafe-inline'` (ver [[CSP default-src self bloqueia o style inline dos templates]]).

## Como verificar que foi resolvido

Testes automaticos (`tests/test_cabecalhos.py`, 8 casos) e `curl -I` em rota normal, em 404 e em 411/413; `get_list` do cabecalho deve ter 1 item.

## O que nao funcionou

Nao verificado no navegador (extensao indisponivel na sessao): violacao de CSP no console.

## Origem

T-0007 do lab (Dev). Fonte: [Starlette: middleware](https://starlette.dev/middleware/).

## Links confiaveis

- [Starlette: middleware](https://starlette.dev/middleware/)

## Relacionadas no Brain

- [[CWE-1021 clickjacking se evita com CSP frame-ancestors e X-Frame-Options em middleware do Starlette]]: o padrao que este teste confirma para `add_middleware`.

## Decisao do Bibliotecario

Promovido a `10_Conhecimento` (2026-09-30): testado na T-0007 com testes automaticos e curl, sem duplicata no Brain. Item de navegador segue como lacuna declarada.
