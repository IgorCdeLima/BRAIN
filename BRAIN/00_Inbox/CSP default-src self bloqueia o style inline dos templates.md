---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/engenheiro
tarefa: T-0006
pesquisa:
confianca: media
fontes: ["https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/style-src"]
verificado_em: 2026-09-30
valido_para: "CSP nos navegadores atuais; templates Jinja2 com <style> no HTML"
criado: 2026-09-30
decisao:
tags: [seguranca, csp, cabecalhos, armadilha, modelagem]
---
# CSP default-src self bloqueia o style inline dos templates

## Conteudo proposto

**Armadilha de modelagem:** a recomendacao do SEC-0005 era `Content-Security-Policy: default-src 'self'; frame-ancestors 'none'`. O `index.html` do lab tem todo o CSS num `<style>` inline. Sem `style-src` explicito, `default-src 'self'` vale para estilos e o navegador **bloqueia** o `<style>` inline: a pagina perde o layout, e nenhum teste automatico (que so confere cabecalhos) percebe.

**Como tratar ao especificar:**

- Conferir se o template tem `<style>`/`style=` ou `<script>` inline antes de fixar a CSP.
- Ou permitir `style-src 'self' 'unsafe-inline'` (risco pequeno, so estilo), ou mover o CSS para arquivo servido pela app, ou usar nonce/hash.
- Criterio de aceite com o navegador: "estilo aplicado e nenhuma violacao de CSP no console".

No lab, a T-0007 usa `'unsafe-inline'` so em `style-src`, como premissa, ate o CSS ir para arquivo.

## Evidencia

MDN (`style-src`): sem `'unsafe-inline'`, nonce ou hash, `<style>` inline e bloqueado, e `default-src` serve de fallback para `style-src`. Leitura do `app/templates/index.html` do lab. Ainda nao testado no navegador (sera na T-0007).

## Links confiaveis

- [MDN: CSP style-src](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/style-src): bloqueio de estilo inline e fallback de `default-src`.

## Por que e reaproveitavel

Toda app com HTML renderizado no servidor que for ganhar CSP.

## Relacionadas no Brain

- [[CWE-1021 clickjacking se evita com CSP frame-ancestors e X-Frame-Options em middleware do Starlette]]
- [[CWE-79 XSS exige autoescape do Jinja2 ligado e nunca usar safe em dado do usuario]]

## Decisao do Bibliotecario
