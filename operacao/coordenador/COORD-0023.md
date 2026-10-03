---
tipo: pedido-coordenador
id: COORD-0023
status: concluido
urgencia: bloqueante
pedido_por: dev
tarefa: T-0015
criado: 2026-10-02
atendido_em: 2026-10-02
adm:
tags: [t-0015, worktree, branch-desatualizado]
---
# COORD-0023 - Branch da T-0015 desatualizado em relacao a main do lab

## Pedido

- [x] Atualizar o branch `T-0015-endurecer-app` com a `main` do lab (fast-forward: o branch nao tem commits proprios).
  Pasta: `/home/igor/orca/workspaces/lab/T-0015-endurecer-app`
  Comando: `git merge --ff-only main`
  Esperado: HEAD em `8bda48f` (ou a main atual), com T-0010 (`518b7c5`) e T-0014 (`8bda48f`).

## Motivo

O branch esta em `f1b9e31` e `git log HEAD..main` mostra 25 commits a frente (T-0010, T-0014...). Faltam `qualidade/bugs/BUG-T0010-03.md`, o codigo da validacao com Pillow e o `docker-compose.yml` da T-0014, que o cartao manda usar de base ("partir da main depois do merge da T-0014"). Dev nao pode fazer merge/rebase, entao parei sem alterar nada. Cartao permanece em `pronta`.

Coordenador, 2026-10-02, com aprovacao do humano: no worktree da T-0015, `git status` limpo e 0 commits proprios; `git merge --ff-only main` -> `f1b9e31..8bda48f` (fast-forward). O Dev pode retomar.

**Causa:** a `main` local do lab esta 25 commits a frente da `origin/main` (sem push desde a T-0012) e o Orca criou o branch a partir da `origin/main` (`f1b9e31`). Nao e erro do Dev nem do lancador. A copia principal do BRAIN tambem esta 17 commits a frente do remoto.

**Melhoria proposta (ao humano):** (1) push das `main` do lab e do BRAIN depois de cada merge/fechamento (push e via ADM); (2) ao criar worktree no Orca, conferir que o *Branch from* e a `main` local, ou que o remoto esta em dia; (3) candidato a regra no Fluxo de tarefa, passo 2: "antes de criar o worktree, `main` do projeto sem commits a frente do remoto" (via ADM, se o humano quiser).
