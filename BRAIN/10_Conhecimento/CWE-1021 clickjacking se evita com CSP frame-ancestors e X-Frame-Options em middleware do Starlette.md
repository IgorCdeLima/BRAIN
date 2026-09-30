---
tipo: padrao
status: rascunho
origem: SEARCH-0002 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0005
pesquisa: SEARCH-0002
confianca: media
fontes: ["https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html", "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html", "https://starlette.dev/middleware/"]
verificado_em: 2026-09-30
valido_para: Starlette/FastAPI atuais
criado: 2026-09-30
decisao: promovido
revisar_em: 2026-12-30
tags: [seguranca, cwe, cwe-1021, clickjacking, cabecalhos, starlette]
---
# CWE-1021 clickjacking se evita com CSP frame-ancestors e X-Frame-Options em middleware do Starlette

## Contexto

Clickjacking (CWE-1021): a pagina da app e embutida em iframe de outro site para enganar o clique do usuario. O controle e enviar cabecalhos HTTP que proibam o embutimento.

## Solucao

**Cabecalhos minimos (OWASP):**
- `Content-Security-Policy: frame-ancestors 'none'` (ou `'self'` se a propria app usa iframe). E o controle moderno e tem prioridade sobre o X-Frame-Options.
- `X-Frame-Options: DENY` por compatibilidade.
- `X-Content-Type-Options: nosniff`.
- `Referrer-Policy: strict-origin-when-cross-origin` (opcional).
Precisam ser cabecalhos HTTP; `<meta>` nao vale. `ALLOW-FROM` e obsoleto.

**Middleware ASGI puro (padrao da doc do Starlette):**
```python
from starlette.datastructures import MutableHeaders
class HeadersSeguranca:
    def __init__(self, app, headers): self.app, self.headers = app, headers
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        async def send2(msg):
            if msg["type"] == "http.response.start":
                h = MutableHeaders(scope=msg)
                for k, v in self.headers: h.append(k, v)
            await send(msg)
        await self.app(scope, receive, send2)
```
Registrar com `app.add_middleware(HeadersSeguranca, headers=[...])` (FastAPI) ou `Middleware(...)` no Starlette.

**Como testar:** `curl -I` em rota HTML e em resposta de erro (404/500) e conferir os cabecalhos; pagina de teste com `<iframe>` para a app deve ser bloqueada.

## Evidencia

Cheat sheets lidos em 2026-09-30. O trecho de codigo vem da doc do Starlette; o `add_middleware` do FastAPI nao foi conferido numa fonte aqui, testar.

## Links confiaveis

- [OWASP Clickjacking Defense](https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html): frame-ancestors x X-Frame-Options.
- [OWASP HTTP Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html): valores recomendados dos demais cabecalhos.
- [Starlette: middleware](https://starlette.dev/middleware/): middleware ASGI puro que altera cabecalhos.

## Por que e reaproveitavel

Todo app web do ambiente que sirva HTML.

## Relacionadas no Brain

- [[CWE-352 CSRF exige token ou cookie SameSite em rotas que mudam estado com cookie de sessao]]

## Decisao do Bibliotecario

Promovido como **rascunho** (2026-09-30): cheat sheets OWASP e doc do Starlette lidos, mas o `add_middleware` do FastAPI nao foi conferido em fonte (limite declarado no SEARCH-0002). Ao testar no lab, mudar para `status: ativo`. Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
