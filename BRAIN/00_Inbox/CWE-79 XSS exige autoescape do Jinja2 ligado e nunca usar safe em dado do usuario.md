---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/pesquisador
tarefa: pauta
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org, jinja.palletsprojects.com]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#1); Jinja2 3.x
criado: 2026-09-30
decisao:
tags: [seguranca, cwe, cwe-79, xss, jinja2]
---
# CWE-79 XSS exige autoescape do Jinja2 ligado e nunca usar safe em dado do usuario

## Conteudo proposto

**O que e:** dado controlado pelo usuario chega ao HTML sem ser codificado e o navegador o executa como script (Cross-site Scripting). Ficou em 1o lugar no CWE Top 25 de 2025.

**Como aparece na nossa stack:**
- `Environment` do Jinja2 criado sem autoescape (na API do Jinja2 o autoescape nao vem ligado por padrao; conferir se o `Jinja2Templates` do Starlette o liga na versao usada).
- Uso de `{{ campo|safe }}`, `Markup(...)` ou `{% autoescape false %}` com dado vindo do usuario (ex.: nome de arquivo enviado no upload, mostrado na listagem).
- Montar HTML por f-string e devolver `HTMLResponse`.
- Inserir dado em contexto de script/atributo sem aspas: autoescape de HTML nao basta em `<script>` nem em `href="javascript:..."`.

**Controle:**
1. Autoescape ligado para `.html` (`select_autoescape`), sem excecao.
2. `|safe` so em conteudo gerado por nos, nunca em entrada do usuario.
3. Dado em JS: passar por `|tojson`, nao por concatenacao.
4. Defesa em profundidade: cabecalho `Content-Security-Policy` restritivo.

**Como testar:** enviar `"><script>alert(1)</script>` e `<img src=x onerror=alert(1)>` em todo campo/nome de arquivo e ver se aparece codificado (`&lt;`) no HTML devolvido.

## Evidencia

Definicao MITRE e cheat sheet OWASP consultados em 2026-09-30; comportamento de autoescape do Jinja2 confirmado na documentacao da API (nao e padrao no `Environment`).

## Links confiaveis

- [CWE-79 (MITRE)](https://cwe.mitre.org/data/definitions/79.html): definicao oficial e exemplos.
- [XSS Prevention Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html): regras de codificacao por contexto (HTML, atributo, JS, URL).
- [Jinja2 API - Autoescaping](https://jinja.palletsprojects.com/en/stable/api/#autoescaping): `select_autoescape`, `|safe`, `Markup`.

## Por que e reaproveitavel

Todo projeto com paginas renderizadas por Jinja2 (revisao do Dev, checklist da Seguranca).

## Relacionadas no Brain

- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario
