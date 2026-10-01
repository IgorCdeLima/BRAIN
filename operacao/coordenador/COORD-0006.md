---
tipo: pedido-coordenador
id: COORD-0006
status: escalado
atendido_em: 2026-09-30
adm: ADM-0013
urgencia: bloqueante
pedido_por: dev
tarefa: T-0007
criado: 2026-09-30
tags: [lab, T-0007, git, merge]
---
# COORD-0006 - Rodar `git merge main` no worktree da T-0007 (negado ao Dev)

## Pedido

- [x] Rodar o merge abaixo (ou autorizar o Dev a rodar):

  - Pasta: `/home/igor/orca/workspaces/lab/T-0007-cabecalhos-http`
  - Comando: `git merge main --no-edit` -> ADM-0013

## Motivo

- O cartao T-0007 esta em `correcao`. O Revisor (passo 2 da secao Revisao) pediu ao Dev que faca `git merge main` no worktree para resolver o conflito de `docs/requisitos/requisitos.md` (RNF-08 da T-0006 na `main` x notas da T-0007).
- O Dev tentou o comando duas vezes e o ambiente negou a permissao. A regra do Dev tambem proibe merge. O Dev nao contornou o bloqueio.
- Ha um conflito entre o pedido do Revisor (Dev faz o merge) e o perfil do Dev (nao faz merge). Decisao necessaria: o Coordenador/Administrador roda o merge, ou libera `git merge` so para este caso.

## Depois do merge (Dev)

1. Resolver `docs/requisitos/requisitos.md` com uma unica definicao do RNF-08 + notas da T-0007 (incluindo 500/SEC-0006).
2. Rodar `docker compose run --build --rm test` e `docker compose run --build --rm lint`.
3. Registrar o hash do merge na Entrega e mudar o status do cartao para `revisao`.

Obs.: o pedido tambem esta no cartao T-0007, secao "Pedidos ao Coordenador". Se houver conflito em `qualidade/`, o Dev para e avisa no cartao.

---

## Atendimento

Coordenador, 2026-09-30: o pedido procede. O erro foi do plano do Coordenador, que mandou o Dev fazer o merge sem conferir o perfil dele. Simulacao: depois da renumeracao dos VER (`786b9ee`), so o `docs/requisitos/requisitos.md` da conflito. Decisao do humano: escalar ao Administrador -> ADM-0013. Ele inicia o merge e deixa o conflito para o Dev.
