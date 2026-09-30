---
tipo: padrao
status: rascunho
origem: SEARCH-0001 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0001
confianca: baixa
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#22)
criado: 2026-09-30
decisao: promovido
revisar_em: 2026-12-30
tags: [seguranca, cwe, cwe-918, ssrf, docker]
---
# CWE-918 SSRF se evita com allowlist de destinos e bloqueio de enderecos internos

## Contexto

**O que e:** o servidor faz uma requisicao para uma URL escolhida pelo usuario, que pode apontar para servicos internos (`http://db:5432`, `http://169.254.169.254/` metadados de nuvem, `localhost`).

**Como aparece na nossa stack:**
- Recurso "importar por URL", preview de link, webhook configuravel, download de imagem remota com `httpx`/`requests`.
- Rodando em Docker/compose, os outros containers (banco, admin) ficam alcancaveis pelo nome do servico.
- Redirecionamentos seguidos para destino interno; DNS que resolve para IP interno.

## Solucao

**Controle:**
1. Melhor: nao aceitar URL; usar identificador que o servidor mapeia.
2. Allowlist de dominios/esquemas (`https` apenas) e porta.
3. Resolver o DNS e bloquear IPs privados, loopback e link-local antes de conectar; nao seguir redirect automaticamente (ou revalidar).
4. Rede do container sem acesso ao que nao precisa (segmentar redes no compose).

**Como testar:** informar `http://localhost`, `http://127.0.0.1:porta`, `http://[::1]`, `http://169.254.169.254`, nome de servico do compose e uma URL que redireciona para eles.

## Evidencia

Cheat sheet de prevencao de SSRF da OWASP consta no indice de cheat sheets (consultado em 2026-09-30); resumo acima segue o consenso geral, sem ter aberto o texto completo. Tratar como pista.

## Links confiaveis

- [CWE-918 (MITRE)](https://cwe.mitre.org/data/definitions/918.html): definicao oficial.
- [SSRF Prevention Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html): allowlist, validacao de IP e cenarios.

## Por que e reaproveitavel

Assim que qualquer recurso buscar URL fornecida de fora.

## Relacionadas no Brain

- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario

Promovido como **rascunho, confianca baixa** (2026-09-30): o proprio Pesquisador marcou como pista (texto completo nao lido). Confirmar nos links antes de tratar como regra. Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
