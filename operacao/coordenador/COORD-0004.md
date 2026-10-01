---
tipo: pedido-coordenador
id: COORD-0004
status: concluido
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: T-0007
criado: 2026-09-30
atendido_em: 2026-09-30
adm:
tags: [lab, merge, t-0007]
---
# COORD-0004 - Merge da T-0007 na main do projeto lab

<!-- Pedido do humano em 2026-09-30, registrado pelo Revisor. O humano pediu explicitamente um COORD em vez da secao "Pedidos ao Coordenador" do cartao. -->

## Pedido

- [x] Fazer o merge do branch `T-0007-cabecalhos-http` na `main` do projeto lab.
  - **Pasta:** `/home/igor/Documentos/01.GITHUB/BRAIN/projetos/lab` (copia principal, branch `main`, hoje em `971a7da`).
  - **Comando:** `git merge --no-ff T-0007-cabecalhos-http -m "Merge T-0007: cabecalhos de seguranca HTTP (SEC-0005, SEC-0006)"`
  - **Antes do merge:** conferir que a `main` nao recebeu, desde a aprovacao, mudanca em `app/main.py` ou `tests/` que exija nova verificacao (`git log 971a7da..main -- app tests`). Se houver, devolver ao Revisor.
- [x] Depois do merge, remover os volumes de teste do Revisor (dados do VER-0013 e do VER-0014, antes numerados VER-0011/0012; a stack ja esta parada, `down` sem `-v`). Pasta: `/home/igor/orca/workspaces/lab/T-0007-cabecalhos-http`. Comando: `docker volume rm t0007-rev_db_data t0007-rev_uploads`.

## Motivo

A T-0007 foi aprovada no VER-0014 (antes VER-0012; renumerado em `786b9ee`; commit verificado `98e9fd6`). Depois do `git merge main` no branch, o merge na `main` so sai com o VER-0015 sobre o novo HEAD. Seguranca sem bloqueante: SEC-0005 e SEC-0006 `verificado`. O humano pediu o merge ao Revisor, que nao tem permissao de merge (perfil do papel).

Cartao: `operacao/tarefas/T-0007.md`.

---

## Atendimento

Coordenador, 2026-09-30: merge NAO feito. `git log 971a7da..main -- app tests` vazio (ok), mas `git merge-tree` mostra conflito em `qualidade/verificacoes/VER-0011.md`, `VER-0012.md` (numeros ja usados pela T-0006) e `docs/requisitos/requisitos.md`. Com o "sim" do humano, T-0007 devolvida para `revisao` (renumerar VER, Dev faz `git merge main`, novo VER). Pedido continua `aberto` ate o merge.

Coordenador, 2026-09-30 (com o "sim" do humano): VER-0015 aprovado sobre `bebf6d5`; `main` (`971a7da`) ancestral do branch; nenhum BUG/SEC aberto da T-0007. Merge feito na `main` do lab: `bbf0f55` (`Merge T-0007: ...`, trailer `Tarefa: T-0007`), sem conflito. Volumes `t0007-rev_db_data` e `t0007-rev_uploads` removidos com `docker volume rm`.
