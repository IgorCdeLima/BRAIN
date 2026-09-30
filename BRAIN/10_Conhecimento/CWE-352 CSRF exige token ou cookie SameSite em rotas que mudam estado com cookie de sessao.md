---
tipo: padrao
status: rascunho
origem: SEARCH-0001 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0001
confianca: baixa
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#3)
criado: 2026-09-30
decisao: promovido
revisar_em: 2026-12-30
tags: [seguranca, cwe, cwe-352, csrf]
---
# CWE-352 CSRF exige token ou cookie SameSite em rotas que mudam estado com cookie de sessao

## Contexto

**O que e:** um site de terceiro faz o navegador do usuario logado enviar uma requisicao que muda estado (POST/PUT/DELETE) e o servidor a aceita porque o cookie vai junto. 3o lugar no CWE Top 25 de 2025.

**Como aparece na nossa stack:**
- Formularios Jinja2 (upload, exclusao) autenticados por **cookie de sessao** sem token anti-CSRF: o FastAPI/Starlette nao traz protecao CSRF embutida.
- Rotas GET que alteram estado.
- Nao se aplica quando a autenticacao e por cabecalho `Authorization: Bearer` enviado por JS (o navegador nao o anexa sozinho).

## Solucao

**Controle:**
1. Token anti-CSRF por sessao (padrao sincronizador) em todo formulario que muda estado, validado no servidor.
2. Cookie de sessao com `SameSite=Lax` (ou `Strict`), `HttpOnly`, `Secure`.
3. Nunca alterar estado em GET.
4. Verificar `Origin`/`Referer` como camada extra.

**Como testar:** repetir o POST de outro origin (pagina HTML de teste) sem o token e conferir que e recusado (403).

## Evidencia

Cheat sheet OWASP consultado em 2026-09-30 (mapeado ao A01 Broken Access Control no indice de cheat sheets).

## Links confiaveis

- [CWE-352 (MITRE)](https://cwe.mitre.org/data/definitions/352.html): definicao oficial.
- [CSRF Prevention Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html): padrao sincronizador, SameSite, verificacao de Origin.

## Por que e reaproveitavel

Toda tela com login por cookie; decisao de arquitetura (cookie vs bearer) afeta o risco.

## Relacionadas no Brain

- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido como **rascunho, confianca baixa** (2026-09-30): o Pesquisador apoiou-se so no indice de cheat sheets, sem ler o texto completo. Antes de tratar como regra, abrir o cheat sheet linkado e confirmar. Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
