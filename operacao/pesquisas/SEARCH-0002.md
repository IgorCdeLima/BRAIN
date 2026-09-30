---
tipo: pesquisa
id: SEARCH-0002
status: respondida
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0005
criado: 2026-09-30
pesquisado_por: pesquisador
pesquisado_em: 2026-09-30
catalogado_em:
notas: []
tags: [seguranca, cwe, dependencias, docker, supply-chain]
---
# SEARCH-0002 - CWE de dependencias, imagem e hardening (1395, 829, 250, 1021) para a stack do lab

## Pergunta

Para as CWE-1395 (dependencia vulneravel), CWE-829 (funcionalidade de origem nao confiavel: dependencias sem versao/hash), CWE-250 (container como root) e CWE-1021 (clickjacking / cabecalhos): qual e o controle recomendado na nossa stack (Python 3.13, FastAPI/Starlette, pip, Docker multi-estagio `python:3.13-slim`) e como testa-lo?

## Contexto

- A revisao de seguranca da T-0005 registrou SEC-0002 a SEC-0005 no lab, todos com severidade baixa. O Brain nao tem nota dessas CWEs, e o [[Mapa das CWE relevantes para Python e FastAPI]] nao as cobre.
- Pontos praticos a responder:
  - como travar dependencias com hash (`pip-compile --generate-hashes` ou `uv pip compile`) e auditar o arquivo travado com `pip-audit -r`;
  - como varrer a camada do sistema da imagem (`osv-scanner scan image`; alternativas) e o que fazer com CVE sem correcao;
  - `USER` sem privilegio com volume nomeado ja existente e com posse de root;
  - cabecalhos minimos (CSP `frame-ancestors`, `X-Frame-Options`, `nosniff`) via middleware do Starlette.
- Uma nota por CWE, no formato das existentes ("CWE-### ... se evita com ..."), com "como testar" e links confiaveis (MITRE CWE, OWASP Cheat Sheets: Docker Security, HTTP Headers, Clickjacking Defense).

## Ja buscado no Brain

- `grep` por CWE-1395, 1104, 829, 1357, 494, 250, 1021 e 693 em `BRAIN/` (inclusive `00_Inbox`): nada encontrado.
- Notas lidas: [[Fontes de referencia para analise de seguranca por CWE e dependencias]] (lista as fontes, nao os controles) e [[osv-scanner sobre requirements.txt acusa versao antiga de dependencia indireta]] (trata so o falso positivo).
- A definicao de cada CWE ja foi lida em cwe.mitre.org nesta revisao. Faltam os controles praticos da stack e a forma de testar.

---

## Resposta

<!-- Preenchido pelo Pesquisador. -->

- **Resumo (3 a 5 linhas):** Dependencia: travar com `pip-compile --generate-hashes`, instalar com `pip install --require-hashes` e auditar com `pip-audit --require-hashes -r` (so cobre Python; a imagem pede varredura a parte, ja em nota do Inbox). Container: `USER` sem privilegio (OWASP Docker, regra 2). Clickjacking: CSP `frame-ancestors 'none'` + `X-Frame-Options: DENY` + `nosniff`, via middleware ASGI do Starlette.
- **Notas geradas no Inbox:** [[CWE-1395 dependencia vulneravel se evita com auditoria do arquivo travado e da camada do sistema da imagem]], [[CWE-829 dependencia sem versao e sem hash se evita com requirements travado com hashes]], [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]], [[CWE-1021 clickjacking se evita com CSP frame-ancestors e X-Frame-Options em middleware do Starlette]]. Ja existiam (seguranca): [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]], [[ruff e pip-audit em Docker Compose com servicos lint e audit no estagio dev]].
- **Links confiaveis:** cwe.mitre.org (1395, 829, 250, 1021); cheatsheetseries.owasp.org (Docker Security, Clickjacking Defense, HTTP Headers); pip.pypa.io (secure installs); github.com/pypa/pip-audit; github.com/jazzband/pip-tools; starlette.dev/middleware.
- **Sem resposta / limites:** (1) `uv pip compile --generate-hashes` nao confirmado em fonte primaria (paginas lidas vieram truncadas); so pip-tools foi confirmado. (2) Volume nomeado ja existente com dono root: a doc do Docker nao trata; a nota traz pratica a testar. (3) `osv-scanner scan image` e alternativas nao pesquisados aqui; a nota do Inbox da Seguranca ja tem o uso testado no lab. (4) `add_middleware` do FastAPI nao conferido em fonte.
- **Conteudo suspeito descartado:** nenhum.

## Dominios propostos

- starlette.dev (doc oficial do Starlette; www.starlette.io nao resolveu). pip.pypa.io, cheatsheetseries.owasp.org e cwe.mitre.org ja devem estar na lista; conferir.

## Catalogacao
