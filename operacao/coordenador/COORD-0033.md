---
tipo: pedido-coordenador
id: COORD-0033
status: escalado
urgencia: nao-bloqueante
pedido_por: engenheiro
tarefa: T-0018
criado: 2026-10-05
atendido_em: 2026-10-05
adm: ADM-0029
tags: [ambiente, regras, internet, pesquisador, leitura, lancador, adr-0017, adm-0009]
---
# COORD-0033 - Mudancas de regra do ambiente decididas pelo humano na T-0018: internet so pelo Pesquisador e leitura limitada a propria tarefa

## Pedido

Escalar ao Administrador (area N4: regras, `agentes/`, `ferramentas/papel.py`), para ADR do ambiente com aprovacao do humano. Nao ha comando a rodar agora; o pedido e de mudanca de regra.

- [ ] 1. **Internet so pelo Pesquisador** (RF-32 do projeto `ambiente`). Decisao do humano, 2026-10-05: "Qualquer outro agente, incluindo o administrador, tem que realizar uma requisicao ao pesquisador procurar na internet por ele. Fora isso, os outros agentes ficam sim limitados a agencia que mantem a IA e ferramentas do git." Muda o item 2 da [[ADR-0017 Papel Pesquisador e internet por fontes confiaveis]] (hoje o lancador libera `WebFetch` nos dominios de `agentes/fontes-confiaveis.json` para todos os papeis) e vale tambem para o Administrador. Pontos que o ADR novo precisa resolver (premissa P12 dos requisitos): `pip-audit`/`osv-scanner` da Seguranca consultam `osv.dev` (ADR-0017 item 5); o Designer abre a aplicacao em `localhost`; o que fazer com `agentes/fontes-confiaveis.json` (passa a ser so a lista de partida do Pesquisador?).
- [ ] 2. **Leitura limitada a propria tarefa** (RF-33). Decisao do humano: "Cada agente em cada worktree/tarefa tem que saber apenas da propria tarefa e do que o BRAIN disponibiliza." Proposta do Engenheiro: o lancador `papel` gera, para papeis de worktree, regras `Read` negadas e `sandbox.filesystem.denyRead` para outros worktrees, outros projetos, cartoes de outras tarefas e `logs/`, deixando o proprio worktree, o proprio cartao, `BRAIN/`, as regras e os canais de pedido (premissa P11: listar `operacao/coordenador` e `operacao/pesquisas` para numerar os proprios pedidos). Papeis da copia principal sem mudanca.
- [ ] 3. (Condicional) Se as regras do sandbox (RF-26: `sandbox.enabled`, `failIfUnavailable`, `allowUnsandboxedCommands: false`, rede por papel de RF-31) nao puderem ficar em managed settings na imagem do container (`SEARCH-0010` item 1), coloca-las nos perfis dos papeis em `agentes/perfis/`. Rede: Pesquisador aberta; demais so `github.com` e `localhost`.

Implementacao so depois do ADR aceito; o teste fica no roteiro da T-0020 (RF-31 a RF-33). Enquanto isso, as regras atuais continuam valendo.

## Motivo

Premissas P11 e P12 confirmadas pelo humano em 2026-10-05 (commit `9bf11c3`). Respostas do humano as questoes Q4 e Q10 da T-0018 (registradas em `projetos/ambiente/docs/requisitos/requisitos.md`, commit `3612576`, e no `ADR-0001` proposto). O Engenheiro nao altera regras, `agentes/` nem `ferramentas/` (N4); so o Administrador, com aprovacao do humano a cada mudanca.

---

## Atendimento

Coordenador, 2026-10-05, com aprovacao do humano: mudanca de regra em area N4 -> escalado ao ADM-0029, com os itens 1 a 3. Fecha quando o ADM-0029 concluir.
