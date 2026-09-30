---
tipo: padrao
status: rascunho
origem: SEARCH-0001 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0001
confianca: baixa
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#10)
criado: 2026-09-30
decisao: promovido
revisar_em: 2026-12-30
tags: [seguranca, cwe, cwe-94, code-injection, ssti]
---
# CWE-94 code injection se evita sem eval, exec e templates montados com entrada do usuario

## Contexto

**O que e:** entrada do usuario vira codigo que a propria aplicacao executa.

**Como aparece na nossa stack:**
- `eval()`, `exec()`, `compile()` sobre texto vindo de fora (calculadoras, filtros "dinamicos").
- **SSTI**: `Template(texto_do_usuario).render()` ou `env.from_string(entrada)` no Jinja2: quem controla o template executa expressoes no servidor.
- `importlib`/`getattr` com nome de modulo/atributo vindo do usuario.
- Deserializacao insegura (ver [[CWE-502 deserializacao de dado nao confiavel se evita com JSON em vez de pickle]]).

## Solucao

**Controle:**
1. Nunca `eval/exec` em entrada; usar parser especifico (`ast.literal_eval` para literais, biblioteca de expressoes segura, ou tabela de operacoes permitidas).
2. Templates ficam em arquivos do projeto; o usuario so fornece **dados** para o `render`, nunca o texto do template.
3. Mapear nomes recebidos para funcoes por allowlist (dicionario), nao por `getattr` livre.

**Como testar:** grep por `eval(`, `exec(`, `from_string(`, `Template(`; enviar `{{7*7}}` em campos que aparecem em templates e conferir que sai literal (nao `49`).

## Evidencia

Definicao MITRE e cheat sheet de prevencao de injecao (OWASP) apontados no indice de cheat sheets, consultados em 2026-09-30. Detalhes de SSTI nao verificados em fonte primaria dedicada: tratar como pista.

## Links confiaveis

- [CWE-94 (MITRE)](https://cwe.mitre.org/data/definitions/94.html): definicao oficial.
- [Injection Prevention Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html): principios gerais contra injecao.

## Por que e reaproveitavel

Revisao de qualquer recurso "dinamico" (filtros, formulas, previews de template).

## Relacionadas no Brain

- [[CWE-78 command injection se evita com subprocess em lista e sem shell]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido como **rascunho, confianca baixa** (2026-09-30): SSTI sem fonte primaria dedicada (declarado no SEARCH-0001). Confirmar antes de tratar como regra. Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
