---
tipo: problema-solucao
status: ativo
origem: T-0007 (Seguranca, SEC-0006 do lab), curado pelo Bibliotecario
tarefa: T-0007
confianca: alta
fontes: ["https://starlette.dev/middleware/", "projetos/lab: SEC-0006"]
verificado_em: 2026-09-30
valido_para: "Starlette 1.7.0 / FastAPI 0.141.1 (imagem do lab)"
revisar_em: 2027-03-30
criado: 2026-09-30
decisao: promovido
tags: [seguranca, cabecalhos, fastapi, starlette, middleware, armadilha]
---
# Middleware do FastAPI nao cobre a resposta 500 do ServerErrorMiddleware

## Sintoma

Com o banco parado, `GET /` voltou 500 **sem** os 4 cabecalhos de seguranca, enquanto `/health` (503 tratado) veio com todos.

## Ambiente

Starlette 1.7.0 / FastAPI 0.141.1 (imagem do lab).

## Causa raiz

O Starlette monta a pilha como `ServerErrorMiddleware` -> middlewares do usuario -> `ExceptionMiddleware`. O 500 de excecao nao tratada e gerado no mais externo, fora dos middlewares registrados com `app.add_middleware` ou `@app.middleware("http")`.

## Solucao

- `exception_handler(Exception)` e `exception_handler(500)` **nao** resolvem: o Starlette instala esse handler no proprio `ServerErrorMiddleware`.
- Envolver o app por fora: um objeto ASGI `Envoltorio(app)` entregue ao uvicorn. O `ServerErrorMiddleware` envia o 500 pelo `send` e so depois relanca a excecao, entao o envoltorio ve o `http.response.start` e pode por os cabecalhos.

## Como verificar que foi resolvido

`TestClient(app, raise_server_exceptions=False)` numa rota que levanta excecao, ou, na app rodando, parar o banco e fazer `GET /`; conferir os cabecalhos no 500.

## O que nao funcionou

Handler global de excecao e middleware comum (ver Solucao).

## Origem

Revisao de seguranca da T-0007 (SEC-0006 do lab). Ordem da pilha conferida com `inspect.getsource(Starlette.build_middleware_stack)` na imagem. Qualquer controle por middleware (cabecalhos, id de correlacao, CORS) tem essa lacuna no 500.

## Links confiaveis

- [Starlette: middleware](https://starlette.dev/middleware/): `ServerErrorMiddleware` e `ExceptionMiddleware` sempre presentes nas pontas da pilha.

## Relacionadas no Brain

- [[FastAPI add_middleware com middleware ASGI puro cobre respostas de erro de outros middlewares]]: cobre 404/405/411/413/422, mas nao o 500.
- [[CWE-1021 clickjacking se evita com CSP frame-ancestors e X-Frame-Options em middleware do Starlette]]: os cabecalhos que faltam no 500.
- [[CWE-200 vazamento de informacao se evita com handler global de erros sem stack trace]]: o handler global nao resolve os cabecalhos no 500.

## Decisao do Bibliotecario

Promovido a `10_Conhecimento` (2026-09-30): reproduzido pela Seguranca com evidencia e leitura do codigo da pilha; sem duplicata.
