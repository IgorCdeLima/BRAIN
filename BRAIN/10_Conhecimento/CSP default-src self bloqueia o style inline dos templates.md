---
tipo: problema-solucao
status: rascunho
origem: T-0006 (Engenheiro), curado pelo Bibliotecario
tarefa: T-0006
confianca: media
fontes: ["https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/style-src"]
verificado_em: 2026-09-30
valido_para: "CSP nos navegadores atuais; templates Jinja2 com <style> no HTML"
revisar_em: 2026-12-30
criado: 2026-09-30
decisao: promovido
tags: [seguranca, csp, cabecalhos, armadilha, modelagem]
---
# CSP default-src self bloqueia o style inline dos templates

## Sintoma

Com `Content-Security-Policy: default-src 'self'; frame-ancestors 'none'`, a pagina perde o layout quando o CSS esta num `<style>` inline. Nenhum teste automatico que so confere cabecalhos percebe.

## Ambiente

Navegadores atuais; app com HTML renderizado no servidor (Jinja2) e CSS em `<style>` no template (`index.html` do lab).

## Causa raiz

Sem `style-src` explicito, `default-src` serve de fallback para estilos. Sem `'unsafe-inline'`, nonce ou hash, o `<style>` inline e bloqueado (MDN, `style-src`).

## Solucao

- Antes de fixar a CSP, conferir se o template tem `<style>`, `style=` ou `<script>` inline.
- Escolher: `style-src 'self' 'unsafe-inline'` (risco pequeno, so estilo), ou mover o CSS para arquivo servido pela app, ou usar nonce/hash.
- No lab, a T-0007 usa `'unsafe-inline'` so em `style-src`, como premissa, ate o CSS ir para arquivo.

## Como verificar que foi resolvido

Criterio de aceite no navegador: "estilo aplicado e nenhuma violacao de CSP no console". A T-0007 nao conseguiu conferir no navegador (extensao indisponivel): **ainda nao testado no navegador**.

## O que nao funcionou

`default-src 'self'` sozinho (recomendacao original do SEC-0005).

## Origem

Modelagem da T-0006 (Engenheiro), a partir do SEC-0005 e da leitura do template do lab.

## Links confiaveis

- [MDN: CSP style-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/style-src): bloqueio de estilo inline e fallback de `default-src`.

## Relacionadas no Brain

- [[CWE-1021 clickjacking se evita com CSP frame-ancestors e X-Frame-Options em middleware do Starlette]]: a CSP que motivou a armadilha.
- [[CWE-79 XSS exige autoescape do Jinja2 ligado e nunca usar safe em dado do usuario]]: a CSP tambem e defesa em profundidade contra XSS.
- [[FastAPI add_middleware com middleware ASGI puro cobre respostas de erro de outros middlewares]]: onde a CSP e aplicada no lab.

## Decisao do Bibliotecario

Promovido como **rascunho** (2026-09-30): fonte primaria (MDN) confere, mas falta teste no navegador. Mudar para `ativo` quando alguem ver o estilo aplicado sem violacao no console.
